# -*- coding:UTF-8 -*-

import string
from Archive import Archive

class Operations:

    def __init__(self, fileName):
        self.archive = Archive()

        self.fileName = fileName
        self.file = self.archive.openFile(fileName, 'r')
        self.convFileToBin()

    def printArchive(self):
        for line in self.file.readlines():
            for octeto in line.split():
                print(octeto, end=" ")

            print()

    def convFileToBin(self):                                                # converter todo o arquivo para binario
        fileOutput = self.archive.openFile(self.fileName+'.binario', 'w')   # cria um novo arquivo para salvar os binarios

        for line in self.file.readlines():                                  # lendo cada linha do arquivo

            for octeto in line.split():                                     # lendo cada octeto da linha
                fileOutput.write(' ')                                       # escrevendo um espaco entre cada octeto

                for i in range(0, len(str(octeto))):                        #iterando em cada byte do octeto

                    if octeto[i] in string.ascii_lowercase or octeto[i] in string.ascii_uppercase:  # se o octeto tiver uma letra
                        list = self.convToBinary(self.whatsLetter(octeto[i]))   # converte a letra pra decimal e depois para binario
                    else:
                        list = self.convToBinary(int(octeto[i]))                # converte o numero nesta posicao do octeto

                    for k in range(0, len(list)):                           # como é retornado o numero em uma lista, percorremos esta lista
                        fileOutput.write(str(list[k]))                      # escreve cada 0 ou 1 no arquivo de saida

        self.archive.close(fileOutput)                                      #fecha o arquivo

    def whatsLetter(self, letter):              # esta funcao converte uma letra 'a', 'b', ..., 'f' para um numero na base decimal
        num = string.ascii_lowercase.index(letter)

        if num == None:                         # se a letra for maiuscula
            num = string.ascii_uppercase.index(letter)  #recupera a posicao dela na string de maiusculas

        return 10+num   # retorna 10 + sua posicao, ou seja, seu valor em hexadecimal

    def convToBinary(self, num):      # esta funcao converte um numero decimal para binario e devolve em uma lista: 9 = [1,0,0,1]

        if num == 0:
            return [0,0,0,0]

        bin = []
        while num > 1:
            num /= 2
            if num == int(num):
                bin.append(0)
            else:
                num -= 0.5
                bin.append(1)

        if num == 1:
            bin.append(1)

        binFinal = []
        num = len(bin)
        for i in range(0, 4-num):   #se o numero em binario tiver menos que 4 bits, precisamos completar com os 0's na frente para completar os 4 bits
            binFinal.append(0)

        for i in range(0, num):     # como a lista esta invertida, vamos colocar na ordem correta
            binFinal.append(bin[num-i-1])

        return binFinal