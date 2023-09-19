Sub reservas()

Dim planilhaAberta As Workbook, planilhaDestino As Worksheet, planilhaOrigem As Worksheet
Dim linhaDestino As Integer, linha As Integer, col As Integer, last_row As Integer, planilha As Integer, linha_colagem As Integer
Dim anexo As String

'Ativa a planilha atual para executar a macro
ThisWorkbook.Activate

'Pergunta ao usuário se ele deseja enviar um produto específico. Caso positivo, a macro irá pedir o nome do produto e compilar os dados somente da coluna do respectivo _ 
produto informado; caso negativo a macro irá compilar dados de todos os produtos da planilha que tenham reserva e o usuário clique em cancelar a macro irá interromper a execução do código

envio = MsgBox("Deseja enviar algum produto específico?", vbQuestion + vbYesNoCancel, "Confirmação")

'Abre um campo para o usuário digitar qual produto deseja enviar, caso tenha informado que deseja enviar um produto específico
If envio = vbYes Then
    produto = InputBox("Digite o nome do produto que deseja enviar:", "Produto")

    ElseIf envio = vbCancel Then
        End

End If

'Interrompe a execução da macro caso o usuário tenha clicado em cancelar na input box
If produto = vbCancel Then
    End
End If

'Identifica se o arquivo de reservas já está aberto. Caso não esteja ele irá abrir o arquivo, limpar os dados (exceto o cabeçalho) e definir a primeira linha de colagem como a linha 2 (pois a linha 1 é o cabeçalho). Também ativa a planilha atual _
  para continuar a execução da macro. Caso a planilha já esteja aberta, ele identifica se a planilha já contém algum dado... se estiver vazia, a primeira linha de colagem será a linha 2, se não estiver vazia a linha de colagem será a primeira linha  _
  após a última linha preenchida
  
If IsWorkBookOpen("Reservas.xlsx") = False Then

    ' Abre a planilha de colagem
    Set planilhaAberta = Workbooks.Open("C:\Users\" & Environ("username") & "\Documents\Reservas.xlsx")
    Set planilhaDestino = planilhaAberta.Sheets(1)
    last_row = ActiveSheet.Range("A1").End(xlDown).Row
    ActiveSheet.Range("A2:F" & last_row).ClearContents
    ThisWorkbook.Activate
    linha_colagem = 2

Else

    Set planilhaAberta = Workbooks("Reservas.xlsx")
    Set planilhaDestino = planilhaAberta.Sheets(1)
    If planilhaAberta.Sheets(1).Range("A2").Value = "" Then
      linha_colagem = 2
    Else
      linha_colagem = planilhaAberta.Sheets(1).Range("A1").End(xlDown).Row + 1
    End If

End If

'Percorre a planilha de cada assessor, ativando cada uma para extrair os dados
For planilha = 1 To 3
  Worksheets(planilha).Activate
  ult_reserva = ActiveSheet.Range("A1").End(xlDown).Row
  col_reservas = Application.Match("RESERVAS", ActiveSheet.Rows(1), 0)

  'Se o usuário tiver definido para enviar um produto específico, a primeira e a última coluna serão a mesma, que será igual à coluna referente ao produto informado _
    Caso não, a primeira e a última coluna serão definidas por seus nomes, e a macro irá extrair dados de todas as colunas contidas nesse intervalo, independente de se adicionar, _
    renomear ou excluir colunas

  If envio = vbYes Then
      prim_coluna = Application.Match(produto, ActiveSheet.Rows(1), 0)
      ult_coluna = Application.Match(produto, ActiveSheet.Rows(1), 0)
  
      Else
      prim_coluna = Application.Match("DIRETAS", ActiveSheet.Rows(1), 0) + 1
      ult_coluna = col_reservas - 1
  
  End If
  
  'Localizar a coluna de onde será copiada a custódia do cliente 
  custodia = Application.Match("Custódia", ActiveSheet.Rows(1), 0)
  
  'Percorrer cada linha da planilha
      For linha = 2 To ult_reserva
  
          'Verifica se o cliente tem alguma reserva, em uma coluna que soma os valores contidos nas colunas do intervalo verificado
          If Cells(linha, col_reservas).Value = 0 Then
  
          GoTo ProximaLinha
  
          Else 'Caso o cliente tenha reserva, a macro percorre cada coluna coluna de cada produto para verificar de qual produto o cliente tem reserva, _
                e salva os dados da reserva em outro arquivo
              For col = prim_coluna To ult_coluna
  
              'Verifica se o cliente tem reserva do produto
                  If IsEmpty(Cells(linha, col).Value) = True Then
  
                  GoTo ProximoProduto
  
                  Else ''Cola' os dados da reserva na planilha modelo, através de atribuição de valores
  
                      planilhaDestino.Cells(linha_colagem, 1).Value = ActiveSheet.Cells(linha, 1).Value
                      planilhaDestino.Cells(linha_colagem, 2).Value = ActiveSheet.Cells(linha, 2).Value
                      planilhaDestino.Cells(linha_colagem, 3).Value = ActiveSheet.Name
                      planilhaDestino.Cells(linha_colagem, 4).Value = ActiveSheet.Cells(1, col).Value
                      planilhaDestino.Cells(linha_colagem, 5).Value = ActiveSheet.Cells(linha, col).Value
                      planilhaDestino.Cells(linha_colagem, 6).Value = ActiveSheet.Cells(linha, custodia).Value
  
                      linha_colagem = linha_colagem + 1
                  End If

'Para sair dos loops quando as condições verificadas forem false, utilizei rótulos na macro e o comando GoTO
  ProximoProduto:
              Next
  
              End If
  
  ProximaLinha:
          Next

Next

End Sub
