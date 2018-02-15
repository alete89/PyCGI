import unittest
import src.logic.csvdb as csvdb
import src.logic.core as core
import os


class TestCore(unittest.TestCase):
    def setUp(self):
        self.testcsv = "test.csv"
        self.dataset = [
            ['1', 'archivo', 'abrir', '2', '1', 'python ./scripts/abrir.py', '1'],
            ['2', 'edicion', 'copiar', '2', '1',
                'python ./scripts/copiar.py', '5'],
            ['3', 'ver', 'ping', '1', '2', 'ping (ingrese una IP)', '2'],
            ['4', 'archivo', 'guardar como', '1', '1',
                'python ./scripts/guardar.py', '1'],
            ['5', 'edicion', 'pegar', '1', '1', 'python ./scripts/pegar.py', '2'],
            ['6', 'ver', 'ping', '2', '1',
                'ping (ingrese un sitio)(modificador)', '1'],
            ['7', 'Dibujo', 'Paint', '1', '1', 'mspaint', '2'],
            ['8', 'prueba', 'numeros', '1', '2', 'python ./scripts/uno.py', '1'],
            ['9', 'prueba', 'numeros', '2', '3', 'python ./scripts/dos.py', '1'],
            ['10', 'prueba', 'numeros', '3', '4', 'python ./scripts/tres.py', '1'],
            ['11', 'prueba', 'numeros', '4', '1', 'ping (ip)', '1']
        ]
        self.columna = 1
        self.valor = "archivo"
        self.dataset_filtrado_expected = [
            ['1', 'archivo', 'abrir', '2', '1', 'python ./scripts/abrir.py', '1'],
            ['4', 'archivo', 'guardar como', '1', '1',
                'python ./scripts/guardar.py', '1']
        ]
        self.header = ["id", "menu", "submenu", "posicion en menu",
                       "orden en secuencia", "comando", "loop"]

    def tearDown(self):
        try:
            os.remove(self.testcsv)
        except OSError:
            pass

    def test_dataFilter(self):
        self.assertEqual(csvdb.dataFilter(self.dataset, self.columna,
                                          self.valor), self.dataset_filtrado_expected)

    def test_getDataFromCsv(self):
        #self.maxDiff = 0
        self.assertEqual(csvdb.getDataFromCsv(core.default_path), self.dataset)

    def test_getHeader(self):
        self.assertEqual(csvdb.getHeader(core.default_path), self.header)

    def test_saveCSV(self):
        self.dataset.append(
            ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis"])
        csvdb.SaveCSV("test.csv", self.dataset,
                      csvdb.getHeader(core.default_path))
        self.assertEqual(self.dataset, csvdb.getDataFromCsv(self.testcsv))


if __name__ == '__main__':
    unittest.main()
