Sub enviar_reservas()

'Otimiza a macro desabilitando atualização de tela e definindo o cálculo das fórmulas como manual
Application.ScreenUpdating = False
Application.Calculation = xlCalculationManual

'Executa a macro de reservas na planilha de cada assessor
Application.Run "planilha_1.xlsm!reservas"
Application.Run "planilha_2.xlsm!reservas"
Application.Run "planilha_3.xlsm!reservas"

'Salva e fecha o arquivo de reservas
Workbooks("RESERVAS.xlsx").Close SaveChanges:=True

'Define o caminho do anexo
anexo = "C:\Users\" & Environ("username") & "\Desktop\RESERVAS.xlsx"

'Cria o e-mail de reservas, anexa o arquivo e envia o e-mail
Set outapp = CreateObject("Outlook.Application")
Set outmail = outapp.CreateItem(0)
 
On Error Resume Next
With outmail
    .Display
    .To = "email@dominio.com"
    .CC = "email@dominio.com"
    .BCC = ""
    .Subject = "Reservas - " & Date & " " & produto
    .HTMLBody = "Segue em anexo as reservas." & .HTMLBody
    .Attachments.Add anexo
    .send
End With

On Error GoTo 0

'Restaura configurações feitas no início da macro para o padrão
Application.ScreenUpdating = True
Application.Calculation = xlCalculationAutomatic

 'Ativa a planilha atual e avisa quando a macro terminar de rodar
ThisWorkbook.Activate
MsgBox "Reservas enviadas!", vbInformation

End Sub
