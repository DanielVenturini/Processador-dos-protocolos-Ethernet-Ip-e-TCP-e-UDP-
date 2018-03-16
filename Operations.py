# -*- coding:UTF-8 -*-

import string
from Archive import Archive

class Operations:

    def __init__(self, fileName):
        self.archive = Archive()

        self.fileName = fileName
        self.file = self.archive.openFile(fileName, 'r')
        self.convFileToBin()

        file = self.archive.openFile(self.fileName + '.binario', 'r')
        self.str = file.readline()
        self.archive.close(file)

        self.getEthernet()
        self.getIP()

        if self.protocol == 'TCP':
            self.getTCP()
        else:
            self.getUDP()

    def convFileToBin(self):                                                # converter todo o arquivo para binario
        fileOutput = self.archive.openFile(self.fileName+'.binario', 'w')   # cria um novo arquivo para salvar os binarios

        self.line = self.file.read()                                        # guardando em self.line todo o arquivo

        for i in range(0, len(self.line)):                                  # iterando em cada byte do arquivo
            num = 0

            if self.line[i] == ' ' or self.line[i] == '\n':                 # quando for ' ' ou '\n' nao gravar
                continue

            if self.line[i] in string.ascii_lowercase:                      # se a dada posicao tiver um caracter de 'a' a 'f', entao recupera o respectivo valor em decimal
                num = 10 + string.ascii_lowercase.index(self.line[i])
            else:
                num = int(self.line[i])

            for bi in self.convToBinary(num):                               # convertendo os valores para binario
                fileOutput.write(str(bi))                                   # gravar os binarios no arquivo

        self.archive.close(fileOutput)                                      #fecha o arquivo
        self.archive.close(self.file)

    def whatsLetter(self, letter):                          # esta funcao converte uma letra 'a', 'b', ..., 'f' para um numero na base decimal
        num = string.ascii_lowercase.index(letter)

        if num == None:                                     # se a letra for maiuscula
            num = string.ascii_uppercase.index(letter)      #recupera a posicao dela na string de maiusculas

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
        for i in range(0, 4-num):   #se o numero em binario tiver menos que 4 bits, precisamos inserir os 0's na frente para completar os 4 bits
            binFinal.append(0)

        for i in range(0, num):     # como a lista esta invertida, vamos colocar na ordem correta
            binFinal.append(bin[num-i-1])

        return binFinal

    def convToDecimal(self, num):   #converte um numero binario em decimal
        mult = 2**(len(num)-1)
        result = 0

        for i in range(0, len(num)):
            if num[i] == '1':
                result += mult

            mult /= 2

        return int(result)

    def getIp(self):            # recupera os primeiros 32 bits no self.str para um endereço IP
        ipStr = ''
        for i in range(0, 4):   # iterando em cada octeto
            ipStr += (str(self.convToDecimal(self.str[i*8:(i+1)*8])) + '.')      # convertendo o octeto para decimal e concatenando

        self.str = self.str[32:]    # apagando da self.str os bits que já foram usados
        return ipStr[:-1]           # retorna a string inteira menos o ultimo ponto que foi concatenado

    def getNextByte(self, qtd):   # recupera os proximos 'qtd' bytes
        result = ''
        for i in range(0, qtd):
            result += self.str[i*8:(i+1)*8]

        self.str = self.str[qtd*8:]
        return result

    def getMac(self): # usando os proximos 6 bytes, será retornado o valor do MAC
        hex = [0,1,2,3,4,5,6,7,8,9,'a','b','c','d','e','f']
        result = ''

        for i in range(0, 12):
            bin = self.str[i*4:(i+1)*4]
            dec = self.convToDecimal(bin)
            result += str(hex[dec])

            if i % 2 != 0:
                result += ':'

        self.str = self.str[48:]
        return result[:-1]

    def getEthernet(self):
        print("***************  ETHERNET  *****************")
        #print("Preambulo: ", self.convToDecimal(self.getNextByte(8)))
        print("MAC1: ", self.getMac())
        print("MAC2: ", self.getMac())
        print("EtherType: ", self.convToDecimal(self.getNextByte(2)))
        print()

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

        self.protocol = self.convToDecimal(self.str[8:16])          # este campo determinara se o proximo sera o TCP ou o UDP
        if self.protocol == 6:
            self.protocol = 'TCP'
        elif self.protocol == 17:
            self.protocol = 'UDP'

        print("PROTOCOL: ", self.protocol)
        print("CHECKSUM: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("IP SOURCE: ", self.getIp())
        print("IP DESTINATION: ", self.getIp())
        print()

    def getTCP(self):
        print("***************  TCP  *****************")
        print("Source Port: ", self.convToDecimal(self.str[:16]))
        print("Destination Port: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("Sequence Number: ", self.convToDecimal(self.str[:32]))
        self.str = self.str[32:]
        print("Acknowledgement Number: ", self.convToDecimal(self.str[:32]))
        self.str = self.str[32:]
        print("Header Length: ", self.convToDecimal(self.str[:4]))
        print("Reserved: ", self.convToDecimal(self.str[4:10]))
        print("Bits: ", self.str[10:16])
        print("Window Size: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("Checksum: ", self.convToDecimal(self.str[0:16]))
        print("Urgent Pointer: ", self.convToDecimal(self.str[16:32]))

    def getUDP(self):
        print("***************  UDP  *****************")
        print("Source Port: ", self.convToDecimal(self.str[:16]))
        print("Destination Port: ", self.convToDecimal(self.str[16:32]))
        self.str = self.str[32:]
        print("Length: ", self.convToDecimal(self.str[:16]))
        print("Checksum: ", self.convToDecimal(self.str[16:32]))