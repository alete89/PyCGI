import unittest
import src.logic.core as core
import os


class TestCore(unittest.TestCase):
    def setUp(self):
        self.path_esperado = 'PRUEBA'
        print os.getcwd()

    def tearDown(self):
        pass

    def test_cfg_file(self):
        core.CFG_PATH = os.getcwd() + "\\test\\cfg_test"
        self.assertEqual(self.path_esperado, core.getTreeViewInitialPath())


if __name__ == '__main__':
    unittest.main()
