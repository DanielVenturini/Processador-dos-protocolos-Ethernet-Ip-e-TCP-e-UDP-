# -*- coding:UTF-8 -*-

class Archive:

    def openFile(self, fileName, opc):
        try:
            file = open(fileName, opc, encoding='UTF-8')
        except FileNotFoundError:
            print("Arquivo %s não existe!" % file)
            return None
        else:
            return file

    def close(self, file):
        file.close()