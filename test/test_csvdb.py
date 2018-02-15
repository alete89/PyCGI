import os
import unittest
import src.logic.csvdb as csvdb


class TestCore(unittest.TestCase):
    def setUp(self):
        self.path = os.getcwd() + "/test/tabla_test.csv"
        self.testcsv = "test.csv"
        self.test_dataset = [
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

    def tearDown(self):
        try:
            os.remove(self.testcsv)
        except OSError:
            pass

    def test_dataFilter(self):
        columna = 1
        valor = "archivo"
        dataset_filtrado_expected = [
            ['1', 'archivo', 'abrir', '2', '1', 'python ./scripts/abrir.py', '1'],
            ['4', 'archivo', 'guardar como', '1', '1',
                'python ./scripts/guardar.py', '1']
        ]
        self.assertEqual(csvdb.dataFilter(self.test_dataset, columna,
                                          valor), dataset_filtrado_expected)

    def test_getDataFromCsv(self):
        #self.maxDiff = 0
        self.assertEqual(csvdb.getDataFromCsv(
            self.path), self.test_dataset)

    def test_getHeader(self):
        header_expected = ["id", "menu", "submenu", "posicion en menu",
                           "orden en secuencia", "comando", "loop"]
        self.assertEqual(csvdb.getHeader(self.path), header_expected)

    def test_saveCSV(self):
        self.test_dataset.append(
            ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis"])
        csvdb.SaveCSV("test.csv", self.test_dataset,
                      csvdb.getHeader(self.path))
        self.assertEqual(self.test_dataset, csvdb.getDataFromCsv(self.testcsv))

    def test_distinct(self):
        columna = 1
        distinct_expected = [
            ['1', 'archivo', 'abrir', '2', '1', 'python ./scripts/abrir.py', '1'],
            ['2', 'edicion', 'copiar', '2', '1',
                'python ./scripts/copiar.py', '5'],
            ['3', 'ver', 'ping', '1', '2', 'ping (ingrese una IP)', '2'],
            ['7', 'Dibujo', 'Paint', '1', '1', 'mspaint', '2'],
            ['8', 'prueba', 'numeros', '1', '2', 'python ./scripts/uno.py', '1']
        ]
        self.assertEqual(csvdb.distinct(
            self.test_dataset, columna), distinct_expected)


if __name__ == '__main__':
    unittest.main()
