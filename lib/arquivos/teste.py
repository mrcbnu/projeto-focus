        cont = 0
        for p in arq:
            cont += 1
        alt = 35 + (cont * 20)
        #div = canvas.Canvas(arquivo, pagesize=(737, 439.4))
        div = canvas.Canvas(arquivo, pagesize=(mm(260), mm(alt)))
        div.setFillColorRGB(0, 0.5, 0.80)  # cor RGB azul escuro
        div.rect(mm(5), mm(alt - 30), mm(250), mm(15), fill=1)  # retangulo fundo azul escuro
        div.setLineWidth(1.5)  # espessura da linha
        div.setFont('Helvetica-Bold', 25)  # fonte e tamanho
        div.setFillColorRGB(0, 0, 0)
        div.drawCentredString(mm(130), mm(alt - 9), 'PROGRAMAÇÃO DE VIAGEM')
        div.line(mm(5),   mm(alt - 15), mm(255), mm(alt - 15))  # primeira linha
        div.line(mm(5),   mm(alt - 30), mm(5),   mm(alt - 15))  # primeira coluna
        div.line(mm(90),  mm(alt - 30), mm(90),  mm(alt - 15))  # segunda coluna
        div.line(mm(140), mm(alt - 30), mm(140), mm(alt - 15))  # terceira coluna
        div.line(mm(255), mm(alt - 30), mm(255), mm(alt - 15))  # quarta coluna
        div.line(mm(5),   mm(alt - 30), mm(255), mm(alt - 30))  # segunda linha
        div.setFillColorRGB(255, 255, 255)  # cor que o proximo texto vai assumir - branco
        div.drawCentredString(mm(45), mm(alt - 27), 'ROTEIRO')
        div.drawCentredString(mm(115), mm(alt - 27), 'CARRO')
        div.drawCentredString(mm(197), mm(alt - 27), 'COLABORADORES')

        linSup = alt - 30
        linInf = alt - 50
        tex = alt - 45

#div = canvas.Canvas(arquivo, pagesize=(737, 439.4))
        div = canvas.Canvas(arquivo, pagesize=(mm(260), mm(155)))
        div.setFillColorRGB(0, 0.5, 0.80)  # cor RGB azul escuro
        div.rect(mm(5), mm(125), mm(250), mm(15), fill=1)  # retangulo fundo azul escuro
        div.setLineWidth(1.5)  # espessura da linha
        div.setFont('Helvetica-Bold', 25)  # fonte e tamnanho
        div.setFillColorRGB(0, 0, 0)
        div.drawCentredString(mm(130), mm(145), 'PROGRAMAÇÃO DE VIAGEM')
        div.line(mm(5),   mm(140), mm(255), mm(140))  # primeira linha
        div.line(mm(5),   mm(140), mm(5),   mm(125))  # primeira coluna
        div.line(mm(90),  mm(140), mm(90),  mm(125))  # segunda coluna
        div.line(mm(140), mm(140), mm(140), mm(125))  # terceira coluna
        div.line(mm(255), mm(140), mm(255), mm(125))  # quarta coluna
        div.line(mm(5),   mm(125), mm(255), mm(125))  # segunda linha
        div.setFillColorRGB(255, 255, 255)  # cor que o proximo texto vai assumir - branco
        div.drawCentredString(mm(45), mm(129), 'ROTEIRO')
        div.drawCentredString(mm(115), mm(129), 'CARRO')
        div.drawCentredString(mm(197), mm(129), 'COLABORADORES')

        linSup = 125
        linInf = 105
        tex = 109