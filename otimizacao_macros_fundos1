Sub aplicar1()
Dim ifinal As Integer, ult_hist As Integer, i As Integer
Dim encontrado As Boolean, outapp As Object, outmail As Object
Dim endereco As String

'Verificar se há alguma aplicação na planilha
    ifinal = Sheets("Fundos").Cells(Rows.Count, 1).End(xlUp).Row

    encontrado = False
    
    For i = 2 To ifinal
        
        If Cells(i, 5).Value = "Aplicação" Then
            encontrado = True
            Exit For
        End If
        
    Next i
    
    If Not encontrado Then
        MsgBox "Nenhuma aplicação foi encontrada!"
        End
    End If

'Otimizar macro
    With Application
        .ScreenUpdating = False
        .DisplayAlerts = False
        .Calculation = xlCalculationManual
    End With

'Filtrar clientes ok para aplicar
  Sheets("Fundos").Range("A1").AutoFilter Field:=5, Criteria1:="aplicar"
  Sheets("Fundos").Range("A1").AutoFilter Field:=8, Criteria1:="sim"
  Sheets("Fundos").Range("A1").AutoFilter Field:=16, Criteria1:="ativo"

'salvar histórico
  ifinal = Sheets("Fundos").Cells(Rows.Count, 1).End(xlUp).Row
  Sheets("Fundos").Range("a2:f" & ifinal).Copy
  ult_hist = Sheets("Histórico_Fundos").Range("A1").End(xlDown).Row + 1
  Worksheets("Histórico_Fundos").Range("A" & ult_hist).PasteSpecial xlPasteValuesAndNumberFormats

'salvar arquivo de aplicação
  ifinal = Sheets("Fundos").Cells(Rows.Count, 1).End(xlUp).Row
  Sheets("Fundos").Range("a1:f" & ifinal).Copy
  Workbooks.Add
  Sheets(1).Range("A1").Select
  Sheets(1).Range("A1:P1").PasteSpecial Paste:=xlAll
  Sheets(1).Range("A1:P1").PasteSpecial Paste:=xlPasteValues
  Selection.Columns.AutoFit

  ActiveWorkbook.SaveAs Filename:="C:\Users\username\Downloads\VBA\aplicacao.xlsx"
  ActiveWorkbook.Close
  Application.DisplayAlerts = True

'redigir e-mail de aplicação

  Set OutApp = CreateObject("Outlook.Application")
    Set OutMail = OutApp.CreateItem(0)

    endereco = "C:\Users\username\Downloads\VBA\aplicacao.xlsx"

    On Error Resume Next
    With OutMail
        .Display
        .To = "Aplicação <email@dominio.com>"
        .CC = "Farmers <email@dominio.com>"
        .BCC = ""
        .Subject = "Aplicação em fundos - " & Date
        .HTMLBody = "Segue em anexo o aporte." & .HTMLBody
        .Attachments.Add endereco
        .Send
    End With

    On Error GoTo 0

'remover filtros e restaurar configurações da planilha
    Worksheets("Fundos").Range("A1").AutoFilter

     With Application
        .EnableEvents = True
        .ScreenUpdating = True
        .Calculation = xlCalculationAutomatic
    End With   
    
    Set OutMail = Nothing
    Set OutApp = Nothing

    Sucesso = MsgBox("Aplicação enviada com sucesso!", vbInformation)

End Sub
