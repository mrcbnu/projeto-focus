from time import sleep
from lib.arquivos.relatorios import *
from lib.arquivos.relatorio.comprovante import *
from lib.arquivos.ordemcarga import *
from lib.interface.layout import *
from lib.interface.valida import *
from lib.interface.vinheta import *
from lib.arquivos.relatorio.fusion import *
import pandas as pd
import os


def main():
    os.system('cls')
    abertura()
    hoje = date.today().strftime('%d/%m/%Y')
    hoje1 = date.today().strftime('%d-%m-%y')
    '''
    Localiza os arquivos necessarios
    se não encontrado será criado um novo 
    '''
    cabecalho('-', 'verificando arquivos...')
    arq = ['lib/arquivos/database/oc_semana1.txt']
    arq_1 = 'lib/arquivos/database/oc_semana1.txt'
    origem = 'lib/arquivos/database/origem.txt'
    temp = 'prog-1.jpg'

    for chave, valor in enumerate(arq):
        if arqExiste(valor):
            print(f'Arquivo {cor(13)}{valor}{cor(0)} encontrado com sucesso')
            sleep(0.2)
        else:
            print(f'Arquivo {cor(3)}{valor} {cor(0)} não encontrado...')
            sleep(0.2)
            criarArquivo(valor)
            sleep(0.2)
    if arqExiste(temp):
        os.remove(temp)

            #######    MENU PRINCIPAL    #########
    while True:
        os.system('cls')
        op = menu(['ORDENS DE CARGA', 'PROGRAMAÇÃO', 'COMPROVANTE', 'PLACAS PICKING', 'SAIR'], 'MENU PRINCIPAL')
        if op == 1: # ORDENS DE CARGA
            while True:
                os.system('cls')
                op1 = menu(['OC HOJE', 'OC PERIODO', 'INCLUIR', 'IMPORTAR', 'GERAR', 'VOLTAR'],
                           'ORDENS DE CARGA')
                if op1 == 1:
                    oc_hoje(arq_1, hoje)
                    input('pressione ENTER para continuar...')
                elif op1 == 2:
                    ini = leiaData('Data inicial dd/mm/aaaa: ')
                    fim = leiaData('Data final dd/mm/aaaa: ')
                    oc_periodo(arq_1, ini, fim)
                    input('pressione ENTER para continuar...')
                elif op1 == 3:
                    incluiOC(arq_1)
                    input('pressione ENTER para continuar...')
                elif op1 == 4:
                    if arqExiste(origem):
                        importaOC(origem, arq_1)
                        os.remove(origem)
                        input('pressione ENTER para continuar...')
                    else:
                        print(f'Arquivo {origem} não encontrado!')
                        input('pressione ENTER para continuar...')
                elif op1 == 5:
                    geraOCnovo(arq_1)
                    input('pressione ENTER para continuar...')
                else:
                    break
        elif op == 2: # PROGRAMAÇÃO
            while True:
                os.system('cls')
                opc = menu(['HOJE', 'FORA DA ROTA', 'FUSION', 'MENU PRINCIPAL'], 'PROGRAMAÇÃO')
                arq_dt = f'lib/arquivos/relatorio/programacao/prog {hoje1}.txt'
                arq_img = f'lib/arquivos/relatorio/programacao/prog {hoje1}.jpg'
                if opc == 1:
                    progDia(arq_dt, arq_1, hoje)
                    if not arqExiste(arq_img):
                        divulga(arq_dt, hoje1)
                    input('pressione ENTER para continuar...')

                elif opc == 2:
                    dtfora = leiaData('Digite a data do roteiro que deseja programar [dd/mm/aaa]: ')
                    dtfora1 = dtfora.strftime('%d-%m-%y')
                    dtfora = dtfora.strftime('%d/%m/%Y')
                    print(dtfora)
                    arq_dt = f'lib/arquivos/relatorio/programacao/prog {dtfora1}.txt'
                    arq_img = f'lib/arquivos/relatorio/programacao/prog {dtfora1}.jpg'
                    progDia(arq_dt, arq_1, dtfora)
                    if not arqExiste(arq_img):
                        divulga(arq_dt, dtfora1)
                    input('pressione ENTER para continuar...')

                elif opc == 3:
                    try:
                        dados = pd.read_csv(
                            r"E:\Meus Documentos\Downloads\Relatório de Motorista e Ajudantes Escalados.csv")

                    except:
                        print(
                            'ERRO: Arquivo de dados não encontrado!, favor fazer download do arquivo de dados no FUSION DMS')

                    else:
                        print('DataFrame criado com sucesso')
                        cabecalho('-', 'GERANDO CONTROLE DE QUILOMETRAGEM')
                        cont = controle(dados)
                        imprime(cont, 1)

                        cabecalho('-', 'GERANDO VISTORIA')
                        vist = vistoria(dados)
                        imprime(vist, 1)

                        cabecalho('-', 'GERANDO ESCALAÇÃO')
                        escalacao(dados)

                    input('pressione ENTER para continuar...')
                elif opc == 4:
                    break
                else:
                    print(f'{cor(3)}OPÇÃO INVÁLIDA... TENTE NOVAMENTE!{cor(0)}')
                    
        elif op == 3: # COMPROVANTE
            comprovante()            
            input('pressione ENTER para continuar....')

        elif op == 4: # PLACAS ROTEIRO
            while True:
                op4 = menu(['PLACAS DE HOJE', 'PLACAS FORA DE ROTA', 'MENU PRINCIPAL'], 'IMPRESSÃO DE PLACAS DO PICKING')
                if op4 == 1:
                    geraPlacasPicking(arq_1, hoje)
                if op4 == 2:
                    dtfora = leiaData('Digite a data do roteiro que deseja imprimir [dd/mm/aaa]: ')
                    dtfora = dtfora.strftime('%d/%m/%Y')
                    geraPlacasPicking(arq_1, dtfora)
                if op4 == 3:
                    break
        elif op == 5: # ENCERRA
            break
        else:
            print(f'{cor(3)}OPÇÃO INVÁLIDA... TENTE NOVAMENTE!{cor(0)}')
    encerra()

if __name__ == '__main__':
    main()
