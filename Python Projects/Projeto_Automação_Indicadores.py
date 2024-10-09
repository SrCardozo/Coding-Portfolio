'''
Planejamento do projeto

#1 - Verificar os arquivos e dados que vou precisar (análise preliminar dos dados)
#2 - Importar todas as bibliotecas necessárias
#3 - Importar e tratar dados
#4 - Fazer loop para criar pastas e planilhas de backup das vendas
#5 - No mesmo loop, calcular os indicadores para cada loja e enviar o e-mail para o respectivo gerente
#6 - Criar ranking de faturamento e enviar e-mail para a diretoria

'''

#------------------------- Importação de Bibliotecas ---------------------


#Importar bibliotecas e definir caminho dos arquivos
import pandas as pd, win32com.client as win32
from tqdm import tqdm
from pathlib import Path
from datetime import datetime as dt, timedelta

caminho = r'C:\Users\AMCTE\OneDrive\Documentos\Python\Projeto AutomacaoIndicadores'


#---------------------------- Funções Auxiliares ------------------------------------

def calcular_indicador(vendas: pd.DataFrame, loja: str, periodo: str):
    '''Função para calcular os três indicadores para cada loja e para cada período, de acordo com os argumentos fornecidos. A função não retorna nada, apenas calcula os indicadores. Caso o dataframe de vendas esteja vazio, os indicadores serão definidos como zero por padrão

        Parameters
        ----------
        vendas: DataFrame do pandas\n
            O DataFrame que contém os dados das vendas (se for diário, já deve vir filtrado).

        loja: str\n
            A loja para a qual o indicador será calculado

        periodo: str\n
            O período que o indicador será calculado. Deve ser um dos valores 'diario' ou 'anual'
    '''

    if periodo == 'diario' or periodo == 'anual':
        indicadores[periodo]['faturamento'][loja] = vendas['Valor Final'].sum().item() if not vendas.empty else 0
        indicadores[periodo]['diversificação'][loja] = vendas['Produto'].nunique() if not vendas.empty else 0
        indicadores[periodo]['ticket médio'][loja] = (round(vendas['Valor Final'].sum() / vendas['Quantidade'].sum(), 2)).item() if not vendas.empty else 0
    else:
        raise Exception('Argumento inválido fornecido! Insira somente "diario" ou "anual" para o período')



def definir_cenario(valor, meta):
    """
    Retorna um ícone HTML que indica o cenário atual em relação à meta.

    A função compara um valor com a meta correspondente e retorna uma seta verde para indicar que o valor atingiu ou superou
    a meta, ou uma seta vermelha para indicar que o valor está abaixo da meta.

    Parâmetros
    ----------
    valor : float
        O valor atual do indicador.
    meta : float
        O valor da meta a ser comparada.

    Retorna
    -------
    str
        Uma string HTML contendo uma seta verde para cima (se o valor for maior ou igual à meta) ou uma seta vermelha para baixo
        (se o valor for menor que a meta).
    """
    if valor >= meta:
        return '<font color=green>▲</font>'  # Seta para cima (indicador positivo)
    else:
        return '<font color=red>▼</font>'  # Seta para baixo (indicador negativo)



def dict_para_html(loja: str, periodo: str) -> str:
  """
    Converte os dados de indicadores e metas de uma loja para uma tabela HTML formatada.

    A função recebe o nome de uma loja e um período (diário ou anual) e gera uma tabela HTML que exibe os indicadores da loja,
    as metas correspondentes e o cenário atual em comparação às metas. Os dados são preenchidos a partir de dicionários globais
    de indicadores e metas, aplicando formatação monetária e comparação com metas.

    Parâmetros
    ----------
    loja : str
        O nome da loja para a qual os indicadores serão exibidos.
    periodo : str
        O período a ser considerado para os indicadores ('diario' ou 'anual').

    Retorna
    -------
    str
        Uma string contendo a representação da tabela em HTML com os indicadores, metas e cenários.
    """
  
  if loja in df_lojas['Loja'].values and (periodo == 'diario' or periodo == 'anual'):
    per = 'Dia' if periodo == 'diario' else 'Ano'
    # Criar tabela html
    tabela_html = '<table border="1" cellpadding="5" cellspacing="0">'
    tabela_html += '<thead><tr>'

    # Adicionar os cabeçalhos da tabela
    tabela_html += '<th>Indicador</th>'
    tabela_html += f'<th>Valor {per}</th>'
    tabela_html += f'<th>Meta {per}</th>'
    tabela_html += f'<th>Cenário {per}</th></tr></thead><tbody>'

    # Preencher a tabela com os valores dos indicadores
    for indicador in indicadores[periodo]:
      tabela_html += '<tr>'
      tabela_html += f'<td>{indicador.title()}</td>'
      tabela_html += f'<td>{cur(indicadores[periodo][indicador][loja])}</td>'
      tabela_html += f'<td>{cur(metas[periodo][indicador])}</td>'
      tabela_html += f'<td>{definir_cenario(indicadores[periodo][indicador][loja], metas[periodo][indicador])}</td>'
      tabela_html += '</tr>'

    tabela_html += '</tbody></table>'
    return tabela_html

  else:
    raise Exception('Argumento inválido fornecido para a função!')
  


#Função lambda para formatar números no padrão brasileiro
cur = lambda num: f'{num:,}'.replace('.', '_').replace(',', '.').replace('_', ',')



def ranking_para_html(dicionario: dict) -> str:
    """
    Função para converter um dicionário ordenado em uma tabela de HTML formatada.

    Recebe um dicionário onde as chaves representam os nomes das lojas e os valores representam os
    respectivos faturamentos. A função gera uma string HTML contendo uma tabela com duas colunas: "Loja" e "Faturamento",
    com uma linha para cada entrada no dicionário.

    Parâmetros
    ----------
    dicionario : dict
        Um dicionário no formato {loja: faturamento}, onde cada chave é o nome de uma loja e o valor é o faturamento.

    Retorna
    -------
    str
        Uma string contendo a representação da tabela em HTML.
    """

    tabela_html = '<table border="1" cellpadding="5" cellspacing="0">'
    tabela_html += '<thead><tr>'

    # Adicionar os cabeçalhos da tabela
    tabela_html += '<th>Loja</th>'
    tabela_html += '<th>Faturamento</th></tr></thead><tbody>'

    # Preenche a tabela com os valores
    for loja in dicionario:
        tabela_html += '<tr>'
        tabela_html += f'<td>{loja}</td>'
        tabela_html += f'<td>{cur(dicionario[loja])}</td>'
        tabela_html += '</tr>'

    tabela_html += '</tbody></table>'
    return tabela_html



#--------------------------- Importação e Tratamento de Dados --------------------------------

#Importação das planilhas
df_vendas = pd.read_excel(f'{caminho}/Bases de Dados/Vendas.xlsx')
df_emails = pd.read_excel(f'{caminho}/Bases de Dados/Emails.xlsx')
df_lojas = pd.read_csv(f'{caminho}/Bases de Dados/Lojas.csv', encoding='cp1252', sep=';')


#Dicionário de metas
metas = {
    'diario': {
        'faturamento': 1000,
        'ticket médio': 500,
        'diversificação': 4
    },
    'anual': {
        'faturamento': 1650000,
        'ticket médio': 500,
        'diversificação': 120
    }
}

#Dicionário de indicadores
indicadores = {
    'diario': {
        'faturamento': {},
        'ticket médio': {},
        'diversificação': {}
    },
    'anual': {
        'faturamento': {},
        'ticket médio': {},
        'diversificação': {}
    }
}



#------------------------------- Execução do Programa ----------------------------------

#Obter data mais recente do arquivo
latest_date = max(df_vendas['Data'])
data_completa = latest_date.strftime('%d/%m/%y')
data_abreviada = latest_date.strftime('%d/%m')



    #------------ Cálculo de Indicadores e Envio de E-mails (Gerentes)--------------

#Inserir barra de progresso para monitoramento da execução do loop
pbar = tqdm(total=len(df_lojas['ID Loja']), position=0, leave=True)

outlook = win32.Dispatch('outlook.application')

for loja in df_lojas['ID Loja']:
  pbar.update()

  #Filtrar vendas por loja e por data para calcular os indicadores
  nome_loja = df_lojas.loc[df_lojas['ID Loja'] == loja, 'Loja'].item()
  vendas_ano = df_vendas[df_vendas['ID Loja'] == loja]
  vendas_dia = vendas_ano[vendas_ano['Data'] == latest_date]

  calcular_indicador(vendas_dia, nome_loja, 'diario')
  calcular_indicador(vendas_ano, nome_loja, 'anual')
  
  #Salvar backup das vendas para cada loja. Se não existir uma pasta para a loja, será criada uma
  try:
    Path(f'{caminho}/Backup Arquivos Lojas/{nome_loja}').mkdir()
  except:
    pass
  vendas_ano.to_excel(f'{caminho}/Backup Arquivos Lojas/{nome_loja}/Vendas {nome_loja} - {latest_date.date()}.xlsx')

  #Enviar e-mail para os gerentes
  gerente, email_gerente = df_emails.loc[df_emails['Loja'] == nome_loja, ['Gerente', 'E-mail']].squeeze()


  mail = outlook.CreateItem(0)
  mail.display()
  mail.To = email_gerente
  mail.Subject = f'OnePage Dia {data_completa} - Loja {nome_loja}'
  mail.HTMLBody = f'''
Bom dia, {gerente}!<br><br>

O resultado de ontem (dia {data_abreviada}) da loja {nome_loja} foi:<br><br>

{dict_para_html(nome_loja, 'diario')}
<br><br>

{dict_para_html(nome_loja, 'anual')}
<br>

Segue em anexo a planilha com todos os dados para mais detalhes.<br>
Qualquer dúvida, estou à disposição.<br><br>

Atenciosamente,<br>
Fulano
'''
  anexo  = fr'{caminho}\Backup Arquivos Lojas\{nome_loja}\Vendas {nome_loja} - {latest_date.date()}.xlsx'
  mail.Attachments.Add(anexo)
  mail.Send() #Descomente esta linha para enviar o e-mail automaticamente

pbar.close()



    #-------------- Rankings de Faturamento e E-mail Diretoria -------------

#Criar rankings de faturamento e verificar as melhores e piores lojas do dia e do ano
ranking_dia = dict(sorted(indicadores['diario']['faturamento'].items(), key=lambda item: item[1], reverse=True))
ranking_ano = dict(sorted(indicadores['anual']['faturamento'].items(), key=lambda item: item[1],reverse=True))

# Identificação de melhor e pior valores considerando valores mínimos e máximos repetidos:
# Aqui, para cada loja no ranking diário e anual, é feita uma verificação se o faturamento dela é igual ao maior ou menor valor do ranking.
# Isso permite identificar todas as lojas que têm o melhor e o pior desempenho, mesmo que existam múltiplos valores máximos ou mínimos.
melhor_diario = [loja for loja, faturamento in ranking_dia.items() if faturamento == max(ranking_dia.values())]
pior_diario = [loja for loja, faturamento in ranking_dia.items() if faturamento == min(ranking_dia.values())]

melhor_anual = [loja for loja, faturamento in ranking_ano.items() if faturamento == max(ranking_ano.values())]
pior_anual = [loja for loja, faturamento in ranking_ano.items() if faturamento == min(ranking_ano.values())]

#Enviar e-mail para a diretoria
mail2 = outlook.CreateItem(0)
mail2.To = df_emails.loc[df_emails['Gerente'] == 'Diretoria', 'E-mail'].item()
mail2.Subject = f'Desempenho Lojas - {data_completa}'

# Construção do corpo do e-mail para a diretoria em HTML, formatado para incluir os rankings diário e anual das lojas.
# O ranking é inserido diretamente como uma tabela HTML utilizando a função 'ranking_para_html'
# O e-mail destaca as melhores e piores lojas com base no faturamento, personalizando a mensagem conforme o número de lojas identificadas (singular ou plural).
mail2.HTMLBody = f'''
Prezados, bom dia!<br><br>
Segue abaixo os rankings diário e anual do faturamento das lojas (ranking diário referente ao dia {data_abreviada}):

<h3>Ranking Diário:</h3>
{ranking_para_html(ranking_dia)}<br>

{"As melhores lojas do dia foram" if len(melhor_diario) > 1 else "A melhor loja do dia foi"} <b>{", ".join(melhor_diario)}</b>, com <b>R${cur(max(ranking_dia.values()))}</b> de faturamento,
e {"as piores do dia foram" if len(pior_diario) > 1 else "a pior do dia foi"} {", ".join(pior_diario)}, com R${cur(min(ranking_dia.values()))} de faturamento.<br><br>

<h3>Ranking Anual:</h3>
{ranking_para_html(ranking_ano)}<br>

{"Atualmente as melhores lojas do ano são" if len(melhor_anual) > 1 else "Atualmente a melhor loja do ano é"} <b>{", ".join(melhor_anual)}</b>, com <b>R${cur(max(ranking_ano.values()))}</b> de faturamento,
e {"as piores do ano são" if len(pior_anual) > 1 else "a pior do ano é"} {", ".join(pior_anual)}, com R${cur(min(ranking_ano.values()))} de faturamento.<br>

Qualquer dúvida, estou à disposição.<br><br>

Atenciosamente,<br>
Fulano
'''
mail2.Send() #Descomente esta linha para enviar o e-mail automaticamente

print('Programa executado com sucesso!')
#----------------------------------------------- Fim do Código ----------------------------------------------