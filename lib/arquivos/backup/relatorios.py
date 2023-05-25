from lib.arquivos.ordemcarga import *
from lib.interface.layout import *
from lib.interface.cores import *
from time import sleep
from datetime import *

def oc_hoje(arquivo, data='hoje'):
    '''
    =>Exibe os roteiros de uma data especefica.
    :param arquivo: arquivo onde estão listados as OCs e seus respectivos Roteiros
    :param data: data especificada pelo usuario, se não informado assume a data corrente.
    '''
    try:
        a = open(arquivo, 'r')
    except:
        print(f'{cor(3)}Erro ao ler arquivo {arquivo}!{cor(0)}')
    else:
        cabecalho('-', 'ROTEIRO DE HOJE')
        print(data)
        print('+','-' * 9,'+', '-' * 44, '+')
        print('| {}|{} |'.format('OC'.center(10), 'ROTEIRO'.center(45)))
        print('+','-' * 9,'+', '-' * 44, '+')
        for v in a:
            dado = v.split(';')
            dado[2] = dado[2].replace('\n', '')
            if dado[2] == data:
                print(f'| {dado[0]:^10}| {dado[1]:<45}|')
        print('+','-' * 9,'+', '-' * 44, '+')
    finally:
        a.close()


def oc_periodo(arquivo, ini, fim):
    '''
    => Exibe os roteiros do periodo informado
    :param arquivo: arquivo onde estão listados as OCs e seus respectivos Roteiros.
    :param ini: data inicial
    :param fim: data final
    '''
    try:
        a = open(arquivo, 'r')
    except:
        print(f'{cor(3)} Erro ao ler o arquivo {arquivo}!{cor(0)}')
    else:
        cabecalho('-', 'ROTEIROS DO PERIODO:')
        print(datetime.strftime(ini, '%d/%m/%Y'),' a ',datetime.strftime(fim, '%d/%m/%Y'))
        print('+','-' * 9,'+', '-' * 29, '+', '-' * 12, '+')
        print('| {}|{} |{}|'.format('OC'.center(10), 'ROTEIRO'.center(30), 'DATA'.center(14)))
        for v in a:
            dado = v.split(';')
            dado[2] = dado[2].replace('\n', '')
            dado[2] = datetime.strptime(dado[2], '%d/%m/%Y')
            if ini <= dado[2] <= fim:
                dado[2] = datetime.strftime(dado[2], '%d/%m/%Y')
                if dado[1] == 'REUNIDAS':
                    print('+', '-' * 9, '+', '-' * 29, '+', '-' * 12, '+')
                print(f'| {dado[0]:^10}| {dado[1]:<30}| {dado[2]:^13}|')
        print('+','-' * 9,'+', '-' * 29, '+', '-' * 12, '+')
    print('AgroLog v1.0')



def divulga(arq_data):
    try:
        arq = open(arq_data, 'r')
    except:
        print(f'{cor(3)}Ops! erro ao acessar o arquivo...{cor(0)}')
    else:
        print(f'{cor(5)}Analizando os dados.', end='')
        sleep(0.25)
        print(' .', end=''); sleep(0.25); print(' .', end=''); sleep(0.25)
        print(' .', end=''); sleep(0.25); print(f' tudo certo! ', end=''); sleep(0.25)
        print(f'{cor(1)}Gerando relatório {cor(0)}\n')
        sleep(0.50)
        print('+', '-' * 56,'+')
        print('|{}{:^58}{}|'.format(cor(13),'ESCALAÇÃO DOS CARROS E COLABORADORES', cor(0)))
        print('+','-' * 18,'+', '-' * 8, '+', '-' * 24, '+')
        print('|{}|{}|{}|'
              .format('ROTA'.center(20),'CARRO'.center(10),'COLABORADORES'.center(26)))
        print('+','-' * 18,'+', '-' * 8, '+', '-' * 24, '+')
        for v in arq:
            dados = v.split(';')
            dados[4] = dados[4].replace('\n', '')
            print(f'| {dados[1]:<19}| {dados[2]:^9}| {dados[3]:<12}{dados[4]:>12} |')
        print('+','-' * 18,'+', '-' * 8, '+', '-' * 24, '+', '\n')

