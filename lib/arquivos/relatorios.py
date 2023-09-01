from lib.arquivos.ordemcarga import *
from lib.interface.layout import *
from lib.interface.cores import *
from time import sleep, strptime
from datetime import *
from lib.interface.valida import diaSemana
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
import subprocess
import fitz
import os


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

    d_ini = datetime.strftime(ini, '%d-%m-%Y')
    d_fim = datetime.strftime(fim, '%d-%m-%Y')
    linha1 = '{}{}{}{}{}{}{}'.format('+', ('-' * 11),'+', ('-' * 31), '+', ('-' * 14), '+')
    periodo = f"{datetime.strftime(ini, '%d/%m/%Y')} a {datetime.strftime(fim, '%d/%m/%Y')}"

    try:
        a = open(arquivo, 'r')
    except:
        print(f'{cor(3)} Erro ao ler o arquivo {arquivo}!{cor(0)}')
    else:
        local = f'lib/arquivos/relatorio/programacao/periodo {d_ini} a {d_fim}.txt'
        b = open(local, 'at')

        cabecalho('-', 'ROTEIRO DO PERIODO')
        print(periodo)
        print(linha1)
        print('| {}|{} |{}|'.format('OC'.center(10), 'ROTEIRO'.center(30), 'DATA'.center(14)))

        b.write(f'{periodo}\n')
        b.write(f'{linha1}\n')
        b.write('| {}|{} |{}|\n'.format('OC'.center(10), 'ROTEIRO'.center(30), 'DATA'.center(14)))

        for v in a:
            dado = v.split(';')
            dado[2] = dado[2].replace('\n', '')
            dado[2] = datetime.strptime(dado[2], '%d/%m/%Y')
            if ini <= dado[2] <= fim:
                dado[2] = datetime.strftime(dado[2], '%d/%m/%Y')
                if dado[1] == 'REUNIDAS':
                    print(linha1)
                    b.write(f'{linha1}\n')
                resultado =(f'| {dado[0]:^10}| {dado[1]:<30}| {dado[2]:^13}|')
                print(resultado)
                b.write(f'{resultado}\n')
        print(linha1)
        b.write(linha1)
        a.close()
        b.close()
        while True:
            resp = str(input('DESEJA IMPRIMIR O RESUMO DOS ROTEIROS [S/N]: ')).upper()
            if resp == 'S' or resp == 'N':
                break
            else:
                print(f'{cor(3)}Opçãp inválida{cor(0)}')
        if resp == 'S':
            imprime(local)


def mm(x):
    return x / 0.352777


def divulga(arq_data, data):

    try:
        arq = open(arq_data, 'r')
        os.system("taskkill /f /im Acrobat.exe")
    except:
        print(f'{cor(3)}Ops! erro ao acessar o arquivo...{cor(0)}')
    else:
        print(f'{cor(5)}Analizando os dados.', end='')
        sleep(0.25)
        print(' .', end=''); sleep(0.25); print(' .', end=''); sleep(0.25)
        print(' .', end=''); sleep(0.25); print(f' tudo certo! ', end=''); sleep(0.25)
        print(f'{cor(1)}Gerando relatório {cor(0)}\n')
        sleep(0.50)

        arquivo = f'lib/arquivos/relatorio/programacao/prog {data}.pdf'

        cont = 0
        for p in arq: #conta quantas rotas contem na programação
            cont += 1

        alt = 35 + (cont * 20)
        div = canvas.Canvas(arquivo, pagesize=(mm(260), mm(alt)))
        div.setFillColorRGB(0, 0.5, 0.80)  # cor RGB azul escuro
        div.rect(mm(5), mm(alt - 30), mm(250), mm(15), fill=1)  # retangulo fundo azul escuro
        div.setLineWidth(1.5)  # espessura da linha
        div.setFont('Helvetica-Bold', 25)  # fonte e tamanho
        div.setFillColorRGB(0, 0, 0)
        div.drawCentredString(mm(130), mm(alt - 9), 'PROGRAMAÇÃO DE VIAGEM')
        div.line(mm(5), mm(alt - 15), mm(255), mm(alt - 15))  # primeira linha
        div.line(mm(5), mm(alt - 30), mm(5), mm(alt - 15))  # primeira coluna
        div.line(mm(90), mm(alt - 30), mm(90), mm(alt - 15))  # segunda coluna
        div.line(mm(140), mm(alt - 30), mm(140), mm(alt - 15))  # terceira coluna
        div.line(mm(255), mm(alt - 30), mm(255), mm(alt - 15))  # quarta coluna
        div.line(mm(5), mm(alt - 30), mm(255), mm(alt - 30))  # segunda linha
        div.setFillColorRGB(255, 255, 255)  # cor que o proximo texto vai assumir - branco
        div.drawCentredString(mm(45), mm(alt - 27), 'ROTEIRO')
        div.drawCentredString(mm(115), mm(alt - 27), 'CARRO')
        div.drawCentredString(mm(197), mm(alt - 27), 'COLABORADORES')

        linSup = alt - 30
        linInf = alt - 50
        tex = alt - 45

        arq.close()
        try:
            arq = open(arq_data, 'r')
            os.system("taskkill /f /im Acrobat.exe")
        except:
            print(f'{cor(3)}Ops! erro ao acessar o arquivo...{cor(0)}')
        else:
            for v in arq:
                dados = v.split(';')
                dados[6] = dados[6].replace('\n', '')
                div.setFillColorRGB(0, 1, 1)
                div.rect(mm(5), mm(linInf), mm(250), mm(20), fill=1)
                div.setFillColorRGB(0, 0, 0)
                div.line(mm(5),   mm(linSup), mm(5),   mm(linInf))  # coluna
                div.line(mm(90),  mm(linSup), mm(90),  mm(linInf))  # coluna
                div.line(mm(140), mm(linSup), mm(140), mm(linInf))  # coluna
                div.line(mm(255), mm(linSup), mm(255), mm(linInf))  # coluna
                div.line(mm(5),   mm(linInf), mm(255), mm(linInf))  # linha inferior
                div.drawString(mm(7), mm(tex), dados[1])
                div.drawCentredString(mm(115), mm(tex), dados[3])
                div.drawString(mm(143), mm(tex), dados[5])
                div.drawString(mm(207), mm(tex), dados[6])
                print(f'OC {dados[0]} ..... ok!')
                sleep(0.5)
                linSup -= 20
                linInf -= 20
                tex -= 20

            div.save()

        diretorio = os.getcwd().replace("\\", "/") + '/'
        arq_jpg = f'lib/arquivos/relatorio/programacao/escalacao.jpg'

        # converter em imagem
        while not arqExiste(arquivo):
            sleep(0.1)
            print("." , end='')
        poppler_path = r'C:\agr-exped\lib\arquivos\relatorio\poppler-0.68.0\bin\pdftoppm.exe'

        subprocess.Popen('"%s" -jpeg "%s" prog' % (poppler_path, arquivo))
        jpg = diretorio + 'prog-1.jpg'
        print('\nGERANDO IMAGEM PARA DIVULGAÇÃO  ', end='')
        while not arqExiste(jpg):
            sleep(0.1)
            print('. ', end='')

        try:
            #shutil.move(jpg, arq_jpg)
            os.rename(jpg, arq_jpg)
            print('\nRELATÓRIO CONCLUIDO')
        except PermissionError as e:
            print(e)
            pass


def geraListagemRoteiro(arquivo, ini, fim):
    dat_ini = datetime.strftime(ini, '%d-%m-%Y')
    dat_fim = datetime.strftime(fim, '%d-%m-%Y')
    relatorio = f'lib/arquivos/relatorio/programacao/roteiro {dat_ini} a {dat_fim}.pdf'
    pdf = canvas.Canvas(relatorio, pagesize=A4)
    pdf.setLineWidth(1.5)
    diaAux = ''
    pag = 1
    lin = 750
    tex = 715
    col = 700
    try:
        arq = open(arquivo, 'r')
    except:
        print(f'{cor(3)} Erro ao ler o arquivo {arquivo}!{cor(0)}')

    for reg in arq:
        dado = reg.split(';')
        dado[2] = dado[2].replace('\n', '')
        dado[2] = datetime.strptime(dado[2], '%d/%m/%Y')
        if ini <= dado[2] <= fim:
            data1 = dado[2] = datetime.strftime(dado[2], '%d/%m/%Y')
            data = datetime.strptime(dado[2], '%d/%m/%Y')
            diaSem = diaSemana(data)
            pdf.setLineWidth(1.5)

            if pag == 1:
                #  TABELA CABEÇALHO PRIMEIRA PAGINA
                pdf.setFont('Helvetica-Bold', 20)
                pdf.line(10, 800, 580, 800)
                pdf.line(10, 800, 10, 770)
                pdf.drawString(20, 777, 'DATA')
                pdf.line(126, 800, 126, 770)
                pdf.drawString(136, 777, data1)
                pdf.line(450, 800, 450, 770)
                pdf.drawString(460, 777, diaSem)
                pdf.line(580, 800, 580, 770)
                pdf.line(10, 770, 580, 770)
                diaAux = diaSem
                pag += 1

            if diaSem != diaAux:
                pdf.showPage()  # QUEBRA PAGINA
                lin = 750
                tex = 715
                col = 700

                # TABELA CABEÇALHO DAS OUTRAS PAGIANS
                pdf.setLineWidth(1.5)
                pdf.setFont('Helvetica-Bold', 20)
                pdf.line(10, 800, 580, 800)
                pdf.line(10, 800, 10, 770)
                pdf.drawString(20, 777, 'DATA')
                pdf.line(126, 800, 126, 770)
                pdf.drawString(136, 777, data1)
                pdf.line(450, 800, 450, 770)
                pdf.drawString(460, 777, diaSem)
                pdf.line(580, 800, 580, 770)
                pdf.line(10, 770, 580, 770)

                diaAux = diaSem

            # TABELA PRINCIPAL
            pdf.line(10, lin, 580, lin)  # ___
            pdf.line(10, lin, 10, col)
            pdf.setFont('Helvetica-Bold', 30)
            pdf.drawString(20, tex, dado[0])
            pdf.line(126, lin, 126, col)
            pdf.setFont('Helvetica-Bold', 20)
            pdf.drawString(136, tex, dado[1])
            pdf.line(380, lin, 380, col)
            pdf.line(450, lin, 450, col)
            pdf.line(580, lin, 580, col)
            lin -= 50
            tex -= 50
            col -= 50
            pdf.line(10, lin, 580, lin)
            pdf.setLineWidth(0.5)
            pdf.line(10, 20, 580,20)
            pdf.setFont('Helvetica', 8)
            pdf.drawString(10, 10, 'Gerado por Focus v1.0')

    pdf.save()
    while True:
        resp = str(input('DESEJA IMPRIMIR O RELATÓRIO DOS ROTEIROS [S/N]: ')).upper()
        if resp == 'S' or resp == 'N':
            break
        else:
            print(f'{cor(3)}Opçãp inválida{cor(0)}')
    if resp == 'S':
        copia = leiaInt('Quantas copias?: ')
        imprime(relatorio,copia)
    geraPlacas(arquivo, ini, fim)


def geraPlacas(arquivo, ini, fim):
    dat_ini = datetime.strftime(ini, '%d-%m-%Y')
    dat_fim = datetime.strftime(fim, '%d-%m-%Y')
    relatorio = f'lib/arquivos/relatorio/programacao/placas {dat_ini} a {dat_fim}.pdf'
    pdf = canvas.Canvas(relatorio, pagesize=A4)
    pdf.setLineWidth(1)
    try:
        arq = open(arquivo, 'r')
    except:
        print(f'{cor(3)} Erro ao ler o arquivo {arquivo}!{cor(0)}')

    for reg in arq:
        dado = reg.split(';')
        dado[2] = dado[2].replace('\n', '')
        dado[2] = datetime.strptime(dado[2], '%d/%m/%Y')

        if ini <= dado[2] <= fim:
            pdf.line(20, 830, 570, 830)
            pdf.line(20, 15, 570, 15)
            pdf.line(20, 830, 20, 15)
            pdf.line(570, 830, 570, 15)

            if dado[1] != 'REUNIDAS' and dado[1] != 'EXPRESSO':
                if dado[1].count(' ') == 1:
                    praca = dado[1].split()
                    pdf.setFont('Helvetica-Bold', 170)
                    pdf.drawCentredString(290, 630, dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 90)
                    pdf.drawCentredString(290, 350, praca[0])
                    pdf.drawCentredString(290, 200, praca[1])
                elif dado[1] == 'ARARANGUÁ':
                    pdf.setFont('Helvetica-Bold', 170)
                    pdf.drawCentredString(290, 630, dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 80)
                    pdf.drawCentredString(290, 320, 'ARARANGUÁ')

                elif dado[1] == 'JARAGUÁ DO SUL':
                    pdf.setFont('Helvetica-Bold', 170)
                    pdf.drawCentredString(290, 630, dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 90)
                    pdf.drawCentredString(290, 320, 'JARAGUÁ')

                elif dado[1] == 'RIO DO SUL':
                    pdf.setFont('Helvetica-Bold', 170)
                    pdf.drawCentredString(290, 630, dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 90)
                    pdf.drawCentredString(290, 320, dado[1])

                else:
                    pdf.setFont('Helvetica-Bold', 170)
                    pdf.drawCentredString(290, 630, dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 90)
                    pdf.drawCentredString(290, 320, dado[1])
                pdf.showPage()

    # pagina com as datas

    inicio = ini
    flag = fim
    tex = 741
    lin = 681
    while inicio <= flag:
        pdf.setFont('Helvetica-Bold', 50)
        pdf.setLineWidth(0.7)
        semana = diaSemana(inicio)
        data = datetime.strftime(inicio,'%d/%m/%Y')
        pdf.drawString(40, tex, semana)
        pdf.drawString(310, tex, data)
        pdf.line(20, lin, 570, lin)
        tex -= 165
        lin -= 165
        inicio = inicio + timedelta(days=1)
    pdf.save()

    while True:
        resp = str(input('DESEJA IMPRIMIR AS PLACAS DA SACARIA? [S/N]: ')).upper()
        if resp == 'S' or resp == 'N':
            break
        else:
            print(f'{cor(3)}Opçãp inválida{cor(0)}')
    if resp == 'S':
        copia = leiaInt('Quantas copias?: ')
        imprime(relatorio, copia)


def controleKM(arq,dt):
    data = datetime.strptime(dt,'%d/%m/%Y')
    data += timedelta(days=1)

    if diaSemana(data) == 'SABADO':
        data += timedelta(days=2)
    datarel = data.strftime('%d/%m/%Y')
    dataarq = data.strftime('%d-%m-%y')
    arqpdf = f'lib/arquivos/relatorio/programacao/controle_KM {dataarq}.pdf'
    imagem = f'lib/arquivos/database/logo.jpg'
    km = canvas.Canvas(arqpdf, pagesize=A4)
    ori = open(arq, 'r') #arquivo de dados

    for reg in ori:
        dado = reg.split(';')
        km.setFont('Helvetica-Bold', 22)
        km.drawCentredString(mm(40), mm(249), dado[0])
        km.drawCentredString(mm(124), mm(249), dado[1])
        km.drawString(mm(70), mm(238), datarel)
        km.drawString(mm(70), mm(228), dado[2])
        km.drawString(mm(85), mm(228), dado[4])
        km.drawString(mm(70), mm(218), dado[5])
        km.drawImage(imagem, mm(16), mm(265), 99, 31)
        km.setFont('Helvetica-Bold', 12)
        km.drawString(mm(70), mm(267), 'CONTROLE DE QUILOMETRAGEM POR ORDEM DE CARGA')

        km.setFont('Helvetica-Bold', 20)
        km.rect(mm(16), mm(196), mm(180), mm(63))  # borda exterior
        km.rect(mm(16), mm(246), mm(180), mm(13))  # linha 1
        km.rect(mm(16), mm(236), mm(180), mm(10))  # linha 2
        km.drawString(mm(19), mm(238), 'DATA')
        km.rect(mm(16), mm(226), mm(180), mm(10))  # linha 3
        km.drawString(mm(19), mm(228), 'CARRO')
        km.rect(mm(16), mm(216), mm(180), mm(10))  # linha 4
        km.drawString(mm(19), mm(218), 'MOTORISTA')
        km.rect(mm(16), mm(206), mm(180), mm(10))  # linha 5
        km.drawString(mm(19), mm(208), 'KM INICIAL')
        km.line(mm(68), mm(259), mm(68), mm(196))  # coluna
        km.drawString(mm(19), mm(198), 'KM FINAL')
        km.setFont('Helvetica-Bold', 12)
        km.drawString(mm(17), mm(187), 'OCORRÊNCIAS')

        lin = 135
        # ocorrencias
        for c in range(0, 3):
            km.rect(mm(16), mm(lin), mm(180), mm(50)) # retangulo borda externa 50mm x 180mm
            km.line(mm(16), (mm(lin) + mm(45)), mm(196), (mm(lin) + mm(45))) # 1 linha ini +  linha col 16 ate col 196
            km.line(mm(16), (mm(lin) + mm(35)), mm(196), (mm(lin) + mm(35))) # 2 linha col 16 ate col 196
            km.line(mm(16), (mm(lin) + mm(30)), mm(196), (mm(lin) + mm(30)))
            km.line(mm(16), (mm(lin) + mm(20)), mm(196), (mm(lin) + mm(20)))
            km.line(mm(16), (mm(lin) + mm(10)), mm(196), (mm(lin) + mm(10)))
            km.line(mm(45), (mm(lin) + mm(50)), mm(45), mm(lin))
            km.line(mm(155), (mm(lin) + mm(35)), mm(155), mm(lin))
            km.line(mm(175), (mm(lin) + mm(35)), mm(175), mm(lin))
            km.setFont('Helvetica-Bold', 10)
            km.drawString(mm(18), (mm(lin) + mm(46)), 'NF')
            km.drawString(mm(47), (mm(lin) + mm(46)), 'CLIENTE / CIDADE')
            km.drawString(mm(18), (mm(lin) + mm(31)), 'QDADE')
            km.drawCentredString(mm(95), (mm(lin) + mm(31)), 'PRODUTO')
            km.drawString(mm(157), (mm(lin) + mm(31)), 'FALTA')
            km.drawString(mm(177), (mm(lin) + mm(31)), 'AVARIA')
            lin -= 57
        # retangulo com oc e contagem
        km.setFont('Helvetica-Bold', 18)
        km.rect(mm(115), mm(5), mm(80),  mm(10))
        km.line(mm(155), mm(5), mm(155), mm(15))
        km.drawString(mm(120), mm(7), "OC ") #informa
        km.drawString(mm(135), mm(7), dado[0])
        km.drawString(mm(160), mm(7), "VOL")
        # quebra pagina
        km.showPage()
    km.save()
    while True:
        resp = str(input('DESEJA IMPRIMIR OS CONTROLES DE KM? [S/N]: ')).upper()
        if resp == 'S' or resp == 'N':
            break
        else:
            print(f'{cor(3)}Opçãp inválida{cor(0)}')
    if resp == 'S':
        imprime(arqpdf)


def vistoria(arquivo, data):
    data = datetime.strptime(data, '%d/%m/%Y')
    dataArq = data.strftime('%d-%m-%y')
    imagem = 'lib/arquivos/database/logo.jpg'
    arqvis = f'lib/arquivos/relatorio/programacao/vistoria {dataArq}.pdf'
    vis = canvas.Canvas(arqvis, pagesize=A4)
    with open(arquivo, 'r') as dados:
        for reg in dados:
            dado = reg.split(';')
            dado[8] = dado[8].replace('\n', '')
            vis.setFont('Helvetica-Bold', 13)
            vis.drawString(mm(38), mm(257), dado[7])
            vis.drawString(mm(157), mm(257), 'AGROSUL')
            vis.drawString(mm(38), mm(248), dado[0])
            vis.drawString(mm(157), mm(248), '47-3330-5747')
            vis.drawString(mm(38), mm(239), dado[8])
            vis.drawString(mm(38), mm(230), dado[4])
            vis.drawString(mm(157), mm(230), dado[5])

            ##### CONTRUÇÃO DO RELATORIO #####

            # cabeçalho

            vis.drawImage(imagem, mm(10), mm(275), 99, 31)
            vis.drawString(mm(83), mm(278), 'ORDEM DE CARREGAMENTO')
            vis.setLineWidth(0.2)
            vis.line(mm(2), mm(268), mm(205), mm(268))

            # primeiro bloco - dados do roteiro (oc, veiculo, motorista)
            vis.setFont('Helvetica-Bold', 10)
            vis.rect(mm(35), mm(255), mm(50), mm(7))
            vis.drawString(mm(5), mm(257), ' Veiculo')
            vis.rect(mm(35), mm(246), mm(50), mm(7))
            vis.drawString(mm(5), mm(248), 'Ordem/Rota')
            vis.rect(mm(35), mm(237), mm(50), mm(7))
            vis.drawString(mm(5), mm(239), 'Data Expedição')
            vis.rect(mm(35), mm(228), mm(50), mm(7))
            vis.drawString(mm(5), mm(230), 'Placa Veiculo')
            vis.rect(mm(155), mm(255), mm(50), mm(7))
            vis.drawString(mm(125), mm(257), 'Transportadora')
            vis.rect(mm(155), mm(246), mm(50), mm(7))
            vis.drawString(mm(125), mm(248), 'Contato')
            vis.rect(mm(155), mm(228), mm(50), mm(7))
            vis.drawString(mm(125), mm(230), 'Motorista')

            # segundo bloco - avaliação de segurança e meio ambiente
            vis.setFillColorRGB(0.7, 0.7, 0.7)
            vis.rect(mm(5), mm(218), mm(200), mm(6), fill=1)
            vis.setFillColorRGB(0, 0, 0)
            vis.setFont('Helvetica-Bold', 8)
            vis.drawString(mm(50), mm(220), 'Avaliação de Segurança e Meio Ambiente')
            vis.drawString(mm(146), mm(220), 'C    NC    NA       Observação/Medidas')

            lin = 209
            topicoSeg = [
                'Os pneus não devem apresentar desgaste excessivo, trincos, ressolagem solta e avarias?',
                'Farois,lanternas e setas estão funcionando?',
                'Para-brisa e vidros laterais estão ausentes de tricos?',
                'Ausência de vasamento de óleo ou graxa?',
                'Conhecimento das normas de segurança e meio ambiente?',
                'Luz de ré funcionando?',
                'Luz de freio funcionando?'
            ]
            for i in range(0, 6):
                vis.rect(mm(5), mm(lin), mm(200), mm(6), fill=0)
                vis.line(mm(145), mm(lin), mm(145), mm(lin + 6))
                vis.drawString(mm(6), mm(lin + 1), topicoSeg[i])
                vis.drawString(mm(147), mm(lin + 2), 'x')
                vis.line(mm(151), mm(lin), mm(151), mm(lin + 6))
                vis.line(mm(157), mm(lin), mm(157), mm(lin + 6))
                vis.line(mm(163), mm(lin), mm(163), mm(lin + 6))
                lin -= 6

            # terceiro bloco - Avaliação qualiodade e Bug Out

            vis.setFillColorRGB(0.7, 0.7, 0.7)
            vis.rect(mm(5), mm(170), mm(200), mm(6), fill=1)
            vis.setFillColorRGB(0, 0, 0)
            vis.setFont('Helvetica-Bold', 8)
            vis.drawString(mm(50), mm(172), 'Avaliação de Qualidade e Bug Out')
            vis.drawString(mm(146), mm(172), 'C    NC    NA       Observação/Medidas')

            topicoQual = [
                'Integridade do Baú?',
                'Interior do Baú limpo?',
                'Constatação de pragas?',
                'Durante o embarque/desembarque foi constatado algum vestigio de praga?',
                'Assoalho forrado com placas de papelão?',
                'Placas de papelão sem vestigio de pragas?',
                'Paletes de madeira sem vestigio de pragas?',
                'Motorista uniformizado e com EPI?'
            ]

            lin = 161
            for i in range(0, 8):
                vis.rect(mm(5), mm(lin), mm(200), mm(6), fill=0)
                vis.line(mm(145), mm(lin), mm(145), mm(lin + 6))
                vis.drawString(mm(6), mm(lin + 1), topicoQual[i])
                vis.drawString(mm(147), mm(lin + 2), 'x')
                vis.line(mm(151), mm(lin), mm(151), mm(lin + 6))
                vis.line(mm(157), mm(lin), mm(157), mm(lin + 6))
                vis.line(mm(163), mm(lin), mm(163), mm(lin + 6))
                lin -= 6

            # quarto bloco -

            vis.rect(mm(5), mm(110), mm(200), mm(6))
            vis.setFillColorRGB(0, 0, 0)
            vis.setFont('Helvetica-Bold', 8)
            vis.drawString(mm(7), mm(112), 'Portas com cadeados -')

            lin = 100
            vis.setFont('Helvetica', 7)
            vis.drawString(mm(5), mm(101), 'Tratativa (Observação/Medidas):')
            for i in range(0, 5):
                vis.line(mm(5), mm(lin), mm(205), mm(lin))
                lin -= 4

            vis.drawString(mm(5), mm(75), 'Data: _______/_______/________')
            vis.drawString(mm(110), mm(75), 'Expedidor: __________________________________________')
            vis.drawString(mm(125), mm(76), ' AGROSUL')
            vis.drawString(mm(5), mm(70), 'Hora: _________________')
            vis.drawString(mm(110), mm(65), 'Responsável pela verificação: _______________________')
            vis.drawString(mm(110), mm(55), 'Motorista: __________________________________________')
            vis.drawString(mm(125), mm(56), dado[5])
            vis.setFont('Helvetica-Bold', 6)
            vis.drawString(mm(110), mm(45), 'C: Significa "CONFORME", ou seja, o equipamento está em condições de uso')
            vis.drawString(mm(110), mm(40),
                           'NC: Signfica "NÃO CONFORME", ou seja, o equipamento não está em condiçõers de uso')
            vis.drawString(mm(110), mm(35),
                           'NA: Significa "NÃO APLICÁVEL",ou seja, o item não atende mais a realidade do equipamento')
            vis.line(mm(2), mm(30), mm(205), mm(30))
            vis.drawString(mm(5), mm(25), 'Senhores motoristas:')
            vis.drawString(mm(5), mm(20),
                           'Operador lhe informará o peso total da carga e a quantidade de paletes de sacos e caixas, '
                           'onde os Srs lhe dizerão a devida disponibilidade dos paletes no veiculo,')
            vis.drawString(mm(5), mm(15),
                           'uma vez que se responsabiliza pela carga, após a saída do veiculo da Royal Canin do Brasil')

            vis.showPage()

    vis.save()
    while True:
        resp = str(input('DESEJA IMPRIMIR VISTORIAS? [S/N]: ')).upper()
        if resp == 'S' or resp == 'N':
            break
        else:
            print(f'{cor(3)}Opçãp inválida{cor(0)}')
    if resp == 'S':
        imprime(arqvis)
        

def geraPlacasPicking(arquivo,data):
    relatorio = f'lib/arquivos/relatorio/programacao/placasPicking.pdf'
    pdf = canvas.Canvas(relatorio, pagesize=A4)
    pdf.setLineWidth(1)
    try:
        arq = open(arquivo, 'r')
    except:
        print(f'{cor(3)} Erro ao ler o arquivo {arquivo}!{cor(0)}')

    novaPag = True
    for reg in arq:
            dado = reg.split(';')
            dado[2] = dado[2].replace('\n', '')
            if dado[2] == data:
                dado[1] = dado[1].replace('FPOLIS', 'FP')
                dado[1] = dado[1].replace('TIJUCAS PALHOÇA', 'TIJUCAS')
                dado[1] = dado[1].replace('JARAGUÁ DO SUL', 'JARAGUA')
                dado[1] = dado[1].replace('LITORAL NORTE', 'NAVEGA')
                dado[1] = dado[1].replace('BALNEÁRIO CAMBORIU', 'B C ')
                dado[1] = dado[1].replace('BRUSQUE GASPAR', 'BRUSQUE')
                dado[1] = dado[1].replace('JLLE CEN/NOR', 'JVILLE')
                dado[1] = dado[1].replace('JLLE CEN/SUL', 'JVILLE')

                if novaPag:
                    pdf.setFont('Helvetica-Bold', 120)
                    pdf.drawCentredString(mm(105), mm(230), dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 80)
                    pdf.drawCentredString(mm(105), mm(170), dado[1])
                    pdf.line(mm(10), mm(150), mm(200), mm(150))
                    novaPag = False
                else:
                    pdf.setFont('Helvetica-Bold', 120)
                    pdf.drawCentredString(mm(105), mm(80), dado[0])  # COL, LIN
                    pdf.setFont('Helvetica-Bold', 80)
                    pdf.drawCentredString(mm(105), mm(20), dado[1])
                    novaPag = True
                    pdf.showPage()
                if dado[1] == 'CHAPECÓ':
                    rotaChape = ['JOAÇABA', 'XANXERE', 'CONCORDIA']
                    for rot in rotaChape:
                        if novaPag:
                            pdf.setFont('Helvetica-Bold', 120)
                            pdf.drawCentredString(mm(105), mm(230), dado[0])  # COL, LIN
                            pdf.setFont('Helvetica-Bold', 80)
                            pdf.drawCentredString(mm(105), mm(170), rot)
                            pdf.line(mm(10), mm(150), mm(200), mm(150))
                            novaPag = False
                        else:
                            pdf.setFont('Helvetica-Bold', 120)
                            pdf.drawCentredString(mm(105), mm(80), dado[0])  # COL, LIN
                            pdf.setFont('Helvetica-Bold', 80)
                            pdf.drawCentredString(mm(105), mm(20), rot)
                            novaPag = True
                            pdf.showPage()
    pdf.save()
    return relatorio


def pdftojpg(pdf_path, output_dir):
    doc = fitz.open(pdf_path)
    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        imagem = f"{output_dir}/imagem_{i + 1}.jpg"
        pix.save(imagem, "JPEG")
    return imagem

def imprime(arquivo, copias):
    diretorio = os.getcwd().replace("\\", "/") + '/' + str(arquivo)
    arq = diretorio
    n = 1
    while n <= copias:
        os.startfile(arq, 'print')
        n += 1
    print('imprimindo arquivo ... ' + str(arq))
    sleep(3)
    input('pressione ENTER para continuar...')
    if diretorio.endswith('.pdf'):
        os.system("taskkill /f /im Acrobat.exe")  # if aqruivo for pdf, feche o acrobat
    #win32api.ShellExecute(0, 'print', os.path.join(arq), None, '.', 0)

