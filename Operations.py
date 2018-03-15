# -*- coding:UTF-8 -*-

import string
from Archive import Archive

class Operations:

    def __init__(self, fileName):
        self.archive = Archive()

        self.fileName = fileName
        self.file = self.archive.openFile(fileName, 'r')
        self.convFileToBin()
        self.getEthernet()
        self.getIP()

    def printArchive(self):
        for line in self.file.readlines():
            for octeto in line.split():
                print(octeto, end=" ")

            print()

    def convFileToBin(self):                                                # converter todo o arquivo para binario
        fileOutput = self.archive.openFile(self.fileName+'.binario', 'w')   # cria um novo arquivo para salvar os binarios

        for line in self.file.readlines():                                  # lendo cada linha do arquivo

            for octeto in line.split():                                     # lendo cada octeto da linha
                #fileOutput.write(' ')                                       # escrevendo um espaco entre cada octeto

                for i in range(0, len(str(octeto))):                        #iterando em cada byte do octeto

                    if octeto[i] in string.ascii_lowercase or octeto[i] in string.ascii_uppercase:  # se o octeto tiver uma letra
                        list = self.convToBinary(self.whatsLetter(octeto[i]))   # converte a letra pra decimal e depois para binario
                    else:
                        list = self.convToBinary(int(octeto[i]))                # converte o numero nesta posicao do octeto

                    for k in range(0, len(list)):                           # como é retornado o numero em uma lista, percorremos esta lista
                        fileOutput.write(str(list[k]))                      # escreve cada 0 ou 1 no arquivo de saida

            #fileOutput.write('\n')                                          # quebrando uma linha

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

    def convToDecimal(self, num):
        mult = 1
        result = 0

        for i in range(0, len(num)):
            if num[i] == '1':
                result += mult
                mult *= 2

        return result

    def getIp(self, num):           # dado um numero em binario, sera convertido para o respectivo IP
        ipStr = ''
        for i in range(0, 4):
            ipStr += (str(self.convToDecimal(num[i*8:((i+1)*8)-1])) + '.')      # convertendo o octeto para decimal e concatenando

        return ipStr[:-1]           # retorna a string inteira menos o ultimo ponto que foi concatenado

    def getEthernet(self):
        file = self.archive.openFile(self.fileName + '.binario', 'r')
        self.str = file.readline()
        self.archive.close(file)

        print("***************  ETHERNET  *****************")
        print("Version: ", self.convToDecimal(self.str[:4]))
        print("IHL: ", self.convToDecimal(self.str[4:8]))
        print("TOS: ", self.convToDecimal(self.str[8:16]))
        print("TOTAL LENGTH: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]                                    # terminei de imprimir a primeira linha, entao quebro ela para comecar a contagem do 0
        print("IDENTIFICATION: ", self.convToDecimal(self.str[:16]))
        print("FLAGS: ", self.str[16:19])
        print("FRAGMENT OFFSET: ", self.convToDecimal(self.str[19:32]))
        self.str = self.str[32:]
        print("TTL: ", self.convToDecimal(self.str[:8]))
        print("GRE: ", self.convToDecimal(self.str[8:16]))
        print("CHECKSUM: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("IP SOURCE: ", self.getIp(self.str[:32]))
        self.str = self.str[32:]
        print("IP DESTINATION: ", self.getIp(self.str[:32]))
        self.str = self.str[32:]

    def getIP(self):

        print("***************  IP  *****************")
        print("Version: ", self.convToDecimal(self.str[:4]))
        print("IHL: ", self.convToDecimal(self.str[4:8]))
        print("TOS: ", self.convToDecimal(self.str[8:16]))
        print("TOTAL LENGTH: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("IDENTIFICATION: ", self.convToDecimal(self.str[:16]))
        print("FLAGS: ", self.str[17:19])
        print("FRAGMENT OFFSET: ", self.convToDecimal(self.str[19:32]))
        self.str = self.str[32:]
        print("TTL: ", self.convToDecimal(self.str[:8]))
        print("PROTOCOL: ", self.convToDecimal(self.str[8:16]))
        self.protocol = self.convToDecimal(self.str[8:16])          # este campo determinara se o proximo sera o TCP ou o UDP

        print("CHECKSUM: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("IP SOURCE: ", self.getIp(self.str[:32]))
        self.str = self.str[32:]
        print("IP DESTINATION: ", self.getIp(self.str[:32]))
        self.str = self.str[32:]