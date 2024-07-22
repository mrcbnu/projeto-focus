from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from time import sleep, strptime
from lib.arquivos.ordemcarga import *
from lib.arquivos.relatorios import pdftojpg

def mm(x):
    return x / 0.352777


def controle(dados):

    print('GERANDO RELATÓRIO CONTROLE DE QUILOMETRAGEM')
    escala_df = dados
    # excluir linhas das transportadoras expresso e reunidas
    escala_df = escala_df.drop(escala_df[escala_df['Motorista'] == 'MOTORISTA TRANSPORTADORA'].index)
    escala_df = escala_df.reset_index()  # reseta o indice do dataframe após excluir transportadora
    # gerar DataFrame
    escala = escala_df[['Carga ERP', 'Destino', 'Veículo', 'Motorista', 'Ajudante 1', 'Ajudante 2', 'Data']]

    # gerar relatorio
    arqpdf = 'lib/arquivos/relatorio/programacao/controle_KM.pdf'
    imagem = 'lib/arquivos/database/logo.jpg'
    km = canvas.Canvas(arqpdf, pagesize=A4)
    linha = len(escala.axes[0])

    for cont in range(linha):
        dado = escala.loc[cont]
        if dado['Motorista'] != 'PAULO CESAR WIRTH':
            print(f"{dado['Carga ERP']}...ok")
            data = str(dado['Data'])
            data = data[:-9]
            km.setFont('Helvetica-Bold', 22)
            km.drawCentredString(mm(40), mm(249), str(dado['Carga ERP']))
            km.drawString(mm(70), mm(249), dado['Destino'])
            km.drawString(mm(70), mm(238), data)
            km.drawString(mm(70), mm(228), dado['Veículo'])
            # km.drawString(mm(85), mm(228), dado[4])
            km.drawString(mm(70), mm(218), dado['Motorista'])
            km.drawImage(imagem, mm(16), mm(265), 99, 31)
            km.setFont('Helvetica-Bold', 12)
            km.drawString(mm(70), mm(267), 'CONTROLE DE QUILOMETRAGEM POR ORDEM DE CARGA')

            km.setFont('Helvetica-Bold', 20)
            km.rect(mm(16), mm(196), mm(180), mm(63))  # borda exterior
            km.rect(mm(16), mm(246), mm(180), mm(13))  # linha 1
            km.rect(mm(16), mm(236), mm(180), mm(10))  # linha 2
            km.drawString(mm(19), mm(238), 'DATA SAIDA')
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
                km.rect(mm(16), mm(lin), mm(180), mm(50))  # retangulo borda externa 50mm x 180mm
                km.line(mm(16), (mm(lin) + mm(45)), mm(196),
                        (mm(lin) + mm(45)))  # 1 linha ini +  linha col 16 ate col 196
                km.line(mm(16), (mm(lin) + mm(35)), mm(196), (mm(lin) + mm(35)))  # 2 linha col 16 ate col 196
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
            km.rect(mm(115), mm(5), mm(80), mm(10))
            km.line(mm(155), mm(5), mm(155), mm(15))
            km.drawString(mm(120), mm(7), "OC ")  # informa
            km.drawString(mm(135), mm(7), str(dado['Carga ERP']))
            km.drawString(mm(160), mm(7), "VOL")
            # quebra pagina
            km.showPage()
    km.save()
    return arqpdf


def vistoria(dados):
    escala_df = dados
    # excluir linhas das transportadoras expresso e reunidas
    escala_df = escala_df.drop(escala_df[escala_df['Motorista'] == 'MOTORISTA TRANSPORTADORA'].index)
    escala_df = escala_df.reset_index()  # reseta o indice do dataframe após excluir transportadora
    # gerar DataFrame
    escala = escala_df[['Carga ERP', 'Destino', 'Veículo', 'Motorista', 'Data']]

    imagem = 'lib/arquivos/database/logo.jpg'
    arqvis = 'lib/arquivos/relatorio/programacao/vistoria.pdf'
    vis = canvas.Canvas(arqvis, pagesize=A4)

    linha = len(escala.axes[0])
    for cont in range(linha):
        dado = escala.loc[cont]
        print(f"{dado['Carga ERP']}...ok")
        data = str(dado['Data'])
        data = data[:-9]
        vis.setFont('Helvetica-Bold', 12)
        vis.drawString(mm(38), mm(257), dado['Destino'])
        vis.drawString(mm(157), mm(257), 'AGROSUL')
        vis.drawString(mm(38), mm(248), str(dado['Carga ERP']))
        vis.drawString(mm(157), mm(248), '47-3330-5747')
        vis.drawString(mm(38), mm(239), data)
        vis.drawString(mm(38), mm(230), dado['Veículo'])
        vis.setFont('Helvetica-Bold', 8)
        vis.drawString(mm(157), mm(230), dado['Motorista'])

        ##### CONTRUÇÃO DO RELATORIO #####

        # cabeçalho

        vis.drawImage(imagem, mm(10), mm(275), 99, 31)
        vis.drawString(mm(83), mm(278), 'ORDEM DE CARREGAMENTO')
        vis.setLineWidth(0.2)
        vis.line(mm(2), mm(268), mm(205), mm(268))

        # primeiro bloco - dados do roteiro (oc, veiculo, motorista)
        vis.setFont('Helvetica-Bold', 10)
        vis.rect(mm(35), mm(255), mm(50), mm(7))
        vis.drawString(mm(5), mm(257), 'Destino')
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

        ### segundo bloco - avaliação de segurança e meio ambiente - desativado temporariamente
        '''
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
        '''
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
            vis.drawString(mm(147), mm(lin + 2), '')
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

        # vis.drawString(mm(5), mm(75), 'Data: _______/_______/________')
        vis.drawString(mm(110), mm(75), 'Expedidor: __________________________________________')
        vis.drawString(mm(125), mm(76), ' AGROSUL')
        # vis.drawString(mm(5), mm(70), 'Hora: _________________')
        vis.drawString(mm(110), mm(65), 'Responsável pela verificação: _______________________')
        vis.drawString(mm(110), mm(55), 'Motorista: __________________________________________')
        vis.drawString(mm(125), mm(56), dado['Motorista'])
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
    return arqvis


def escalacao(dados):
    escala_df = dados
    # excluir linhas das transportadoras expresso e reunidas
    escala_df = escala_df.drop(escala_df[escala_df['Motorista'] == 'MOTORISTA TRANSPORTADORA'].index)
    escala_df = escala_df.reset_index()  # reseta o indice do dataframe após excluir transportadora
    # gerar DataFrame
    escala = escala_df[['Carga ERP', 'Destino', 'Veículo', 'Motorista', 'Ajudante 1', 'Ajudante 2']]

    linha = len(escala.axes[0])  # contar quantas rotas tem na programação,
    arquivo = 'lib/arquivos/relatorio/programacao/escalacao.pdf'

    # gerar cabecalho da escalação
    alt = 35 + (linha * 20)
    div = canvas.Canvas(arquivo, pagesize=(mm(260), mm(alt)))
    div.setFillColorRGB(0, 0.5, 0.8)  # cor RGB azul escuro
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
    div.drawCentredString(mm(45), mm(alt - 25), 'ROTEIRO')
    div.drawCentredString(mm(115), mm(alt - 25), 'CARRO')
    div.drawCentredString(mm(197), mm(alt - 25), 'COLABORADORES')

    # gerar bloco com a escalação dos roteiros e colaboradores
    linSup = alt - 30
    linInf = alt - 50
    tex = alt - 42
    for cont in range(linha):
        dado = escala.loc[cont]
        ajudante1 = str(dado['Ajudante 1'])
        ajudante2 = str(dado['Ajudante 2'])
        div.setFont('Helvetica-Bold', 20)
        div.setFillColorRGB(0, 1, 1)
        div.rect(mm(5), mm(linInf), mm(250), mm(20), fill=1)
        div.setFillColorRGB(0, 0, 0)
        div.line(mm(5), mm(linSup), mm(5), mm(linInf))  # coluna
        div.line(mm(90), mm(linSup), mm(90), mm(linInf))  # coluna
        div.line(mm(140), mm(linSup), mm(140), mm(linInf))  # coluna
        div.line(mm(255), mm(linSup), mm(255), mm(linInf))  # coluna
        div.line(mm(5), mm(linInf), mm(255), mm(linInf))  # linha inferior
        div.drawString(mm(7), mm(tex), dado['Destino'])
        div.drawCentredString(mm(115), mm(tex), dado['Veículo'])
        div.setFont('Helvetica-Bold', 18)
        if ajudante2 != 'nan':
            div.drawString(mm(143), mm(tex + 6), dado['Motorista'])
            div.drawString(mm(143), mm(tex - 0.5), ajudante1)
            div.drawString(mm(143), mm(tex - 7), ajudante2)
        elif ajudante1 == 'nan':
            div.drawString(mm(143), mm(tex), dado['Motorista'])
        else:
            div.drawString(mm(143), mm(tex + 4), dado['Motorista'])
            div.drawString(mm(143), mm(tex - 6), ajudante1)
        print(f"OC {dado['Carga ERP']} ..... ok!")
        sleep(0.5)
        linSup -= 20
        linInf -= 20
        tex -= 20
    div.save()
    destinoimagem = 'lib/arquivos/relatorio/programacao'
    imagem = pdftojpg(arquivo, destinoimagem)
    return imagem
