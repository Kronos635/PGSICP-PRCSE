#!/usr/bin/env python3
# coding: utf-8
#
# 20211217 - PGSICP-PRCSE - Grupo2
#
# 
#
alfa="abcdefghijklmnopqrstuvwxyz"
#def vigenereMatrix(pos, rep):
#    print(f'rep: {rep}; pos: {pos}')
#    if(rep == len(alfa)):
#        return alfa[pos]
#    if(pos % (len(alfa)-1) == 0 and pos != 0):
#        return alfa[pos] + vigenereMatrix(pos-len(alfa)+1, rep+1)
#    else:
#        return alfa[pos] + vigenereMatrix(pos+1, rep+1)

###############################################################################################################################################
# Função recursiva de preenchimento de um dicionário baseado no alfabeto começando na letra identificada na posição 'pos'
#
# Parâmetros
#   pos - posição da letra no alfabeto
#   rep - Número de ciclos da função com limite no len(alfabeto)
#   myDict - Dicionário a devolver
def vigenereDict(pos, rep, myDict):
    #print(f'rep: {rep}; pos: {pos}')
    if(rep == len(alfa)):                                       # Esta é a condição de saída, ou seja, já iteramos o número de letras
        myDict[alfa[pos]] = alfa[pos]
        return myDict
    if(pos % (len(alfa)-1) == 0 and pos != 0):                  # Se a posição for igual ao limite de len(alfa)-1 então faz roll-over
        myDict[alfa[pos]] = alfa[pos-len(alfa)]
        return vigenereDict(pos-len(alfa)+1, rep+1, myDict)
    else:                                                       # Just another round
        myDict[alfa[pos]] = alfa[pos]
        return vigenereDict(pos+1, rep+1, myDict)


def cifra (mensagem, chave, pos):
    if(pos == len(mensagems)):
        return dictAlfa[mensagem[pos][chave[pos]]]

dictAlfa={}    


# Preenchimento do dicionário de dicionários
for x in range(len(alfa)):                                      # Ciclo do dicionário exterior
    dictAux={}
    for y in range(len(alfa)):                                  # Ciclo dos dicionários interiores
    #dictAlfa = (vigenereMatrix(x,1))
        #dictAlfa[alfa[x]] = vigenereDict(x,1,dictAux)           # Chamada à função recursiva
        dictAlfa[alfa[x]] = vigenereDict(x,1,dictAux)

# Imprimir a matriz
for x in range(len(alfa)):
    print(dictAlfa[alfa[x]])
