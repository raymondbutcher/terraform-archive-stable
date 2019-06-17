import datetime
import os
import time

from pretf.api import block
from pretf.test import SimpleTest
from pretf.workflow import delete_files


class TestModule(SimpleTest):
    def test_init(self):

        # Clean up old files are prepare for these tests.
        delete_files("*.json")
        if not os.path.exists("src"):
            os.mkdir("src")

        with self.create("main.tf.json"):

            archive = yield block(
                "module",
                "archive",
                {
                    "source": "../",
                    "source_dir": "src",
                    "output_path": "out.zip",
                    "search": ["*.txt"],
                },
            )

            yield block("output", "output_md5", {"value": archive.output_md5})
            yield block("output", "search_results", {"value": archive.search_results})

        self.init()

    def test_changes(self):
        delete_files("src/*")

        # Create archive.
        with open("src/one.txt", "w") as open_file:
            open_file.write("a")
        outputs = self.apply()
        assert outputs["search_results"] == ["one.txt"]
        first_output_md5 = outputs["output_md5"]

        # Change contents and affect the hash and search results.
        with open("src/two.txt", "w") as open_file:
            open_file.write("b")
        outputs = self.apply()
        assert outputs["search_results"] == ["one.txt", "two.txt"]
        second_output_md5 = outputs["output_md5"]
        assert first_output_md5 != second_output_md5

    def test_permissions(self):
        delete_files("src/*")

        # Create archive.
        with open("src/one.txt", "w") as open_file:
            open_file.write("a")
        os.chmod("src/one.txt", 0o644)
        outputs = self.apply()
        first_output_md5 = outputs["output_md5"]

        # Change group permissions without affecting the hash.
        os.chmod("src/one.txt", 0o666)
        outputs = self.apply()
        second_output_md5 = outputs["output_md5"]
        assert second_output_md5 == first_output_md5

        # Change executable permissions and affect the hash.
        os.chmod("src/one.txt", 0o744)
        outputs = self.apply()
        third_output_md5 = outputs["output_md5"]
        assert third_output_md5 != first_output_md5

    def test_timestamps(self):
        delete_files("src/*")

        # Create archive.
        with open("src/one.txt", "w") as open_file:
            open_file.write("a")
        when = time.mktime(datetime.datetime(2017, 7, 7, 7, 7, 7).timetuple())
        os.utime("src/one.txt", (when, when))
        outputs = self.apply()
        first_output_md5 = outputs["output_md5"]

        # Change timestamps without affecting the hash.
        when = time.mktime(datetime.datetime(2012, 2, 2, 2, 2, 2).timetuple())
        os.utime("src/one.txt", (when, when))
        outputs = self.apply()
        third_output_md5 = outputs["output_md5"]
        assert third_output_md5 == first_output_md5
