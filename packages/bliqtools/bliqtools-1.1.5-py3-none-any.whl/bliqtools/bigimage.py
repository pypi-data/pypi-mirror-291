"""
The purpose of the BigImage class is to provide a method to manage and display a very Big Image
without having to worry too much about the memory restrictions. The image is constructed
by placing blocks of pixels at their positions (i.e. the top corner of the block). 
The class BigImage will return a preview decimated (i.e. reduced) by 'factor' (an integer) to make it manageable
and possible to display reasonably well.  It makes it possible to work with an image that would be several GB without 
sacrificing speed: for instance, and image of 1 GB made of 17x17x2048x2048 images can be displayed in less than a second.

"""

import unittest
import tempfile
import time
import cProfile
from pathlib import Path
from multiprocessing import Pool, cpu_count
from collections import deque
from threading import Thread, RLock
import subprocess
import shutil

import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import tifffile
import psutil

from bliqtools.testing import Progress, MemoryMonitor, TimeIt
from bliqtools.nirvana import FilePath


class BlockEntry:
    """Class for keeping track of an image block, either on disk or in memory.
    An image block is a section of the image (i.e. a numpy array) with its top corner.
    The entry will have its data either in the data property, or on disk, not both.
    """

    cache_previews_in_background = False
    use_cache_previews = False

    def __init__(self, coords, data, image_filepath=None):
        """
        Initialize the entry with the corner coords and the data or the image filepath.
        If we have the data immediately, then we compute previews with a group of useful
        factors since it is not expensive to do so.
        """
        self.coords = coords
        self._data = data
        self.image_filepath = image_filepath
        self._saved_filepath = None
        self.last_access = None
        self.previews = {}
        self._lock = RLock()

        self._shape = None
        if data is not None:
            self._shape = data.shape

        if self._data is not None:
            self.cache_previews(factors=[16, 32, 64])
        elif BlockEntry.cache_previews_in_background:
            thread = Thread(target=self.cache_previews)
            thread.start()

    def cache_previews(self, factors=None):
        """
        Computes the preview for a given factor and stores them.
        You may need to invalidate the cache manually if you use it.
        """
        with self._lock:
            if BlockEntry.use_cache_previews:
                if factors is None:
                    factors = [16, 32, 64]
                for factor in factors:
                    self.previews[factor] = self.get_preview(factor=factor)

    @property
    def is_purged(self):
        """
        True if the data is not in memory
        """
        with self._lock:
            return self._data is None

    @property
    def data(self):
        """
        Return the numpy data of the entry. If it is not already loaded,
        obtain it from the _saved_filepath if it has been set, or from
        the image_filepath that was passed on init.
        """
        with self._lock:
            if self.is_purged:
                if self._saved_filepath is not None:
                    self._data = np.load(self._saved_filepath)
                else:
                    try:
                        self._data = tifffile.imread(self.image_filepath)
                    except Exception:
                        self._data = np.asarray(Image.open(self.image_filepath))

                self._saved_filepath = None

            return self._data

    @data.setter
    def data(self, new_value):
        """
        Allows assignment to the data block (e.g., self.data *= mask)
        """
        with self._lock:
            self.previews = {}
            self._data = new_value

    @property
    def shape(self):
        """
        Return the shape of the block.  Tries to avoid loading the image data if possible:
        if we had access to the data block before, we saved the shape into _shape.
        If not, we load the data and get the shape from there.
        """
        with self._lock:
            if self._shape is None:
                self._shape = self.data.shape

            return self._shape

    def index_slices(self, factor=1):
        """
        Return the slices (x_min:x_max, y_min:y_max) needed to insert this block into the BigImage
        with the given factor
        """
        return (
            slice(self.coords[0] // factor, (self.coords[0] + self.shape[0]) // factor),
            slice(self.coords[1] // factor, (self.coords[1] + self.shape[1]) // factor),
        )

    def get_preview(self, factor: int):
        """
        Return a version of the block that is 'factor' smaller.  A factor of 1 is the full-sized original image.
        """
        with self._lock:
            if factor in self.previews.keys():
                return self.previews[factor]

            x, y = self.data.shape

            return self.data[0:x:factor, 0:y:factor]

    def get_preview_shape(self, factor: int):
        """
        Return the size of the reduced preview using a formula that matches the exact reduction algorithm
        This avoids round off errors when the shape is not a multiple of the reduction factor
        we use the @property shape from EntryBlock because it is cached, and may avoid reading the actual data.
        """
        with self._lock:
            x, y = self.shape
            return (len(range(0, x, factor)), len(range(0, y, factor)))

    def purge(self, directory):
        """
        Delete from memory the arrays after having saved them in the provided directory.

        """
        with self._lock:
            if not self.is_purged:
                i, j = self.coords
                _saved_filepath = Path(directory, f"Tile@{i}-{j}.npy")
                if not _saved_filepath.exists():
                    np.save(_saved_filepath, self._data)
                    self._saved_filepath = _saved_filepath

                self._data = None
                self.last_access = time.time()

    def cut_block(self, cut_indexes, axis):
        """
        From a list of indexes, cut the image along 'axis' and return the sub blocks as entries.

        This function may not be that useful.  May be removed.
        """
        corrected_indexes = []
        for cut_index in cut_indexes:
            if cut_index < 0:
                corrected_indexes.append(cut_index + self.data.shape[axis])
            else:
                corrected_indexes.append(cut_index)

        split_data = np.split(self.data, corrected_indexes, axis=axis)

        coord_translation = [0]
        coord_translation.extend(corrected_indexes)

        blocks = []
        for i, sub_data in enumerate(split_data):
            translated_coords = list(self.coords)
            translated_coords[axis] += coord_translation[i]

            blocks.append(BlockEntry(coords=translated_coords, data=sub_data))

        return blocks

    def get_overlap_blocks(self, overlap):
        """
        Assuming an overlap of 'overlap' pixels in all directions (top, bottom, left and right),
        cut a block into 9 sub blocks.

        This function may not be that useful.  May be removed.
        """
        entry_strips = self.cut_block(cut_indexes=[overlap, -overlap], axis=0)

        labelled_strips = {
            "-": entry_strips[0],
            "0": entry_strips[1],
            "+": entry_strips[2],
        }

        labelled_entries = {}
        for label, entry_strip in labelled_strips.items():
            strip_cuts = entry_strip.cut_block(cut_indexes=[overlap, -overlap], axis=1)
            labelled_entries[label + "-"] = strip_cuts[0]
            labelled_entries[label + "0"] = strip_cuts[1]
            labelled_entries[label + "+"] = strip_cuts[2]

        return labelled_entries

    @classmethod
    def uniform(cls, shape, value):
        """
        Return a block with a uniform value and a given shape
        """
        block = np.full(shape=shape, fill_value=value)
        return block

    def linear_overlap_mask(self, overlap_in_pixels):
        """
        Calculate the required mask to linearly attenuate the four regions
        of overlap (top, bottom, left and right).
        Notice that the four corners (top-left, top-right bottom-left and bottom-right)
        will be mutiplied twice because they contain both a horizontal mask and a vertical mask.

        This function could be improved with a smoother mask (gaussian, sigmoid, etc)
        """
        mask = np.ones(shape=self.shape, dtype=np.float32)

        individual_masks = self.linear_overlap_masks(overlap_in_pixels)
        for slice_0, slice_1, sub_mask in individual_masks:
            mask[slice_0, slice_1] *= sub_mask

        return mask

    def linear_overlap_masks(self, overlap_in_pixels):
        """
        Calculate the four masks required to linearly attenuate the four regions
        of overlap (top slice, bottom slice, left slice and right slice).
        Notice that the four corners (top-left, top-right bottom-left and bottom-right)
        will be mutiplied twice because they contain both a horizontal mask and a vertical mask.
        """
        if (
            overlap_in_pixels > self.shape[0] / 2
            or overlap_in_pixels > self.shape[1] / 2
        ):
            raise ValueError("Overlap cannot be larger than half the size of the block")

        shape = self.shape

        mask_low0 = np.ones(shape=(overlap_in_pixels, shape[1]), dtype=np.float32)
        mask_high0 = np.ones(shape=(overlap_in_pixels, shape[1]), dtype=np.float32)
        mask_low1 = np.ones(shape=(shape[0], overlap_in_pixels), dtype=np.float32)
        mask_high1 = np.ones(shape=(shape[0], overlap_in_pixels), dtype=np.float32)

        zero_to_one = np.array(np.linspace(0, 1, overlap_in_pixels), dtype=np.float32)
        one_to_zero = np.array(np.linspace(1, 0, overlap_in_pixels), dtype=np.float32)

        for k in range(shape[0]):
            mask_low1[k, :] *= zero_to_one

        for k in range(shape[1]):
            mask_low0[:, k] *= zero_to_one

        for k in range(shape[0]):
            mask_high1[k, :] *= one_to_zero

        for k in range(shape[1]):
            mask_high0[:, k] *= one_to_zero

        return [
            (slice(0, overlap_in_pixels), slice(0, shape[1]), mask_low0),
            (range(-overlap_in_pixels, 0, 1), slice(0, shape[1]), mask_high0),
            (slice(0, shape[0]), slice(0, overlap_in_pixels), mask_low1),
            (slice(0, self.shape[0]), range(-overlap_in_pixels, 0, 1), mask_high1),
        ]

    def apply_mask(self, mask):
        """
        Multiplies the data block by a mask of the same size.  The multiplication is upgraded
        to the dtype of the mask, then cast back to the original type of the data. If the mask makes the data
        go over the maximum range of the original type, it will roll over.
        """
        self.data = np.multiply(self.data, mask).astype(self.data.dtype)

    def apply_partial_masks(self, masks_with_slices):
        """
        Go through the list and apply all masks
        """
        for slice_0, slice_1, mask in masks_with_slices:
            self.apply_partial_mask(slice_0, slice_1, mask)

    def apply_partial_mask(self, slice_0, slice_1, mask):
        """
        Multiplies the data block by a mask of a smaller size.  The multiplication is upgraded
        to the dtype of the mask, then cast back to the original type of the data.
        """
        self.data[slice_0, slice_1] = np.multiply(
            self.data[slice_0, slice_1], mask
        ).astype(self.data.dtype)


class BigImage:
    """
    A class for extremely large images that manages memory efficiently to preview a lower resolution version quickly
    """

    def __init__(self, size=None):
        """
        Create BigImage with an expected size. If the size is None, it will be computed
        from the entries when needed in get_preview.  If the provided size is too small
        to accomodate all the images, an error will occur.
        """
        self.size = size
        self.data = None
        self.other_resolutions = []
        self.entries = []
        self._work_dir = tempfile.TemporaryDirectory()

    def __del__(self):
        """
        To avoid warnings, we explicitly cleanup the temporary directory
        """
        self._work_dir.cleanup()

    def add_block(self, coords, data=None, image_filepath=None):
        """
        The data from the numpy array 'data' goes to pixel "coords" in the large image

        BlockEntries are kept in a simple list that is used to reconstruct the low resolution version
        """
        if data is None and image_filepath is None:
            raise ValueError("You must provide either the numpy data or an image file")

        self.entries.append(
            BlockEntry(coords=coords, data=data, image_filepath=image_filepath)
        )

    def add_entry(self, entry):
        """
        Adds an entry to the entries.  It could be an already-loaded image or a filepath, we do not
        concern ourselves with the details.
        """
        self.entries.append(entry)

    def purge_if_needed(self):
        """
        Purges if process memory is getting too large
        """
        process = psutil.Process()
        memory_used_by_process_in_gb = process.memory_info().rss
        memory_available_in_gb = psutil.virtual_memory().available
        total_memory = memory_used_by_process_in_gb + memory_available_in_gb
        if memory_used_by_process_in_gb / total_memory > 0.9:
            self.purge()

    def purge(self):
        """
        Purges arrays from memory and save everything to disk
        """
        for entry in self.entries:
            entry.purge(directory=self._work_dir.name)

    def calculate_size(self, factor=1):
        """
        Calculate the size of the image considering the tiles present with a reduction factor
        """
        max_x = 0
        max_y = 0
        for entry in self.entries:
            small_shape = entry.get_preview_shape(factor=factor)
            max_x = max(entry.coords[0] // factor + small_shape[0], max_x)
            max_y = max(entry.coords[1] // factor + small_shape[1], max_y)
        return max_x, max_y

    def get_reduced_resolution_preview(self, factor=16, progress=None):
        """
        Put together all blocks in a reduced version of the final image, reduced
        by a a value of "factor" (i.e. factor 2 is half the size, 1 is the original size)
        Nothing fancy for overlap: just overwrite the data. If a size
        was provided, it must be large enough to contain the blocks
        """

        small_width, small_height = self.calculate_size(factor)

        preview = None

        if progress is None:
            progress = Progress(total=len(self.entries), delay_before_showing=1)

        with progress as p:
            for entry in self.entries:
                small_block = entry.get_preview(factor=factor)
                scaled_x, scaled_y = (
                    entry.coords[0] // factor,
                    entry.coords[1] // factor,
                )

                slice0 = slice(scaled_x, scaled_x + small_block.shape[0])
                slice1 = slice(scaled_y, scaled_y + small_block.shape[1])

                if preview is None:
                    preview = np.zeros(
                        shape=(small_width, small_height), dtype=small_block.dtype
                    )

                preview[slice0, slice1] += small_block
                self.purge_if_needed()
                p.next()

        return preview

    def get_reduced_resolution_block(self, coords, factor=1):
        """
        Get a reduced preview for a block at given coordinates if available
        """
        for entry in self.entries:
            if entry.coords == coords:
                return entry.get_preview(factor)
        return None


class TestBigImage(unittest.TestCase):
    """
    Several tests for BigImage and understanding its details
    """

    img_graph_path = None

    @classmethod
    def setUpClass(cls):
        cls.img_graph_path = "/tmp/Graphs"
        shutil.rmtree(cls.img_graph_path)

        Path(cls.img_graph_path).mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        subprocess.run(["open", cls.img_graph_path], check=True)

    def test_01_init(self):
        """
        We can create a BigImage object
        """
        img = BigImage()
        self.assertIsNotNone(img)

    def test_02_add_block(self):
        """
        We can add a block to a BigImage object
        """
        img = BigImage()
        small_block = np.ones(shape=(10, 10), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)
        self.assertEqual(len(img.entries), 1)

    def test_03_tempdir(self):
        """
        Understanding how tempfile.TemporaryDirectory() works.
        We need to keep the reference to the object, will
        not use it for now.
        """
        tdir = tempfile.TemporaryDirectory()
        tdir.cleanup()

    def test_04_add_many_blocks(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Block", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.random.randint(
                            0, 255, size=(10_00, 10_00), dtype=np.uint8
                        )
                        img.add_block(coords=(i, j), data=small_block)
                        p.next()

        self.assertEqual(len(img.entries), 100)

    def test_05_purge_actually_clears_memory(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        small_block = np.random.randint(0, 255, size=(10_00, 10_00), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)

        self.assertFalse(img.entries[0].is_purged)

        img.entries[0].purge(img._work_dir.name)

        self.assertTrue(img.entries[0].is_purged)

    def test_06_add_many_blocks_with_purge(self):
        """
        We can add a block to a BigImage object
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.zeros(shape=(10_000, 10_000), dtype=np.uint8)
                        img.add_block(coords=(i * 10_000, j * 10_000), data=small_block)
                        p.next()
                    img.purge_if_needed()

        self.assertEqual(len(img.entries), 100)

    def test_07_add_block_get_reduced_version(self):
        """
        Can we get a reduced version of a block?

        """

        img = BigImage()
        small_block = np.random.randint(0, 255, size=(10_000, 10_000), dtype=np.uint8)
        img.add_block(coords=(0, 0), data=small_block)
        reduced_block = img.get_reduced_resolution_block((0, 0), factor=10)
        self.assertEqual(reduced_block.shape, (1000, 1000))

    def test_08_get_reduced_preview(self):
        """
        Extract a reduced dimension preview from the BigImage
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.full(
                            shape=(1_000, 1_000), fill_value=10 * i + j, dtype=np.uint8
                        )
                        img.add_block(coords=(i * 1_000, j * 1_000), data=small_block)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=20)
        self.assertEqual(preview.shape, (500, 500))
        plt.imshow(preview, interpolation="nearest")
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_09_get_reduced_preview_missing_blocks(self):
        """
        Extract a reduced dimension preview from the BigImage
        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(i):
                        small_block = np.full(
                            shape=(1_000, 1_000), fill_value=10 * i + j, dtype=np.uint8
                        )
                        img.add_block(coords=(i * 1_000, j * 1_000), data=small_block)
                        p.next()

        self.assertEqual(img.calculate_size(), (10000, 9000))
        preview = img.get_reduced_resolution_preview(factor=20)
        self.assertEqual(preview.shape, (500, 450))

        plt.imshow(preview, interpolation="nearest")
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def cheap_tile_loader_knock_off(self, filepaths):
        """
        This function mimicks the behaviour of TileLoader because I do not want to import it
        for testing here.

        Returns the number of tiles in i,j,k
        """
        i = set()
        j = set()
        k = set()
        for filepath in filepaths:
            i.add(filepath.i)
            j.add(filepath.j)
            k.add(filepath.k)

        some_filepath = filepaths[0]
        some_entry = BlockEntry(coords=(0, 0), data=None, image_filepath=some_filepath)
        w, h = some_entry.data.shape

        return len(i), len(j), len(k), w, h

    def test_10_from_real_dataset_attempt(self):
        """
        This assumes a dataset at path, with Nirvana-style tiles.
        We work with the first layer only.
        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        _, _, _, w, h = self.cheap_tile_loader_knock_off(layer1_filepaths)

        img = BigImage()
        with TimeIt(description="Real dataset"):
            with Progress(total=len(layer1_filepaths), show_every=400) as p:
                for filepath in layer1_filepaths:
                    pixel_x = (filepath.i - 1) * w
                    pixel_y = (filepath.j - 1) * h

                    entry = BlockEntry(
                        coords=(pixel_x, pixel_y), data=None, image_filepath=filepath
                    )
                    img.add_entry(entry)
                    p.next()
            with cProfile.Profile() as profiler:
                with MemoryMonitor():
                    preview = img.get_reduced_resolution_preview(factor=32)
                    profiler.print_stats("time")

        plt.imshow(preview, interpolation="nearest")
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_11_pil_thumbnail(self):
        """
        PIL offers a function to create a thumbnail of an image.
        Unfortunately, this is not faster than either numpy slicing or scipy
        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        some_filepath = layer1_filepaths[0]
        with TimeIt():
            with Image.open(some_filepath) as im:
                _ = im.thumbnail((64, 64))

    def test_12_tifffile_writes_images_as_tiles(self):
        """
        Tifffile can write "tiled" images. This attempts to use the feature
        to try to see if it means what I think it means, but when the file
        is opened, I see multiple pages, nto a single image.
        Not sure what to do with this.
        """
        data = np.random.rand(2, 5, 3, 301, 219).astype("float32")
        tifffile.imwrite(
            "/tmp/temp.tif",
            data,
            bigtiff=True,
            photometric="rgb",
            planarconfig="separate",
            tile=(32, 32),
            compression="zlib",
            compressionargs={"level": 8},
            predictor=True,
            metadata={"axes": "TZCYX"},
        )

    def test_13_get_fast_preview_from_cache(self):
        """
        When loading entries directly with data, the BlockEntry class
        will keep a preview reduced by a factor 16.  Making the preview will be really fast

        """

        img = BigImage()
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.full(
                            shape=(1_024, 1_024), fill_value=10 * i + j, dtype=np.uint8
                        )
                        img.add_block(coords=(i * 2048, j * 2048), data=small_block)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=32)
        plt.imshow(preview)
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    @unittest.skip("No gain at all from calculating in parallel.")
    def test_14_compute_previews_in_parallel(self):
        """
        This assumes a dataset at path, with Nirvana-style tiles.
        We work with the first layer only.
        """

        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        _, _, _, w, h = self.cheap_tile_loader_knock_off(layer1_filepaths)

        img = BigImage()

        for filepath in layer1_filepaths:
            pixel_x = (filepath.i - 1) * w
            pixel_y = (filepath.j - 1) * h

            entry = BlockEntry(
                coords=(pixel_x, pixel_y), data=None, image_filepath=filepath
            )
            img.add_entry(entry)

        with TimeIt():
            for entry in img.entries:
                compute_previews(entry)

        with TimeIt():
            with Pool(5) as p:
                p.map(compute_previews, img.entries)

    def reslice_block(self, coords, block, cut_indexes, axis):
        """
        Function used for development of the test below.
        """
        sub_blocks = np.split(block, cut_indexes, axis=axis)

        start_pos = [0]
        start_pos.extend(cut_indexes)

        blocks_with_positions = []
        for i, sub_block in enumerate(sub_blocks):
            sub_block_coords = list(coords)
            sub_block_coords[axis] += start_pos[i]
            blocks_with_positions.append((sub_block, tuple(sub_block_coords)))

        return blocks_with_positions

    def test_breakup_tiles_in_smaller_tiles_from_overlap(self):
        """
        Attempt at managing overlap by breaking down tiles in smaller tiles.
        As will be seen below, this is not the best strategy and leaves many artifacts
        in the final image.

        This test is one of the first step in that direction.
        """
        small_block = np.full(shape=(1_024, 1_024), fill_value=128, dtype=np.uint8)

        overlap_in_pixels = 100
        sub_tiles = np.split(
            small_block, [overlap_in_pixels, 1024 - overlap_in_pixels], axis=0
        )
        self.assertEqual(len(sub_tiles), 3)
        self.assertEqual(sub_tiles[0].shape, (overlap_in_pixels, 1024))
        self.assertEqual(sub_tiles[1].shape, (1024 - 2 * overlap_in_pixels, 1024))
        self.assertEqual(sub_tiles[2].shape, (overlap_in_pixels, 1024))
        all_sub_tiles = []
        for sub_tile in sub_tiles:
            all_sub_tiles.extend(
                np.split(
                    sub_tile, [overlap_in_pixels, 1024 - overlap_in_pixels], axis=1
                )
            )

    def test_breakup_tiles_in_smaller_tiles_from_overlap_with_function(self):
        """
        Attempt at managing overlap by breaking down tiles in smaller tiles.
        As will be seen below, this is not the best strategy and leaves many artifacts
        in the final image.

        This test is the second step in that direction.

        """
        small_block = np.full(shape=(1_024, 1_024), fill_value=128, dtype=np.uint8)

        expected_coords = ((0, 0), (100, 0), (924, 0))
        expected_shapes = ((100, 1024), (824, 1024), (100, 1024))
        sub_blocks = self.reslice_block(
            coords=(0, 0), block=small_block, cut_indexes=[100, 1024 - 100], axis=0
        )
        for i, (sub_block, sub_coords) in enumerate(sub_blocks):
            self.assertEqual(sub_coords, expected_coords[i])
            self.assertEqual(sub_block.shape, expected_shapes[i])

        expected_coords = ((0, 0), (0, 100), (0, 924))
        expected_shapes = ((1024, 100), (1024, 824), (1024, 100))
        sub_blocks = self.reslice_block(
            coords=(0, 0), block=small_block, cut_indexes=[100, 1024 - 100], axis=1
        )
        for i, (sub_block, sub_coords) in enumerate(sub_blocks):
            self.assertEqual(sub_coords, expected_coords[i])
            self.assertEqual(sub_block.shape, expected_shapes[i])

    def test_reslice_blockentries(self):
        """
        Attempt at managing overlap by breaking down tiles in smaller tiles.
        As will be seen below, this is not the best strategy and leaves many artifacts
        in the final image.

        This test is the third step in that direction.
        """

        data = np.full(shape=(1_024, 1_024), fill_value=128, dtype=np.uint8)
        start_entry = BlockEntry(coords=(0, 0), data=data)
        entries = start_entry.cut_block(cut_indexes=[100, 924], axis=0)

        axis = 0
        for i in [0, 1]:
            entry = entries[i]
            next_entry = entries[i + 1]
            self.assertEqual(
                entry.coords[axis] + entry.data.shape[axis], next_entry.coords[axis]
            )

        axis = 1
        for entry in entries:
            cut_entries = entry.cut_block(cut_indexes=[100, 924], axis=1)
            for i in [0, 1]:
                entry = cut_entries[i]
                next_entry = cut_entries[i + 1]
                self.assertEqual(
                    entry.coords[axis] + entry.data.shape[axis], next_entry.coords[axis]
                )

    def test_reslice_blockentries_negative_cut_from_end(self):
        """
        Attempt at managing overlap by breaking down tiles in smaller tiles.
        As will be seen below, this is not the best strategy and leaves many artifacts
        in the final image.

        Here, provide negative indices for the right so we don't need to know the size of the block we cut
        """
        data = np.full(shape=(1_024, 1_024), fill_value=128, dtype=np.uint8)
        start_entry = BlockEntry(coords=(0, 0), data=data)
        entries = start_entry.cut_block(cut_indexes=[100, -100], axis=0)

        axis = 0
        for i in [0, 1]:
            entry = entries[i]
            next_entry = entries[i + 1]
            self.assertEqual(
                entry.coords[axis] + entry.data.shape[axis], next_entry.coords[axis]
            )

        axis = 1
        for entry in entries:
            cut_entries = entry.cut_block(cut_indexes=[100, -100], axis=1)
            for i in [0, 1]:
                entry = cut_entries[i]
                next_entry = cut_entries[i + 1]
                self.assertEqual(
                    entry.coords[axis] + entry.data.shape[axis], next_entry.coords[axis]
                )

    def test_20_preview_with_cut_blocks(self):
        """
        A small digression that turned out to be not so useful: cahcing a preview.

        When loading entries directly with data, the BlockEntry class
        will keep a preview reduced by a factor 16.  Making the preview will be really fast.

        However, if we perform computation on the block, then the cached preview interferes.

        """

        img = BigImage()
        overlap = 400
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(4):
                    for j in range(4):
                        small_block = np.full(
                            shape=(2048, 2048),
                            fill_value=20 * i + 5 * j,
                            dtype=np.uint8,
                        )
                        entry = BlockEntry(
                            coords=(i * (2048 - overlap), j * (2048 - overlap)),
                            data=small_block,
                        )
                        entry_strips = entry.cut_block(
                            cut_indexes=[overlap, -overlap], axis=0
                        )

                        entry_strips[0].data //= 2
                        entry_strips[2].data //= 2

                        cut_entries = []
                        for entry_strip in entry_strips:
                            strip_cuts = entry_strip.cut_block(
                                cut_indexes=[overlap, -overlap], axis=1
                            )
                            strip_cuts[0].data //= 2
                            strip_cuts[2].data //= 2
                            cut_entries.extend(strip_cuts)

                        for entry in cut_entries:
                            img.add_entry(entry)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=4)
        plt.imshow(preview)
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_21_preview_with_cut_overlap_blocks(self):
        """
        Now that all necessary functions have been created and tested,
        this is the real first attempt(eventually unsuccessful) to try to cut the block in sub-blocks to manage
        each overlap section individually.

        Here, I test a simple average (divide by 2 for edges and 4 for corners).

        Unfortunately, applying the reduction on small blocks may result in glitches at the edges
        if the overlap length is not a multiple of the reduction factor, or if the block size
        is not a multiple either.  Overall, bad idea to split the block to treat them,
        the next tests will apply the mask directly onto the whole block.

        It is quite obvious in the final figure shown/saved.

        """

        img = BigImage()
        overlap = 100

        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(10):
                    for j in range(10):
                        small_block = np.full(
                            shape=(2048, 2048),
                            fill_value=20 * i + 5 * j,
                            dtype=np.uint8,
                        )
                        entry = BlockEntry(
                            coords=(i * (2048 - overlap), j * (2048 - overlap)),
                            data=small_block,
                        )
                        overlapped_entries = entry.get_overlap_blocks(overlap=overlap)

                        overlapping_labels = list(overlapped_entries.keys())
                        overlapping_labels.remove("00")  # center

                        for label in overlapping_labels:
                            if label in ["++", "--", "-+", "+-"]:  # Need to correct 2x
                                correction = 4
                            else:
                                correction = 2
                            entry = overlapped_entries[label]
                            entry.data //= correction
                            overlapped_entries[label] = entry

                        for label, entry in overlapped_entries.items():
                            img.add_entry(entry)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=32)
        plt.imshow(preview)
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_22_preview_with_cut_overlap_blocks_linear_correction(self):
        """
        Second attempt (also unsuccessful) to try to cut the block in sub-blocks to manage
        each overlap section individually. Here, I test a linear factor but the same problem described here
        is also apparent: applying the reduction on small blocks may result in glitches at the edges
        if the overlap length is not a multiple of the reduction factor, or if the block size
        is not a multiple either.  Overall, bad idea to split the block to treat them,
        the next tests will apply the mask directly onto the whole block.

        """
        BlockEntry.cache_previews_in_background = False
        BlockEntry.use_cache_previews = False
        img = BigImage()

        overlap = 512
        with MemoryMonitor():
            with Progress(total=100, description="Tile", show_every=10) as p:
                for i in range(4):
                    for j in range(4):
                        block = np.full(
                            shape=(2048, 2048),
                            fill_value=20 * i + 5 * j,
                            dtype=np.uint8,
                        )
                        entry = BlockEntry(
                            coords=(i * (2048 - overlap), j * (2048 - overlap)),
                            data=block,
                        )
                        overlapping_entries = entry.get_overlap_blocks(overlap=overlap)

                        overlapping_labels = list(overlapping_entries.keys())

                        for label in overlapping_labels:
                            over_entry = overlapping_entries[label]

                            shape = over_entry.data.shape
                            mask = np.ones(shape=shape, dtype=np.float16)
                            if label[0] == "+":
                                for k in range(shape[1]):
                                    mask[:, k] = np.array(np.linspace(1, 0, shape[0]))
                            elif label[0] == "-":
                                for k in range(shape[1]):
                                    mask[:, k] = np.array(np.linspace(0, 1, shape[0]))

                            if label[1] == "+":
                                for k in range(shape[0]):
                                    mask[k, :] *= np.array(np.linspace(1, 0, shape[1]))
                            elif label[1] == "-":
                                for k in range(shape[0]):
                                    mask[k, :] *= np.array(np.linspace(0, 1, shape[1]))

                            over_entry.data = np.multiply(over_entry.data, mask).astype(
                                np.uint8
                            )

                            img.add_entry(over_entry)

                        # for label, entry in overlapped_entries.items():
                        #     img.add_entry(entry)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=8)
        plt.imshow(preview)
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_23_preview_with_global_mask_correction(self):
        """
        Third strategy, that will tunr out to be very successful:
        We calculate a mask for the whole block that tapers the edges to zero for
        smooth adddition to the map.  The glitch oberved by managing separate sub-blocks
        is gone because there are no sub-blocks.

        """
        BlockEntry.cache_previews_in_background = False
        BlockEntry.use_cache_previews = False
        img = BigImage()

        map_size = (17, 17)
        shape = (2048, 2048)
        overlap = 512

        mask = None

        with MemoryMonitor():
            with Progress(
                total=map_size[0] * map_size[1], description="Tile", show_every=10
            ) as p:
                for i in range(map_size[0]):
                    for j in range(map_size[1]):
                        block = np.full(
                            shape=shape, fill_value=20 * i + 5 * j, dtype=np.uint16
                        )
                        entry = BlockEntry(
                            coords=(i * (shape[0] - overlap), j * (shape[1] - overlap)),
                            data=block,
                        )
                        if mask is None:
                            mask = entry.linear_overlap_mask(overlap_in_pixels=overlap)
                        entry.apply_mask(mask)
                        img.add_entry(entry)
                        p.next()

        preview = img.get_reduced_resolution_preview(factor=64)
        plt.imshow(preview)
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_24_from_real_dataset_attempt(self):
        """
        We test this strategy of a mask applied on each block with a real dataset.
        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        layer1_filepaths = [filepath for filepath in filepaths if filepath.k == 1]
        _, _, _, w, h = self.cheap_tile_loader_knock_off(layer1_filepaths)

        img = BigImage()
        overlap = 250
        masks = None
        with cProfile.Profile() as profiler:
            with TimeIt(description="Real dataset building with mask"):
                with Progress(total=len(layer1_filepaths), show_every=10) as p:
                    for filepath in layer1_filepaths:
                        pixel_x = (filepath.i - 1) * (w - overlap)
                        pixel_y = (filepath.j - 1) * (h - overlap)

                        entry = BlockEntry(
                            coords=(pixel_x, pixel_y),
                            data=None,
                            image_filepath=filepath,
                        )

                        if masks is None:
                            masks = entry.linear_overlap_masks(
                                overlap_in_pixels=overlap
                            )

                        entry.apply_partial_masks(masks)
                        img.add_entry(entry)
                        p.next()
        profiler.print_stats("time")

        preview = img.get_reduced_resolution_preview(factor=8)

        plt.imshow(preview, interpolation="nearest")
        plt.title(self.id())
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    @unittest.skip("This is a very lengthy test (2 minutes). Uncomment to run")
    def test_25_from_real_3d_dataset(self):
        """
        The ultimate test: a very large 3D dataset.
        You should have a big dataset in Downloads/Test_maps/C1

        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        _, _, nk, w, h = self.cheap_tile_loader_knock_off(filepaths)
        overlap = 250
        mask = None
        with MemoryMonitor() as m:
            with TimeIt(description="Real dataset building with mask"):
                with Progress(
                    description="Completing layer", total=nk, show_every=1
                ) as p:
                    for k in range(1, nk + 1):
                        img = BigImage()
                        layer_k_filepaths = [
                            filepath for filepath in filepaths if filepath.k == k
                        ]
                        print(f"Mapping layer {k}")
                        for filepath in layer_k_filepaths:
                            pixel_x = (filepath.i - 1) * (w - overlap)
                            pixel_y = (filepath.j - 1) * (h - overlap)

                            entry = BlockEntry(
                                coords=(pixel_x, pixel_y),
                                data=None,
                                image_filepath=filepath,
                            )

                            if mask is None:
                                mask = entry.linear_overlap_mask(
                                    overlap_in_pixels=overlap
                                )

                            entry.apply_mask(mask)
                            img.add_entry(entry)
                        p.next()

                        preview = img.get_reduced_resolution_preview(factor=1)
                        tifffile.imwrite(f"/tmp/Layer-{k}.tif", preview, bigtiff=True)

                        plt.imshow(preview, interpolation="nearest")
                        plt.title(f"Layer {k} of " + self.id())
                        image_path = Path(self.img_graph_path, self.id() + ".pdf")
                        plt.savefig(image_path)

            m.report_stats()

    @unittest.skip("This is a very lengthy test (2 minutes). Uncomment to run")
    def test_26_from_real_3d_dataset_one_big_tiff(self):
        """
        Again with a large 3D dataset, now save all layers in a single TIFF using the
        contiguous=True option and a contextmanager with tifffile ... as tif:
        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        _, _, nk, w, h = self.cheap_tile_loader_knock_off(filepaths)
        overlap = 250
        mask = None
        with tifffile.TiffWriter(f"/tmp/Big_Image.tif", bigtiff=True) as tif:
            with MemoryMonitor() as m:
                with TimeIt(description="Real dataset building with mask"):
                    with Progress(
                        description="Completing layer", total=nk, show_every=1
                    ) as p:
                        for k in range(1, nk + 1):
                            img = BigImage()
                            layer_k_filepaths = [
                                filepath for filepath in filepaths if filepath.k == k
                            ]
                            print(f"Mapping layer {k}")
                            for filepath in layer_k_filepaths:
                                pixel_x = (filepath.i - 1) * (w - overlap)
                                pixel_y = (filepath.j - 1) * (h - overlap)

                                entry = BlockEntry(
                                    coords=(pixel_x, pixel_y),
                                    data=None,
                                    image_filepath=filepath,
                                )

                                if mask is None:
                                    mask = entry.linear_overlap_mask(
                                        overlap_in_pixels=overlap
                                    )

                                entry.apply_mask(mask)
                                img.add_entry(entry)
                            p.next()

                            preview = img.get_reduced_resolution_preview(factor=1)
                            tif.write(preview, contiguous=True)

                            plt.imshow(preview, interpolation="nearest")
                            plt.title(self.id())
                            image_path = Path(self.img_graph_path, self.id() + ".pdf")
                            plt.savefig(image_path)
                m.report_graph()

    def test_26_from_real_3d_dataset_save_layers_in_thread(self):
        """
        Is it faster to save in a separate thread?

        Short answer: no.

        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        _, _, nk, w, h = self.cheap_tile_loader_knock_off(filepaths)
        overlap = 250
        masks = None
        with cProfile.Profile() as profiler:
            with MemoryMonitor() as m:
                with TimeIt(description="Real dataset building with mask"):
                    with Progress(
                        description="Completing layer", total=nk, show_every=1
                    ) as p:
                        for k in range(1, nk // 3 + 1):
                            img = BigImage()
                            layer_k_filepaths = [
                                filepath for filepath in filepaths if filepath.k == k
                            ]
                            print(f"Mapping layer {k}")
                            for filepath in layer_k_filepaths:
                                pixel_x = (filepath.i - 1) * (w - overlap)
                                pixel_y = (filepath.j - 1) * (h - overlap)

                                entry = BlockEntry(
                                    coords=(pixel_x, pixel_y),
                                    data=None,
                                    image_filepath=filepath,
                                )

                                if masks is None:
                                    masks = entry.linear_overlap_masks(
                                        overlap_in_pixels=overlap
                                    )

                                entry.apply_partial_masks(masks)
                                img.add_entry(entry)
                            p.next()

                            preview = img.get_reduced_resolution_preview(factor=1)
                            thread = Thread(
                                target=tifffile.imwrite,
                                args=(f"/tmp/Layer-{k}.tif", preview),
                                kwargs={"bigtiff": True},
                            )
                            thread.start()

                            plt.imshow(preview, interpolation="nearest")
                            plt.title(f"Layer {k} of " + self.id())
                            image_path = Path(self.img_graph_path, self.id() + ".pdf")
                            plt.savefig(image_path)
            m.report_graph()
        profiler.print_stats("time")

    def test_27_one_layer_one_thread(self):
        """
        Is it faster to do each layer in its own thread?
        The number of thread is hard to estimate: it depends on available cores and memory.

        """
        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()

        _, _, nk, w, h = self.cheap_tile_loader_knock_off(filepaths)
        overlap = 200
        factor = 1
        thread = None

        available_mem = psutil.virtual_memory().available / 1e9
        approximate_task = available_mem // 2

        for k in range(1, nk + 1):
            layer_filepath = f"/tmp/Layer-{k}.tif"
            layer_k_filepaths = [filepath for filepath in filepaths if filepath.k == k]

            thread = Thread(
                target=build_one_layer,
                args=(layer_k_filepaths, k, w, h, overlap, factor, layer_filepath),
            )
            thread.start()

            if k % approximate_task == 0:
                thread.join()

        thread.join()

    def test_28_partial_masks(self):
        """
        Test to use partial masks instead of full mask on blocks.
        It is significantly faster because it performs 50% less calculations at least.
        (Only on overlap, not full image)
        """
        overlap = 200
        shape = (2048, 2048)
        block = np.full(shape=shape, fill_value=128, dtype=np.uint8)
        entry = BlockEntry(
            coords=(0, 0),
            data=block,
        )
        masks = entry.linear_overlap_masks(overlap)
        entry.apply_partial_masks(masks)

        plt.imshow(entry.data)
        image_path = Path(self.img_graph_path, self.id() + ".pdf")
        plt.savefig(image_path)

    def test_29_use_worker_threads_and_deque(self):
        """
        Use worker threads to go through the queue of data to process.
        We allow 4 threads because we have 4 to 8 cores but other processes
        need to run too.
        """

        root_dir = FilePath(Path.home(), "Downloads/Test_maps/C1")
        filepaths = root_dir.contents()
        _, _, nk, w, h = self.cheap_tile_loader_knock_off(filepaths)
        overlap = 200
        factor = 1

        # Fill the queue with data
        queue = deque()  # a deque is MUCH faster and simpler than a Queue
        for k in range(1, nk + 1):
            layer_k_filepaths = [filepath for filepath in filepaths if filepath.k == k]
            layer_filepath = f"/tmp/Layer-{k}.tif"
            queue.appendleft(
                (layer_k_filepaths, k, w, h, overlap, factor, layer_filepath)
            )

        # Start the worker threads
        thread = None
        for _ in range(cpu_count() // 4):
            thread = Thread(target=layer_builder_worker_thread, args=(queue,))
            thread.start()

        thread.join()


def layer_builder_worker_thread(queue):
    """
    Small worker thread that will take data if available to build one layer,
    ifno data available it quits.
    """
    while True:
        try:
            args = queue.pop()
            # Reusing the same function as previous test
            build_one_layer(*args)
        except IndexError:
            break


def build_one_layer(filepaths, k, w, h, overlap, factor, layer_filepath):
    """
    With all the filepaths making up a layer, this function builds the preview of
    the image at 'factor' reduction and saves it to layer_filepath
    """
    masks = None
    img = BigImage()
    layer_k_filepaths = filepaths
    print(f"Building layer {k}")
    with Progress(
        total=len(layer_k_filepaths), show_every=1, description=f"Layer {k} progress"
    ) as p:
        for filepath in layer_k_filepaths:
            pixel_x = (filepath.i - 1) * (w - overlap)
            pixel_y = (filepath.j - 1) * (h - overlap)

            entry = BlockEntry(
                coords=(pixel_x, pixel_y),
                data=None,
                image_filepath=filepath,
            )

            if overlap > 0:
                if masks is None:
                    masks = entry.linear_overlap_masks(overlap_in_pixels=overlap)

                entry.apply_partial_masks(masks)

            img.add_entry(entry)
            img.purge_if_needed()
            p.next()

    print(f"Starting preview for layer {k} at factor {factor}")
    preview = img.get_reduced_resolution_preview(factor=factor)
    tifffile.imwrite(layer_filepath, preview, bigtiff=True)


def compute_previews(entry):
    """
    Function used in the multiprocessing example
    """
    for factor in [16, 32, 64, 128]:
        preview = entry.get_preview(factor=factor)
        entry.previews[factor] = preview


if __name__ == "__main__":
    unittest.main()
    unittest.main(
        defaultTest=["TestBigImage.test_09_get_reduced_preview_missing_blocks"]
    )
