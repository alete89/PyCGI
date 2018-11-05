import unittest
import src.logic.paramFinder as pf


class TestCore(unittest.TestCase):
    def setUp(self):
        self.test_dataset = [
            ['3', 'ver', 'ping', '1', '2', 'comando <un parametro> -p <otro parametro>', '2']
        ]

    def tearDown(self):
        pass

    def test_paramFinder(self):
        comando_completo = pf.getParameters(self.test_dataset)
        print comando_completo
        self.assertEqual(comando_completo,
                         ['3', 'ver', 'ping', '1', '2', 'comando <un parametro> -p <otro parametro>', '2', ["un parametro", "otro parametro"]])


if __name__ == '__main__':
    unittest.main()
