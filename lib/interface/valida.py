from typing import List, Union

from lib.interface.cores import *
from datetime import *


def leiaInt(msg):
    '''
    -> Função que valida a entrada de um numero inteiro
    :param msg: indicação ao usuario informando a entrada do valor a ser validado
    :return: retorna o valor correto
    '''
    while True:
        try:
            num = int(input(msg))
        except (TypeError, ValueError):
            print(f'{cor(3)}não é um numero inteiro valido!{cor(0)}')
            continue
        except KeyboardInterrupt:
            print(f'{cor(5)}O usuário preferiu não informar o valor {cor(0)}')
            return 0
        else:
            return num


def leiaFloat(msg):
    '''
    -> Função que valida a entrada de um numero real
    :param msg: indicação ao usuario informando a entrada do valor a ser validado
    :return: retorna o valor correto
    '''
    while True:
        try:
            num = float(input(msg))
        except (TypeError, ValueError):
            print(f'{cor(3)}não é um numero real valido!{cor(0)}')
            continue
        else:
            return num


def leiaData(msg) -> object:
    data = ''
    while True:
        try:
            data = str(input(msg))
            data = datetime.strptime(data, '%d/%m/%Y')
        except:
            print(f'{cor(3)}Data errada{cor(0)}')
        else:
            break
    return data


def leiaCol(msg):
    '''
    -> função que valida o codigo de colaborador a ser escalado na ordem de carga
    :param msg: mensagem apontando motorista e ou ajudante
    :return: retorna nome do coladorador
    '''
    colaboradores = ['ANTONIO','CLAUDIO','ADILSON','JAIR','KLEITON','SIDNEY','BOMBASAR',
                    'PEDRO','RICARDO','JHONATAN','TIAGO A','THIAGO G',
                    'RODRIGO','AGNALDO','PATRIC','DADO', 'ALVES', 'A DEFINIR']

    while True:
        cod = leiaInt(msg)

        if cod > len(colaboradores):
            print('Codigo inexistente... digite novamente!')
        else:
            if cod == 0:
                col = '-'
            else:
                col = colaboradores[cod - 1]
            break
    print(f'{cor(7)}{col}{cor(0)}')
    return col


def leiaCar(msg):
  
    carros = [{'COD': 13, 'APELIDO': 'ATE', 'PLACA': 'MLV-2343', 'MODELO': 'MB ATEGO'},
              {'COD': 16, 'APELIDO': 'KAN', 'PLACA': 'MMJ-2652', 'MODELO': 'KANGOO'},
              {'COD': 18, 'APELIDO': 'MFU', 'PLACA': 'MFU-2698', 'MODELO': 'VW DELIVERY'},
              {'COD': 22, 'APELIDO': 'QIB', 'PLACA': 'QIB-3742', 'MODELO': 'VW DELIVERY'},
              {'COD': 23, 'APELIDO': 'QIC', 'PLACA': 'QIC-3812', 'MODELO': 'VW DELIVERY'},
              {'COD': 35, 'APELIDO': 'QIS', 'PLACA': 'QIS-1156', 'MODELO': 'FORD CARGO'},
              {'COD': 38, 'APELIDO': 'QIF', 'PLACA': 'QIF-9367', 'MODELO': 'MB SPRINTER'},
              {'COD': 43, 'APELIDO': 'QJI', 'PLACA': 'QJI-0188', 'MODELO': 'MB SPRINTER'},
              {'COD': 71, 'APELIDO': 'RKW', 'PLACA': 'RKW8D23', 'MODELO': 'WW DELIVERY'},
              {'COD': 80, 'APELIDO': 'B45', 'PLACA': 'RXY0B45', 'MODELO': 'MB SPRINTER'},
              {'COD': 81, 'APELIDO': 'B75', 'PLACA': 'RXY0B75', 'MODELO': 'MB SPRINTER'},
              {'COD': 99, 'APELIDO': 'QJB', 'PLACA': 'QJB-4938', 'MODELO': 'FORD CARGO'}
              ]

    encontrado = False
    carroL = []

    while not encontrado:
        inex = 0
        val = leiaInt(msg)
        for item in carros:
            if val == item['COD']:
                print(f'{cor(7)}{item["APELIDO"]}{cor(0)}')
                carro = item['APELIDO']
                carroL.append(item['COD'])
                carroL.append(item['APELIDO'])
                carroL.append(item['PLACA'])
                carroL.append(item['MODELO'])
                encontrado = True
            else:
                inex += 1
                if inex == len(carros):
                    print(f'{cor(3)}Codigo inexistente... Tente novamente!{cor(0)}')
    return carroL


def diaSemana(data):
    dias = ['SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO']
    dia = data.weekday()
    sem = dias[dia]
    return sem

