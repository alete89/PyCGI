import unittest
import src.logic.core as core
import os


class TestCore(unittest.TestCase):
    def setUp(self):
        self.dataSet = core.fullDataSet("./test/tabla_test.csv")

    def tearDown(self):
        pass

    def test_getTreeViewInitialPath_from_cfg(self):
        path_esperado = 'InitialPath'
        core.CFG_PATH = os.getcwd() + "/test/cfg_test"
        self.assertEqual(path_esperado, core.getTreeViewInitialPath())

    def test_getTreeViewRootPath_from_cfg(self):
        path_esperado = "pathRoot"
        core.CFG_PATH = os.getcwd() + "/test/cfg_test"
        self.assertEqual(path_esperado, core.getTreeViewRootPath())

    def test_menuOrder(self):
        menu = "archivo"
        menuList = core.subMenuList(menu, self.dataSet)
        ordenEsperado = ["guardar como", "abrir"]
        self.assertEqual(ordenEsperado, menuList)


if __name__ == '__main__':
    unittest.main()
