# -*- coding:utf-8 -*-

'''
el parámetro delimiter=';' está seteado así porque la configuración internacional de windows
usa ';' por defecto como separador de columnas en un CSV. Tras unificar criterios ese caracter
se puede cambiar por ',' o el que nosotros elijamos.
'''

import csv

COLUMN_DELIMITER = ';'


def SaveCSV(path, dataset, header):
    with open(unicode(path), 'wb') as stream:
        writer = csv.writer(stream, delimiter=COLUMN_DELIMITER)
        writer.writerow(header)
        for row in range(len(dataset)):
            rowdata = []
            for column in range(len(dataset[0])):
                item = dataset[row][column]
                if item is not None:
                    rowdata.append(unicode(item).encode('utf8'))
                else:
                    rowdata.append('')
            writer.writerow(rowdata)


def getDataFromCsv(path):
    dataSet = []
    with open(unicode(path), 'r') as stream:
        reader = csv.reader(stream, delimiter=COLUMN_DELIMITER)
        reader.next()
        for rowdata in reader:
            if any(x.strip() for x in rowdata):
                dataSet.append(rowdata)
    return dataSet


def dataFilter(dataset, columna, valor):
    filteredDataSet = []
    for rowdata in dataset:
        if rowdata[columna] == valor:
            filteredDataSet.append(rowdata)
    return filteredDataSet


def distinct(dataset, columna):
    filteredDataSet = []
    for rowdata in dataset:
        if rowdata[columna] not in [fila[columna] for fila in filteredDataSet]:
            filteredDataSet.append(rowdata)
    return filteredDataSet


def getColumn(dataset, columna):
    return [fila[columna] for fila in dataset]


def getHeader(path):
    with open(unicode(path), 'rb') as stream:
        reader = csv.reader(stream, delimiter=COLUMN_DELIMITER)
        header = reader.next()
        return header


def sortDataSet(dataset, column, invertido=False):
    sortedDataSet = sorted(dataset, key=lambda col: col[column], reverse=invertido)
    return sortedDataSet
