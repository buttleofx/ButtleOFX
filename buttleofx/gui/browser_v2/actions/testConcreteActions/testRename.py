import unittest
import os
import shutil

import inspect

from OpenGL import GL

from buttleofx.gui.browser_v2.browserItem import BrowserItem
from buttleofx.gui.browser_v2.actions.concreteActions.rename import Rename


class TestRename(unittest.TestCase):
    def setUp(self):
        print("set up")
        self._directory = "buttle_test"
        self._base_path = os.path.expanduser("~")
        self._path = os.path.join(self._base_path, self._directory)

        if os.path.exists(self._path):
            shutil.rmtree(self._path)
        os.makedirs(self._path)

    def test_file_rename(self):
        extension = ".txt"
        old_filename = "plop" + extension
        new_filename = "success" + extension
        open(os.path.join(self._path, old_filename), 'a').close()

        bi = BrowserItem(self._path, old_filename, 1, True)
        re = Rename(bi, new_filename)
        re.process()
        self.assertTrue(self, os.path.exists(os.path.join(self._path, new_filename + extension)))

    def tearDown(self):
        print("tear down")

unittest.main()

