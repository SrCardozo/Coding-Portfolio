from selenium import webdriver
from selenium.webdriver.common.by import By
from pandas import read_excel
from time import sleep

#abrir navegador no modo de navegação segura
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--safebrowsing-enable-standard-protection')
navegador = webdriver.Chrome(options=chrome_options)

#navegar até a página de login e logar no sistema de emissão de NF
navegador.get(r"C:\Users\AMCTE\Downloads\Exercício - Automatizar Emissão de Nota Fiscal\login.html")
navegador.find_element(By.XPATH, '/html/body/div/form/input[1]').send_keys('usuario')
navegador.find_element(By.XPATH, '/html/body/div/form/input[2]').send_keys('senha')
navegador.find_element(By.TAG_NAME, 'button').click()

#Importar e tratar informações de preenchimento
dados = read_excel(r'C:\Users\AMCTE\Downloads\Exercício - Automatizar Emissão de Nota Fiscal\NotasEmitir.xlsx')
dados = dados[['Cliente', 'Endereço', 'Bairro', 'Municipio', 'CEP', 'CPF/CNPJ',  
'Inscricao Estadual', 'Descrição', 'Quantidade', 'Valor Unitario', 'Valor Total', 'UF']]

#Gerar NF para cada cliente da base de dados
for row in dados.index:
    for i in range(11):
        valor = str(dados.iloc[row, i])
        navegador.find_element(By.XPATH, f'/html/body/div/form/input[{i+1}]').clear()
        navegador.find_element(By.XPATH, f'/html/body/div/form/input[{i+1}]').send_keys(valor)

    navegador.find_element(By.XPATH, '/html/body/div/form/select').send_keys(dados.loc[row, 'UF'])
    navegador.find_element(By.TAG_NAME, 'button').click()

#pausa para baixar o último arquivo antes de fechar o navegador
sleep(5)