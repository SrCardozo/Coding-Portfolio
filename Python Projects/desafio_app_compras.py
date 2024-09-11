# %%writefile compras.py  -> salvar como arquivo .py

import json as js, time, os
from pathlib import Path


def adicionar_item(compras, item, quantidade):
    compras[item] = quantidade


def remover_item(compras, item):
    del compras[item]


def visualizar_compras(compras):
    for item in compras:
        print(f'{item}: {compras[item]}')
    print('\nPressione enter para continuar')
    input()


def salvar_compras(compras, nome_arquivo):
    with open(f'C:/Users/AMCTE/Downloads/Listas/{nome_arquivo}', 'w') as arquivo:
        js.dump(compras, arquivo)


def carregar_compras(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        return js.loads(arquivo.read())



def gerenciar_compras(compras, nome_arquivo=None):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(1, 'Adicionar item')
        print(2, 'Remover item')
        print(3, 'Visualizar lista')
        print(4, 'Salvar e sair')
        print(5, 'Sair sem salvar')

        opcao = input('Escolha uma opção:')

        if opcao == '1':
            item = input('Digite o nome do item:')
            qtd = int(input('Digite a quantidade:'))
            adicionar_item(compras, item, qtd)

        elif opcao == '2':
            item = input('Digite o nome do item:')
            remover_item(compras, item)

        elif opcao == '3':
            visualizar_compras(compras)

        elif opcao == '4':
            if nome_arquivo is None:
                salvar_nome = input('Digite o nome do arquivo para salvar:')

                if not salvar_nome.endswith('.json'):
                    salvar_nome += '.json'
            else:
                salvar_nome = nome_arquivo

            salvar_compras(compras, salvar_nome)
            break

        elif opcao == '5':
            break

        else:
            print('Opção inválida!')
            time.sleep(1)

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(1, 'Criar uma nova lista de compras')
        print(2, 'Carregar uma lista existente')
        print(3, 'Sair')

        opcao = input('Escolha uma opção:')

        if opcao == '1':
            compras = {}
            gerenciar_compras(compras)

        elif opcao == '2':
            print('\nListas disponíveis:')
            listas = [arquivo for arquivo in list(Path('C:/Users/AMCTE/Downloads/Listas').iterdir()) if arquivo.name.endswith('.json')]

            if not listas:
                print('Nenhuma lista encontrada')
                time.sleep(2)
                continue
            else:
                for i, lista in enumerate(listas):
                    print(i + 1, lista.name)
                print('\n')
                escolha = int(input('Escolha uma lista para carregar (0 se nenhuma):'))

                if 0 > escolha or escolha > len(listas):
                    print('Opção inválida!')
                    time.sleep(1)
                    continue

                if escolha == 0:
                    continue

                arquivo = listas[escolha - 1]
                compras = carregar_compras(arquivo)
                gerenciar_compras(compras, arquivo.name)

        elif opcao == '3':
            break

        else:
            print('Opção inválida!')
            time.sleep(1)


if __name__ == '__main__':
    os.system('cls')
    main()