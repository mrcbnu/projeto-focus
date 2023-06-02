from lib.arquivos import relatorios
#from lib.arquivos.relatorios import *
from lib.interface.valida import *
from lib.interface.layout import *
from time import sleep
from datetime import timedelta, date
import os


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
            data_ini = data_fim = ''
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
                            if cont == 1:
                                data_ini = datetime.strptime(oc_ori[2], '%d/%m/%Y')

                            else:
                                data_fim = datetime.strptime(oc_ori[2], '%d/%m/%Y')

            relatorios.geraListagemRoteiro(arq_des, data_ini, data_fim)
            relatorios.oc_periodo(arq_des, data_ini, data_fim)
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
                    while True:
                        print(f'{cor(1)}{dados[0]} - {dados[1]}{cor(0)} ')
                        carro = leiaCar('Codigo do veiculo: ')
                        motorista = leiaCol('Codigo do motorista: ')
                        ajudante = leiaCol('Codigo do ajudante: ')

                        while True:
                            resp = str(input('Confirma [S/N]? ')).upper()
                            if resp == 'S' or resp == 'N':
                                break
                            else:
                                print(f'{cor(3)}Opçãp inválida{cor(0)}')
                        if resp == 'S':
                            des = open(arq_hj, 'at')
                            des.write(f'{dados[0]};{dados[1]};{carro[0]};{carro[1]};{carro[2]};{motorista};{ajudante};'
                                      f'{carro[3]};{data}\n')
                            des.close()
                            linha('-', 25)
                            break

        des = open(arq_hj, 'r')
        existe = des.read()
        des.close()

        if len(existe) == 0:
            print('ERRO... NÃO HÁ ORDENS DE CARGA')
            os.remove(arq_hj)
        else:
            relatorios.controleKM(arq_hj, data)
            relatorios.vistoria(arq_hj,data)

    else:
        print('PROGRAMAÇÃO JÁ FEITA')
        hoje = date.today().strftime('%d-%m-%y')
        diretorio = os.getcwd().replace('\\', '/') + '/'
        div = f'lib/arquivos/relatorio/programacao/prog {hoje}.jpg'

        while True:
            resp = str(input('ESCOLHA SUA OPÇÃO: [V] VISUALIZAR [A] APAGAR ')).upper()
            if resp in 'VA':
                break
            else:
                print('ERRO! opção incorreta, tente novamente')
        if resp == 'V':
            if arqExiste(diretorio + div):
                os.startfile(diretorio + div)
            else:
                print('ERRO! imagem de divulgação não gerada.... utilize a opção [2] Divulga')
        else:
            print('Apagando programação...')
            sleep(2)
            try:
                os.remove(diretorio + arq_hj)
            except FileNotFoundError as erro:
                print(f'ERRO - {erro}  ')
            try:
                os.remove(diretorio + div)
            except FileNotFoundError as erro:
                print(f'Erro! - {erro}')
            print('PROGRAMAÇÃO APAGADA!')

    linha('-', 42)




def geraOC(arq):
    '''

    :param arq:
    :return:
    '''

    matriz = (
            'REUNIDAS', 'EXPRESSO', 'BALNEÁRIO CAMBORIU', 'ITAJAI','TIJUCAS PALHOÇA', 'TUBARÃO', 'FPOLIS CENTRO',
            'SÃO JOSÉ', 'BNU SUL/LES', 'REUNIDAS', 'EXPRESSO', 'ARARANGUÁ', 'SÃO JOSÉ',
            'FPOLIS CENTRO','JLLE CEN/NOR','BNU NOR/OES', 'REUNIDAS', 'EXPRESSO', 'JARAGUÁ DO SUL', 'SÃO JOSÉ',
            'FPOLIS NORTE', 'PORTO BELO', 'BNU SUL/LES', 'REUNIDAS', 'EXPRESSO', 'BALNEÁRIO CAMBORIU', 'ITAJAI',
            'FPOLIS CENTRO', 'FPOLIS SUL', 'RIO DO SUL', 'LITORAL NORTE', 'JLLE CEN/SUL', 'REUNIDAS', 'EXPRESSO',
            'MAFRA', 'BRUSQUE GASPAR', 'BNU NOR/OES', 'CHAPECÓ', 'LAGES'
            )
    # PEGAR O ULTIMO REGISTRO DO ARQUIVO DE DADOS E USAR COMO PARAMETRO INICIAL
    with open(arq, 'r') as origem:
        for reg in origem:
            ultimo = reg.split(';')
            data = datetime.strptime(ultimo[2], '%d/%m/%Y')
            data_ini = data + timedelta(days=1)
            data_ult = data_ini
            while True:
                semana = diaSemana(data_ini)
                if semana == 'SEGUNDA':
                    break
                else:
                    data_ini = data_ini + timedelta(days=1)
    # VALIDAR DATAS E ROTAS
        while True:
            resp = str(input('DESEJA INCLUIR LAGES NO ROTEIRO [S/N]: ')).upper()
            if resp == 'S' or resp == 'N':
                break
            else:
                print(f'{cor (3)}Opçãp inválida{cor (0)}')
        linha('-', 80, 1)
        cont = 0
        oc = 101
        for item, valor in enumerate(matriz):

            cont += 1
            if valor == 'REUNIDAS':
                if cont == 1:
                    data_ult = data_ini
                    semana = diaSemana(data_ult)
                else:
                    data_ult = datetime.strptime(data_ult, '%d/%m/%Y')
                    data_ult = data_ult + timedelta(days=1)
                    semana = diaSemana(data_ult)
                data_ult = datetime.strftime(data_ult, '%d/%m/%Y')
                transp = '5219'
                oct = 100
                linha('-', )
                print(f'{cor(13)}{data_ult} - {semana}{cor(0)}')

            elif valor == 'EXPRESSO':
                transp = '6702'
                oct = 101

            elif ('BALNEÁRIO' in valor) or ('ITAJAI' in valor) or ('JARAGUÁ' in valor):
                transp = '5834'
            else:
                transp = '493'
            if valor != 'LAGES' or (valor == 'LAGES' and resp == 'S'):
                try:
                    origem = open(arq, 'at')
                    if valor == 'REUNIDAS' or valor == 'EXPRESSO':
                        origem.write(f'{oct};{valor};{data_ult};{transp}\n')
                        origem.close()

                    else:
                        oc += 1
                        origem.write(f'{oc};{valor};{data_ult};{transp}\n')
                        origem.close()
                except:
                    print(f'Ops! problemas em gravar dados')
                else:
                    print(f'{cor (7)}OC {oc} - {valor} {cor (1)}cadastrado com sucesso!{cor (0)}')

            else:
                oc -= 1

        data_ult = datetime.strptime(data_ult, '%d/%m/%Y')
        relatorios.geraListagemRoteiro(arq, data_ini, data_ult)
        relatorios.oc_periodo(arq, data_ini, data_ult)