from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoAlertPresentException
from pandas import read_excel

#Iniciar navegador na página principal do sistema
navegador = webdriver.Chrome()
navegador.get(r"C:\Users\AMCTE\Downloads\Exercício - Processo de Consulta em sites\index.html")

#Função para abrir consulta de acordo com a cidade
def abrir_consulta(cidade):
    
    navegador.switch_to.window(navegador.window_handles[0])

    ActionChains(navegador).move_to_element(navegador.find_element(By.TAG_NAME, 'button')).perform()
    menu = navegador.find_element(By.CLASS_NAME, 'dropdown-content')
    botao = [elemento for elemento in menu.find_elements(By.TAG_NAME, 'a') if cidade in elemento.text]
    botao[0].click()

    navegador.switch_to.window(navegador.window_handles[1])

#Obter lista dos processos a serem consultados de uma planilha
processos = read_excel(r'C:\Users\AMCTE\Downloads\Exercício - Processo de Consulta em sites/Processos.xlsx')
processos['Status'] = processos['Status'].astype(str)

#Consultar cada processo no site
for row in processos.index:
    abrir_consulta(processos.loc[row, 'Cidade'])
    
    #Preencher formulário com os dados de busca
    navegador.find_element(By.ID, 'nome').send_keys(processos.loc[row, "Nome"])
    navegador.find_element(By.ID, 'advogado').send_keys(processos.loc[row, "Advogado"])
    navegador.find_element(By.ID, 'numero').send_keys(processos.loc[row, "Processo"])

    #Clicar em consultar e confirmar consulta
    navegador.find_element(By.TAG_NAME, 'button').click()
    navegador.switch_to.alert.accept()

    #Atualizar processo na planilha de acordo com o resultado da consulta
    while True:
        try:
            alerta = navegador.switch_to.alert
            
            if 'nenhum processo encontrado' in alerta.text.casefold():
                processos.loc[row, 'Status'] = 'Não encontrado'
            else:
                processos.loc[row, 'Status'] = 'Encontrado'
            alerta.accept()
            break
        except NoAlertPresentException:
            continue
    
    #Fechar consulta
    navegador.close()

#Salvar nova planilha com status dos processos
processos.to_excel(r'C:\Users\AMCTE\Downloads\Status_Processos.xlsx', index=False)