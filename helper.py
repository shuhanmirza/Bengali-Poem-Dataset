import csv
import re

def writeDataToCsv(data, filePath):
    fieldList = list(data[0].keys())

    with open(filePath, "w", encoding='utf-8') as csvfile:
        dictWriter = csv.DictWriter(csvfile, fieldList)
        dictWriter.writeheader()
        dictWriter.writerows(data)


def readDataFromCsv(filePath):
    data = []

    with open(filePath, encoding="utf-8") as csvfile:
        dictReader = csv.DictReader(csvfile)
        for row in dictReader:
            data.append(row)

    return data


def getStringFromFile(path):
    s = open(path, encoding="utf-8")
    msg = ''
    flg = 0

    for m in s:
        if flg == 0:
            msg = msg + m.strip()
            flg = 1
        else:
            msg = msg + "\n" + m.strip()

    return msg


def writeFile(string, path):
    file = open(path, 'w', encoding='utf-8')
    file.write(string)
    file.close


def appendFile(string, path):
    file = open(path, 'a+')
    file.write(string)
    file.close


def stringCleaner(name):
    name = name.strip()
    name = name.lower()

    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")

    restricted_chars = ['_', '.', '-', '"', "'", '–', ':']

    for element in restricted_chars:
        if name.find(element) == len(name) - 1:
            name = name[:-1]

        if name.find(element) == 0:
            name = name[-1:]

    for element in restricted_chars:
        if name.find(element) == len(name) - 1:
            name = name[:-1]

        if name.find(element) == 0:
            name = name[-1:]

    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")
    name = name.replace("  ", " ")

    return name


def sentenceCount(text):
    textList = text.split("\n")

    count = 0
    for i in textList:
        if i:
            count += 1
    return count


def removeHtmlTags(text):
    text = text.replace('<br>', '\n')
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def countWords(text):
    words = text.split()

    return len(words)
