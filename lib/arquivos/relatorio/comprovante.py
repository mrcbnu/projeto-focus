from lib.arquivos.ordemcarga import arqExiste, criarArquivo
from lib.interface.cores import *
from lib.interface.valida import leiaInt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from time import sleep
from lib.arquivos.relatorios import imprime
from lib.interface.layout import *
import os


def mm(x):
    return x / 0.352777


def comprovante():
    cabecalho('-', 'COMPROVANTE DE ENTREGA')
    arquivo = 'c:/agr-exped/lib/arquivos/database/comprovante.txt'
    if not arqExiste(arquivo):
        print(f'Arquivo {cor(3)}{arquivo} {cor(0)} não encontrado...')
        sleep(0.2)
        criarArquivo(arquivo)
        sleep(0.2)
    arq = open(arquivo, 'at')
    print('-' * 12, ' DADOS DO CLIENTE ', '-' * 13)
    lstComprovante = []
    cliente = str(input('Cliente:')).upper()
    lstComprovante.append(cliente)
    cidade = str(input('Cidade:')).upper()
    lstComprovante.append(cidade)
    endereco = str(input('Endereço:')).upper()
    lstComprovante.append(endereco)
    nf = leiaInt('Nota Fiscal: ')
    lstComprovante.append(nf)
    transportadora = str(input('Transportadora:')).upper()
    lstComprovante.append(transportadora)
    observacao = str(input('Observações: ')).upper()
    lstComprovante.append(observacao)
    arq.write(f'{cliente};{cidade};{endereco};{nf};{transportadora};')
    print('\n','-' * 10, ' PRODUTOS OU MATERIAIS ', '-' * 10)

    while True:
        produto = str(input('Produto:')).upper()
        lstComprovante.append(produto)
        qdade = leiaInt('Qdade:')
        lstComprovante.append(qdade)
        arq.write(f'{produto};{qdade}')
        while True:
            resp = str(input('Deseja adicionar outro produto [S/N]?')).upper()
            if resp == 'N' or resp =='S':
                break
        if resp == 'N':
            arq.write('\n')
            break
        else:
            arq.write(';')

    arq.close()
    print('\n','-'* 43)
    geraComprovante(lstComprovante)

def geraComprovante(lista):
    # data = datetime.strptime(data, '%d/%m/%Y')
    # dataArq = data.strftime('%d-%m-%y')
    # print(dataArq)

    imagem = 'lib/arquivos/database/logo.jpg'
    arqcom = f'lib/arquivos/relatorio/comprovantes/comprovante.pdf'
    com = canvas.Canvas(arqcom, pagesize=A4)

    ##### CONSTRUÇÃO DO RELATORIO #####

    # cabeçalho

    com.drawImage(imagem, mm(10), mm(275), 99, 31)
    com.setFont('Helvetica-Bold', 15)
    com.drawString(mm(83), mm(278), 'COMPROVANTE DE ENTREGA')
    com.setLineWidth(0.2)
    com.line(mm(5), mm(268), mm(205), mm(268))

    # primeiro bloco - dados do CLIENTE
    com.setFont('Helvetica-Bold', 11)
    com.rect(mm(40), mm(255), mm(95), mm(7))
    com.drawString(mm(5), mm(257), 'Cliente:')
    com.rect(mm(40), mm(246), mm(165), mm(7))
    com.drawString(mm(5), mm(248), 'Endereço:')
    com.rect(mm(40), mm(237), mm(50), mm(7))
    com.drawString(mm(5), mm(239), 'Ref Nota Fiscal:')
    com.rect(mm(40), mm(228), mm(50), mm(7))
    com.drawString(mm(5), mm(230), 'Data Expedição:')
    com.rect(mm(155), mm(255), mm(50), mm(7))
    com.drawString(mm(140), mm(257), 'Cidade:')
    com.rect(mm(155), mm(228), mm(50), mm(7))
    com.drawString(mm(124), mm(230), 'Transportadora:')

    # segundo bloco - PRODUTOS
    com.line(mm(5), mm(220), mm(205), mm(220))
    com.setFillColorRGB(0.9, 0.8, 0.8)
    com.rect(mm(5), mm(205), mm(200), mm(6), fill=1)
    com.setFillColorRGB(0, 0, 0)
    com.setFont('Helvetica-Bold', 9)
    com.drawString(mm(90), mm(207), 'PRODUTOS OU MATERIAIS')
    com.drawString(mm(40), mm(200), 'QDADE')
    com.drawString(mm(65), mm(200), 'DESCRIÇÃO')
    com.line(mm(5), mm(75), mm(205), mm(75))

    # terceiro bloco - ASSINATURA CLIENTE

    com.setFont('Helvetica', 8)
    com.drawString(mm(5), mm(70), 'Observações')
    com.setFont('Helvetica-Bold', 9)
    com.drawCentredString(mm(110), mm(40), 'DECLARO TER RECEBIDO DA AGROSUL CATARINENSE LTDA, TODOS OS ITENS')
    com.drawCentredString(mm(110), mm(35), 'E SERVIÇOS DESCRITOS ACIMA')
    com.drawCentredString(mm(110), mm(20), '__________________________________')
    com.drawCentredString(mm(110), mm(15), 'ASSINATURA DO CLIENTE')

    # leitura dos dados e prenchimento do relatorio

    campo = len(lista)-1
    #print(campo)
    com.setFont('Helvetica-Bold', 11)
    com.drawString(mm(42), mm(257), lista[0])
    com.drawString(mm(157), mm(257), lista[1])
    com.drawString(mm(42), mm(248), lista[2])
    com.drawString(mm(42), mm(239), str(lista[3]))
    com.drawString(mm(157), mm(230), lista[4])
    com.drawString(mm(5), mm(65), lista[5])
    linha = 185
    for i in range(6, campo, 2):
        a = str(lista[i])
        b = str(lista[i + 1])
        com.drawString(mm(65), mm(linha), a)
        com.drawString(mm(45), mm(linha), b)

        linha -= 10

    com.save()
    print('\nGerando impressão do comprovante....\n')
    sleep(2)
    imprime(arqcom, 1)
###
