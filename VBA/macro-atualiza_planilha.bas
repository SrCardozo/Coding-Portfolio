Sub atualizar_planilha()

'Otimizar macro
Application.ScreenUpdating = False
Application.Calculation = xlCalculationManual

'Declarar variáveis
Dim planilha As Workbook

'Atualizar dados desta planilha e salvar alterações
For n = 10 To 13

    ThisWorkbook.Sheets(n).ListObjects(1).QueryTable.Refresh

Next

ThisWorkbook.Save

'Repetir processo de atualização para outra planilha (também abre e fecha o arquivo)
Set planilha = Workbooks.Open("C:\Users\nome.usuario\caminho\do\arquivo\planilha.xlsm")
planilha.RefreshAll
planilha.Close (True)

'Repetir o processo de atualização para outras duas planilhas, executando uma macro nelas que é semelhante a esta. No caso das macros dessas outras duas planilhas, além de atualizar as conexões elas também registram o horário
  de atualização em um local específico da planilha, para informar aos usuários quando o arquivo foi atualizado (utilizando texto "Atualizado em " + Now()). Após rodar as macros, reseta as configurações do Excel para o padrão

With Application
    .Run "planilha2.xlsm!atualizar_planilha"
    .Run "planilha3.xlsm!atualizar_planilha"
    .Calculation = xlCalculationAutomatic
    .ScreenUpdating = True
End With

'Notifica do término da atualização dos dados
MsgBox "Atualização concluída!", vbInformation
End Sub