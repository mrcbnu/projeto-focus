from lib.interface.cores import cor
from lib.interface.valida import leiaInt


def linha(s, x=80, cr=0):
    print(f'{cor(cr)}{s}'*x, f'{cor(0)}')


def cabecalho(x, msg):
    linha(x, cr=7)
    print('{}{}{}'.format(cor(11), msg.center(60), cor(0)))
    linha(x, cr=7)


def menu(lst, msg):
    cabecalho('-', msg)
    while True:
        op = 1
        for val in lst:
            print(f'{cor(7)}[{op}] {val}{cor(0)} ', end='')
            op += 1
        print()
        linha('-', cr=7)
        resp = leiaInt(f'{cor(13)}Escolha sua opção{cor(0)} ')
        if resp > len(lst):
            print(f'{cor(3)}Opção inválida{cor(0)}')
        else:
            break
    return resp

