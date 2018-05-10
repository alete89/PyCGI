import unittest
import src.logic.core as core
import os


class TestCore(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getTreeViewInitialPath_from_cfg(self):
        path_esperado = 'InitialPath'
        core.CFG_PATH = os.getcwd() + "\\test\\cfg_test"
        self.assertEqual(path_esperado, core.getTreeViewInitialPath())

    def test_getTreeViewRootPath_from_cfg(self):
        path_esperado = "pathRoot"
        core.CFG_PATH = os.getcwd() + "\\test\\cfg_test"
        self.assertEqual(path_esperado, core.getTreeViewRootPath())


if __name__ == '__main__':
    unittest.main()
