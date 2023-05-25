from lib.arquivos.relatorios import *
from lib.interface.valida import *
from time import sleep
from datetime import timedelta


def arqExiste(arquivo):
    '''
    => Verifica se o existencia do arquivo a ser manipulado
    :param arquivo: nome do arquivo
    :return: retorna False se o arquivo não for encontrado
             retorna True se o arquivo for encontrado
    '''
    try:
        a = open(arquivo, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criarArquivo(arquivo):
    '''
    => Cria um arquivo de texto
    :param arquivo: nome do arquivo
    :return:
    '''
    try:
        a = open(arquivo, 'wt+')
        a.close()
    except:
        print(f'{cor(3)}Houve um Erro na criação do arquivo!{cor(0)}')
    else:
        print(f'Arquivo {cor(9)}{arquivo} {cor(0)}criado com sucesso!')


def importaOC(arq_ori, arq_des):
    cabecalho('-', 'IMPORTAÇÃO DE ORDENS DE CARGA SEMANAL')
    try:
        ori = open(arq_ori, 'r')
    except:
        print(f'{cor(3)}Ops! problemas em abrir arquivo de origem{cor(0)}')
    else:
        print(f'Arquivo {cor(7)}{arq_ori} {cor(0)}localizado com sucesso! ')
        try:
            des = open(arq_des, 'r')
        except:
            print(f'{cor(3)}Ops! problemas em abrir arquivo de destino{cor(0)}')
        else:
            print(f'Arquivo{cor(7)} {arq_des} {cor(0)}localizado com sucesso!')
            cont = 0
            for novo in ori:
                oc_ori = novo.split(';')
                duplicado = False
                with open(arq_des, 'r') as des:
                    for antigo in des:
                        oc_ant = antigo.split(';')
                        if oc_ori[0] == oc_ant[0]:
                            print(f'{cor(3)}OC {oc_ori[0]} já existe....{cor(0)}')
                            sleep(0.1)
                            duplicado = True

                if not duplicado:
                    with open(arq_des, 'at') as des:
                        try:
                            des.write(f'{oc_ori[0]};{oc_ori[1]};{oc_ori[2]};{oc_ori[3]}')
                        except:
                            print(f'{cor(3)}Ops! problemas em gravar novo registro{cor(0)}')
                        else:
                            print(f'{cor(5)}Gravando registro....{cor(0)}')
                            #sleep(0.25)
                            print(f'{cor(7)}{oc_ori[0]} registrado com sucesso!{cor(0)}')
                            cont += 1
    try:
        ori.close()
    except:
        print(f'{cor(9)}Foram registrados {cont} Ordens de Carga{cor(0)}')
    finally:
        print(f'{cor(9)}Foram registrados {cont} Ordens de Carga{cor(0)}')
    des.close()


def incluiOC(arquivo):
    cabecalho('-', 'INCLUSÃO DE ORDEM DE CARGA')

    while True:
        with open(arquivo, 'r') as arq:
            for reg in arq:
                ultimo_reg = reg.split(';')
                ultimo_oc = ultimo_reg[0]
        arq = open(arquivo, 'at')
        oc = int(ultimo_oc) + 1
        print(f'OC......: {oc}')
        roteiro = str(input('ROTEIRO.: ')).upper()
        data = leiaData('DATA....: ')
        data = datetime.strftime(data, '%d/%m/%Y')
        transp = leiaInt('TRANSPORTADORA: ')
        while True:
            resp = str(input('CONFIRMA [S/N]: ')).upper()
            if resp == 'S' or resp =='N':
                break
            else:
                print(f'{cor(3)}Opçãp inválida{cor(0)}')
        if resp == 'S':
            try:
                arq.write(f'{oc};{roteiro};{data};{transp}\n')
            except:
                print(f'Ops! problemas em gravar dados')
            else:
                print(f'{cor(7)}OC {oc} {cor(1)}cadastrado com sucesso!{cor(0)}')
            linha('-', 40, 1)
        while True:
            resp = str(input('DESEJA CONTINUAR [S/N]: ')).upper()
            if resp == 'S' or resp =='N':
                break
            else:
                print(f'{cor(3)}Opçãp inválida{cor(0)}')
        linha('-', 40, 1)
        if resp == 'N':
            break
    arq.close()


def progDia(arq_hj, arq_geral, data='hoje'):
    cabecalho('-', 'PROGRAMAÇÃO DE HOJE')
    if not arqExiste(arq_hj):
        print(f'arquivo {arq_hj} não existe . . . criando arquivo!')
        sleep(0.5)
        criarArquivo(arq_hj)

        with open(arq_geral, 'r') as ori:
            for reg in ori:
                dados = reg.split(';')
                dados[3] = dados[3].replace('\n', '')
                if dados[2] == data and dados[3] == '493':
                    print(f'{cor(1)}{dados[0]} - {dados[1]}{cor(0)} ')
                    carro = leiaCar('Codigo do veiculo: ')
                    motorista = leiaCol('Codigo do motorista: ')
                    ajudante = leiaCol('Codigo do ajudante: ')
                    linha('-', 25)
                    des = open(arq_hj, 'at')
                    des.write(f'{dados[0]};{dados[1]};{carro};{motorista};{ajudante}\n')
                    des.close()
    else:
        print('Programação já feita...')
    linha('-', 42)


def geraOC(arq):
    '''

    :param arq:
    :return:
    '''

    matriz = (
            'REUNIDAS','BAUER', 'BALNEARIO CAMBORIU', 'ITAJAI', 'TIJUCAS', 'TUBARAO', 'FPOLIS CENTRO',
            'SAO JOSE', 'BLUMENAU', 'REUNIDAS', 'BAUER', 'BALNEARIO  BRUSQUE','ARARANGUA', 'SAO JOSE',
            'FPOLIS CENTRO', 'JOINVILLE', 'BLUMENAU', 'REUNIDAS', 'BAUER', 'JARAGUA DO SUL', 'SAO JOSE',
            'FPOLIS NORTE', 'PORTO BELO', 'BLUMENAU', 'REUNIDAS', 'BAUER', 'BALNEARIO CAMBORIU', 'ITAJAI',
            'FPOLIS CENTRO', 'FPOLIS SUL', 'RIO DO SUL', 'SAO FRANCISCO', 'JOINVILLE', 'REUNIDAS', 'BAUER',
            'MAFRA', 'BRUSQUE/GASPAR', 'BLUMENAU', 'CHAPECO', 'LAGES'
            )
    # PEGAR O ULTIMO REGISTRO DO ARQUIVO DE DADOS E USAR COMO PARAMETRO INICIAL
    with open(arq, 'r') as origem:
        for reg in origem:
            ultimo = reg.split(';')
            oc = ultimo[0]
            data = datetime.strptime(ultimo[2], '%d/%m/%Y')
            data = data + timedelta(days=2)
    # VALIDAR DATAS E ROTAS

        for item, valor in enumerate(matriz):
            oc = int(oc) + 1
            if valor == 'REUNIDAS':
                data = data + timedelta(days=1)
                semana = diaSemana(data)
                data1 = datetime.strftime(data, '%d/%m/%Y')
                transp = '5219'
                linha('-', )
                print(f'{cor(13)}{data1} - {semana}{cor(0)}')
            elif valor == 'BAUER':
                transp = '121067'
            elif ('BALNEARIO' in valor) or ('ITAJAI' in valor) or ('JARAGUA' in valor):
                transp = '5834'
            else:
                transp = '493'

            origem = open(arq, 'at')
            if valor != 'LAGES':
                try:
                    origem.write(f'{oc};{valor};{data1};{transp}\n')
                except:
                    print(f'Ops! problemas em gravar dados')
                else:
                    print(f'{cor (7)}OC {oc} - {valor} {cor (1)}cadastrado com sucesso!{cor (0)}')
            else:
                while True:
                    resp = str(input('DESEJA INCLUIR LAGES NO ROTEIRO [S/N]: ')).upper()
                    if resp == 'S' or resp == 'N':
                        break
                    else:
                        print(f'{cor (3)}Opçãp inválida{cor (0)}')
                linha('-', 80, 1)
                if resp == 'S':
                    try:
                        origem.write (f'{oc};{valor};{data1};{transp}\n')
                    except:
                        print (f'Ops! problemas em gravar dados')
                    else:
                        print (f'{cor (7)}OC {oc} - {valor} {cor (1)}cadastrado com sucesso!{cor (0)}')
                    break

