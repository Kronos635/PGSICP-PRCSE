#!/usr/bin/env python3
import re 

def validarPassword(password):
    while True:   
        if (len(password)<8 or len(password)>16): 
            return("A sua password deve ter entre 8 e 16 elementos de comprimento.")
        elif not re.search("[a-z]", password): 
            return("A sua password deve conter minúsculas do alfabeto de a até z.")
        elif not re.search("[A-Z]", password): 
            return("A sua password deve conter maúsculas do alfabeto de A até Z.")
        elif not re.search("[0-9]", password): 
            return("A sua password deve conter algarismos do intervalo de 0 a 9.")
        elif not re.search("[^A-Za-z0-9]", password): 
            return("A sua password deve conter carateres especiais.")
        elif re.search("\s", password): 
            return("A sua password tem espaços em branco, remova-os por favor.")
        else: 
            return "OK"
