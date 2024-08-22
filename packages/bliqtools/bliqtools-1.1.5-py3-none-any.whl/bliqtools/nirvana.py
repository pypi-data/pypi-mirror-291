"""
This module is a helper to access files as saved by Nirvana VMS and Lightsheet
from Bliq Photonics.

You can do:
    
    import bliqtools.nirvana

"""

import unittest
import os
import re
from enum import StrEnum
from pathlib import Path
import subprocess
from contextlib import redirect_stderr

from pyometiff import OMETIFFReader, OMEXML


class FileType(StrEnum):
    """
    The types of files produced and recognized by Nirvana
    """

    IMAGE_VMS = "ImageVMS"
    IMAGE_TILE = "ImageTile"
    # Not ready yet
    # IMAGE_LIGHTSHEET = "ImageLightsheet"
    # IMAGE_SPARQ_HI = "ImageSparqHi"
    # IMAGE_SPARQ_LO = "ImageSparqLo"
    # IMAGE_SLAM = "ImageSlam"

    DIRECTORY = "Directory"
    SYSTEM_FILE = "System file"
    UNKNOWN = "Unknown"


class FilePath(Path):
    """
    An extension to the Path class of PathLib to include metadata obtained from the filename itself
    """

    patterns = {
        FileType.IMAGE_VMS: {
            "regex": r"-([^-.]+?)-Ch-(\d)-Frame_(\d+)-Time_(\d.+?)s",
            "groups": ["provider", "channel", "frame", "time"],
            "types": [str, int, int, float],
        },
        FileType.IMAGE_TILE: {
            "regex": r"VOI.(\d+).X(\d+?).Y(\d+?).Z(\d+?).C(\d+).T(\d+)",
            "groups": ["voi", "i", "j", "k", "channel", "time"],
            "types": [int, int, int, int, int, int],
        },
        FileType.SYSTEM_FILE: {
            "regex": r"^\..+",
            "groups": [],
            "types": [],
        },
    }

    registered_metadata = [
        "provider",
        "channel",
        "frame",
        "time",
        "filetype",
        "i",
        "j",
        "k",
        "voi",
    ]

    def __init__(self, *args):
        """
        Initializing file from complete filepath
        """
        super().__init__(*args)

        self.metadata = self.extract_metadata()

    def __getattribute__(self, name):
        if name in FilePath.registered_metadata:
            return self.metadata.get(name, None)

        return super().__getattribute__(name)

    @classmethod
    def is_nirvana_filetype(cls, filepath):
        """
        Returns if a name is a valid Nirvana file name before creating an object File
        """
        metadata = FilePath(filepath).metadata

        if metadata["filetype"] != FileType.UNKNOWN:
            return True

        return False

    @property
    def ome_tiff(self):
        """
        Returns a dictionary containing the OME-TIFF metadata
        """
        return self.metadata.get("ome-tiff", None)

    @property
    def ome_xml(self):
        """
        Return an object to access the OME-XML properties. To obtain the text, use self.metadata['ome-xml']
        See documentation at https://github.com/filippocastelli/pyometiff/blob/main/pyometiff/omexml.py
        """
        ome_xml = self.metadata.get("ome-xml", None)
        if ome_xml is not None:
            return OMEXML(ome_xml)
        return None

    def extract_metadata(self):
        """
        Extract all metadata available (from filename, and OME TIFF)
        """
        metadata = {}

        filename_metadata = self.extract_filename_metadata()

        metadata.update(filename_metadata)

        filetype = filename_metadata["filetype"]
        if filetype in [FileType.IMAGE_VMS, FileType.IMAGE_TILE]:
            ome_metadata, xml_metadata = self.extract_ome_metadata()

            if ome_metadata is not None:
                metadata["ome-tiff"] = ome_metadata
            if xml_metadata is not None:
                metadata["ome-xml"] = xml_metadata

        return metadata

    def extract_filename_metadata(self):
        """
        Extract metadata from filename
        """

        filepath = self

        metadata = {"filetype": FileType.UNKNOWN, "filepath": str(filepath)}
        if Path(filepath).is_dir():
            metadata["filetype"] = FileType.DIRECTORY

        filename = Path(filepath).name
        for filetype, matching_info in self.patterns.items():
            match = re.search(matching_info["regex"], filename)
            if match is not None:
                for i, name in enumerate(matching_info["groups"]):
                    cast_type = matching_info["types"][i]
                    metadata[name] = cast_type(match.group(i + 1))
                metadata["filetype"] = filetype

        return metadata

    def extract_ome_metadata(self):
        """
        Extract OME metadata from TIFF file when available
        """

        if self.exists():
            with redirect_stderr(
                None
            ):  # Suppress the stderr when OME metadata not available
                reader = OMETIFFReader(fpath=self)
                _, metadata, xml_metadata = reader.read()
                return metadata, xml_metadata
        else:
            return None, None

    def write_xattr(self, prefix="bliq.nirvana"):
        """
        On macOS (Darwin) and Linux, extended attributes are available in the file system
        We write our metadata extracted from the filename to the extended attribute of the file
        By default, the prefix "bliq.nirvana" is added to the metadata property.
        """
        for key, value in self.metadata.items():
            if key != "filepath":
                job = subprocess.run(
                    ["xattr", "-w", f"{prefix}.{key}", f"{value}", str(self)],
                    check=True,
                )
                if job.returncode != 0:
                    raise RuntimeError(
                        f"Unable to set extended attributes for file {self}"
                    )

    def delete_xattr(self, prefix="bliq.nirvana"):
        """
        On macOS (Darwin) and Linux, extended attributes are available in the file system
        We delete our metadata previoulsy written to the extended attribute of the file
        By default, the prefix "bliq.nirvana" is added to the metadata property.
        """
        for key, _ in self.metadata.items():
            if key != "filepath":
                job = subprocess.run(
                    ["xattr", "-d", f"{prefix}.{key}", str(self)], check=True
                )
                if job.returncode != 0:
                    raise RuntimeError(
                        f"Unable to delete extended attributes for file {self}"
                    )

    def contents(self, ignore_system_files=True):
        """
        Returns the content of a directory as a list of FilePath objects
        By default, will ignore system files (defined as beginning with a dot)
        """
        filepaths = []
        for filename in os.listdir(self):
            filepath = FilePath(self, filename)
            if not ignore_system_files or filepath.filetype != FileType.SYSTEM_FILE:
                filepaths.append(filepath)

        return filepaths


class TestClasses(unittest.TestCase):
    """
    Unittesting demonstrating use of classes.

    """

    test_dir = "./test_data"
    filepath = Path(
        test_dir,
        "Test-001",
        "FLIR camera-Ch-1",
        "Test-001-FLIR camera-Ch-1-Frame_002377-Time_0.023s.tif",
    )
    large_FilePath = ""
    nirvana_dir = Path(test_dir, "Test-001")
    channel_dir = Path(test_dir, "Test-001", "FLIR camera-Ch-1")

    def short_test_id(self):
        """
        Simple function to identify running test
        """
        return self.id().split(".")[
            -1
        ]  # Remove complete class name before the function name

    def test_check_metadata(self):
        """
        Extract metadata from filename
        """
        nirvana_file = FilePath(self.filepath)
        self.assertIsNotNone(nirvana_file)
        metadata = nirvana_file.metadata
        self.assertIsNotNone(metadata)
        self.assertEqual(metadata["provider"], "FLIR camera")
        self.assertEqual(metadata["channel"], 1)
        self.assertEqual(metadata["frame"], 2377)
        self.assertEqual(metadata["time"], 0.023)
        self.assertEqual(metadata["filetype"], FileType.IMAGE_VMS)

    def test_get_metadata_as_properties(self):
        """
        Meta data properties are accessible as Python properties
        """
        nirvana_file = FilePath(self.filepath)
        self.assertIsNotNone(nirvana_file)
        self.assertEqual(nirvana_file.provider, "FLIR camera")
        self.assertEqual(nirvana_file.channel, 1)
        self.assertEqual(nirvana_file.frame, 2377)
        self.assertEqual(nirvana_file.time, 0.023)
        self.assertEqual(nirvana_file.filetype, FileType.IMAGE_VMS)

    def test_init_valid_nirvana_filepath(self):
        """
        The FilePath must exist and be a directory
        """
        f = FilePath("/tmp")
        self.assertIsNotNone(f)

    def test_get_files(self):
        """
        The FilePath must contain Nirvana files with understandable metadata
        """

        f = FilePath(self.channel_dir)
        self.assertIsNotNone(f)
        files = f.contents()
        self.assertIsNotNone(files)
        self.assertTrue(len(files) == 3)

    def test_get_all_metadata_from_filepath(self):
        """
        We can obtain a list of metadata for each file, and it must include filepath
        """
        f = FilePath(self.channel_dir)
        metadata = [filepath.metadata for filepath in f.contents()]
        self.assertEqual(len(metadata), 3)
        self.assertIsNotNone(metadata[0]["filepath"])

    def test_is_a_nirvana_file(self):
        """
        Check if name is valid before creating object
        """
        self.assertTrue(FilePath.is_nirvana_filetype(self.filepath))
        self.assertFalse(FilePath.is_nirvana_filetype("/tmp/123.tif"))

    @unittest.skip("No access")
    def test_large_filepath(self):
        """
        Retrieve large number of files from directory (only tested locally)
        """
        f = FilePath(self.large_FilePath)
        self.assertIsNotNone(f)
        files = f.get_nirvana_files()
        self.assertTrue(len(files) > 60_000)

    def test_is_file(self):
        """
        We can still use the functions of the parent Path. Check that it is a file
        """
        nirvana_file = FilePath(self.filepath)
        self.assertTrue(nirvana_file.is_file())

    def test_is_dir(self):
        """
        We can still use the functions of the parent Path. Check that it is a directory
        """
        nirvana_file = FilePath(self.test_dir)
        self.assertTrue(nirvana_file.is_dir())

    def test_dir_content(self):
        """
        We can obtain the contents of a directory as an array of FilePaths
        """
        nirvana_file = FilePath(self.test_dir, "Test-001", "FLIR camera-Ch-1")

        images = [
            filepath
            for filepath in nirvana_file.contents()
            if filepath.filetype == FileType.IMAGE_VMS
        ]
        self.assertEqual(len(images), 3)

    def test_filetypes(self):
        """
        Each FileType is recognized from a regular expression of the filename.
        """
        self.assertEqual(
            FilePath(
                "test_data/Test-001-FLIR camera-Ch-1-Frame_002377-Time_0.023s.tif"
            ).filetype,
            FileType.IMAGE_VMS,
        )
        self.assertEqual(
            FilePath("test_data/Test-001-VOI_1_X001_Y002_Z003_C1-T0.tif").filetype,
            FileType.IMAGE_TILE,
        )
        self.assertEqual(FilePath("test_data/.DS_Store").filetype, FileType.SYSTEM_FILE)
        self.assertEqual(FilePath("test_data").filetype, FileType.DIRECTORY)
        self.assertEqual(FilePath("whatever").filetype, FileType.UNKNOWN)

    def test_write_xattr(self):
        """
        Test that we can write the metadata as extended attributes of a file
        """
        f = FilePath(
            "test_data/Test-001/FLIR camera-Ch-1/Test-001-FLIR camera-Ch-1-Frame_002377-Time_0.023s.tif"
        )
        self.assertTrue(f.exists())
        f.write_xattr()

    def test_write_delete_xattr(self):
        """
        Test that we can delete the metadata as extended attributes of a file
        """
        f = FilePath(
            "test_data/Test-001/FLIR camera-Ch-1/Test-001-FLIR camera-Ch-1-Frame_002379-Time_0.067s.tif"
        )
        self.assertTrue(f.exists())
        f.write_xattr()
        f.delete_xattr()

    def test_ome_metadata(self):
        """
        Test showing that we can extract OME metadata from TIFF files
        """
        f = FilePath("test_data/image-008-VOI_1-X001-Y001-Z001-C1-T001.tif")
        ome_metadata, xml_metadata = f.extract_ome_metadata()
        self.assertIsNotNone(ome_metadata)
        self.assertTrue(type(ome_metadata), dict)
        self.assertTrue(len(ome_metadata) > 0)
        self.assertIsNotNone(xml_metadata)
        self.assertTrue(type(xml_metadata), str)
        self.assertTrue(len(xml_metadata) > 0)

    def test_ome_tiff_properties_metadata(self):
        """
        Test showing that we can extract OME metadata from TIFF files
        """
        f = FilePath("test_data/image-008-VOI_1-X001-Y001-Z001-C1-T001.tif")
        self.assertIsNotNone(f.ome_tiff)
        self.assertTrue(isinstance(f.ome_tiff, dict))
        self.assertIsNotNone(f.ome_xml)
        self.assertTrue(isinstance(f.ome_xml, OMEXML))
        self.assertIsNotNone(f.metadata["ome-xml"])
        self.assertTrue(isinstance(f.metadata["ome-xml"], str))

    def test_ome_xml_metadata(self):
        """
        Explore the OME-XML data provided with OMEXML
        See documentation at https://github.com/filippocastelli/pyometiff/blob/main/pyometiff/omexml.py
        """
        f = FilePath("test_data/image-008-VOI_1-X001-Y001-Z001-C1-T001.tif")
        _, xml_metadata = f.extract_ome_metadata()
        obj = OMEXML(xml_metadata)
        self.assertTrue(isinstance(xml_metadata, str))
        self.assertFalse(isinstance(obj, str))
        self.assertEqual(obj.image().Pixels.channel_count, 1)
        print(f.ome_tiff)
        print(f.ome_xml)


if __name__ == "__main__":
    unittest.main()
