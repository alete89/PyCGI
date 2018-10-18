import unittest
import src.logic.paramFinder as pf


class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_dataset = [
            ['3', 'ver', 'ping', '1', '2', 'ping <ingrese una IP>', '2']
        ]

    def tearDown(self):
        pass

    def test_paramFinder(self):
        comandos, parametros = pf.findParameters(self.test_dataset)
        self.assertEqual(comandos, ["ping"])
        self.assertEqual(parametros, [["ingrese una IP"]])


if __name__ == '__main__':
    unittest.main()
