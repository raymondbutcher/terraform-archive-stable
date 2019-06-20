import datetime
import os
import time
from pathlib import Path

from pretf.test import SimpleTest
from pretf.workflow import delete_files


class TestModule(SimpleTest):
    def test_init(self):
        self.init("v1")
        self.destroy("v1")
        if not os.path.exists("src"):
            os.mkdir("src")

    def test_changes(self):
        delete_files("src/*", "out.zip")

        # Create an archive.
        Path("src/one.txt").write_text("a")
        outputs = self.apply("v1")
        assert outputs["search_results"] == ["one.txt"]
        first_output_md5 = outputs["output_md5"]
        assert os.path.exists("out.zip")

        delete_files("out.zip")

        # Add a second file and affect the hash and search results.
        Path("src/two.txt").write_text("b")
        outputs = self.apply("v1")
        assert outputs["search_results"] == ["one.txt", "two.txt"]
        second_output_md5 = outputs["output_md5"]
        assert first_output_md5 != second_output_md5
        assert os.path.exists("out.zip")

        delete_files("out.zip")

        # Change the file contents and affect the hash.
        Path("src/two.txt").write_text("c")
        outputs = self.apply("v1")
        third_output_md5 = outputs["output_md5"]
        assert third_output_md5 != second_output_md5
        assert os.path.exists("out.zip")

    def test_permissions(self):
        delete_files("src/*", "out.zip")

        # Create an archive.
        Path("src/one.txt").write_text("a")
        os.chmod("src/one.txt", 0o644)
        outputs = self.apply("v1")
        first_output_md5 = outputs["output_md5"]
        assert os.path.exists("out.zip")

        delete_files("out.zip")

        # Change group permissions without affecting the hash.
        os.chmod("src/one.txt", 0o666)
        outputs = self.apply("v1")
        second_output_md5 = outputs["output_md5"]
        assert second_output_md5 == first_output_md5
        assert os.path.exists("out.zip")

        delete_files("out.zip")

        # Change executable permissions and affect the hash.
        os.chmod("src/one.txt", 0o744)
        outputs = self.apply("v1")
        third_output_md5 = outputs["output_md5"]
        assert third_output_md5 != first_output_md5
        assert os.path.exists("out.zip")

    def test_timestamps(self):
        delete_files("src/*", "out.zip")

        # Create an archive.
        Path("src/one.txt").write_text("a")
        when = time.mktime(datetime.datetime(2017, 7, 7, 7, 7, 7).timetuple())
        os.utime("src/one.txt", (when, when))
        outputs = self.apply("v1")
        first_output_md5 = outputs["output_md5"]
        assert os.path.exists("out.zip")

        delete_files("out.zip")

        # Change timestamps without affecting the hash.
        when = time.mktime(datetime.datetime(2012, 2, 2, 2, 2, 2).timetuple())
        os.utime("src/one.txt", (when, when))
        outputs = self.apply("v1")
        third_output_md5 = outputs["output_md5"]
        assert third_output_md5 == first_output_md5
        assert os.path.exists("out.zip")

    def test_disabled(self):
        delete_files("src/*", "out.zip")

        # Use a different configuration that has enabled = false.
        # It will not create an archive.
        Path("src/one.txt").write_text("a")
        outputs = self.apply("v2")
        assert not outputs["output_md5"]
        assert not outputs["search_results"]
        assert not os.path.exists("out.zip")
