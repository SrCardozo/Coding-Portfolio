Sub atualizar_dados()
    ' Declarar variáveis
    Dim ult_RF As Long, ult_update As Long, ult_CC As String, ult_fundo As String, caminho1 As String, caminho2 As String
    Dim RF_Custodia2 As String, RF_Custodia1 As String, CC_Custodia1 As String, CC_Custodia2 As String, ult_assessor As Long
    Dim RF As Worksheet, CC As Worksheet, Fundos As Worksheet, clientes As Worksheet, Blacklist As Worksheet
    Dim intervalo As Range, AUM As Workbook, AUM1 As Worksheet, Custodia2 As Workbook, Origem As Worksheet
    Dim ult_auc As Long, ult_cell As Long, ArrayRow As Long, i As Long, j As Long
    Dim combinedRange As Range, individualRange As Range
    Dim ResultArray() As Variant
    
    ' Definir caminhos dos arquivos com base no usuário
    If Environ("USERNAME") = "usuario.um" Then
        caminho1 = "C:\Users\usuario.um\OneDrive\Atualizações\"
        caminho2 = "C:\Users\usuario.um\Documents\"
    ElseIf Environ("USERNAME") = "usuario.dois" Then
        caminho1 = "C:\Users\usuario.dois\One Drive\Atualizações\"
        caminho2 = "C:\Users\usuario.dois\Downloads\"
    End If

    ' Verificar se os arquivos de conta corrente do dia já foram baixados
    CC_Custodia1 = Dir(caminho2 & "Conta Corrente - " & Format(Date, "dd") & " " & Format(Date, "mm") & " " & Year(Date) & "*")
    CC_Custodia2 = Dir(caminho2 & "Lista_Saldos_*")
    If Len(CC_Custodia1) = 0 Then
        MsgBox "O arquivo da conta corrente Custodia1 não está na pasta. Baixe-o ou mova-o para a pasta correspondente e execute a macro novamente", vbExclamation, "ARQUIVO AUSENTE"
        End
    ElseIf Len(CC_Custodia2) = 0 Then
        MsgBox "O arquivo da conta corrente Custodia2 não está na pasta. Baixe-o ou mova-o para a pasta correspondente e execute a macro novamente", vbExclamation, "ARQUIVO AUSENTE"
        End
    End If
    
    ' Desativar atualização da tela
    Application.ScreenUpdating = False

    'Verificar se foi postado um novo arquivo de clientes (AUM) na pasta. Caso não, o código irá pular essa parte para não copiar dados antigos. A macro que verifica o arquivo
      mais recente está após o final desta
    On Error Resume Next
    Set AUM = Workbooks.Open(ArquivoMaisRecenteD2("J:\path\2024\" & Format(Date, "mm")), , True)
    On Error GoTo 0

    ' Definir planilhas
    Set RF = ThisWorkbook.Sheets(2)
    Set CC = ThisWorkbook.Sheets(3)
    Set Fundos = ThisWorkbook.Sheets(4)
    Set clientes = ThisWorkbook.Sheets(5)

    ' Definir nomes dos arquivos
    RF_Custodia1 = "RFCLIENTEDISP WM.csv"
    RF_Custodia2 = "RF_Custodia2.xlsx"
    
    ' Atualizar Posição de Renda Fixa Custodia1
    RF.Range("A1").CurrentRegion.ClearContents
    ' Importar arquivo CSV
    With RF.QueryTables.Add(Connection:="TEXT;" & caminho1 & RF_Custodia1, Destination:=RF.Range("A1"))
        .TextFileParseType = xlDelimited
        .TextFileConsecutiveDelimiter = False
        .TextFileTabDelimiter = False
        .TextFileSemicolonDelimiter = False
        .TextFileCommaDelimiter = True ' Usar True para vírgula como delimitador
        .TextFileSpaceDelimiter = False
        .TextFileColumnDataTypes = Array(1) ' 1 = Texto
        .Refresh
    End With
    ThisWorkbook.Connections("RFCLIENTEDISP WM").Delete
    RF.Range("A:B").Delete
    RF.Range("P:AO").Delete
    RF.Columns("A:A").NumberFormat = "Geral"
    RF.Columns("F:F").NumberFormat = "Geral"
    RF.Columns("H:I").NumberFormat = "m/d/aaaa"
    
    ' Abrir planilha com Posição de Renda Fixa Custodia2
    Workbooks.Open caminho1 & "RF_Custodia2.xlsx", , True
    Set Origem = Workbooks("RF_Custodia2.xlsx").Sheets(1)
    
    ' Copiar comercial papers
    Origem.Range("A:M").AutoFilter Field:=5, Criteria1:="=NC*"
    ult_update = RF.Cells(Rows.Count, 1).End(xlUp).Row + 1
    Call CopiarArrays(ult_update)
    Origem.AutoFilterMode = False
    
    ' Copiar debentures
    Origem.Range("A:M").AutoFilter Field:=4, Criteria1:="Debenture"
    ult_update = RF.Cells(Rows.Count, 1).End(xlUp).Row + 1
    Call CopiarArrays(ult_update)
    Origem.AutoFilterMode = False

    ' Copiar CRIs, CRAs e FIDCs
    Origem.Range("A:M").AutoFilter Field:=4, Criteria1:=Array("Cra", "Cri", "Fidc"), Operator:=xlFilterValues
    ult_update = RF.Cells(Rows.Count, 1).End(xlUp).Row + 1
    ult_RF = Origem.Cells(Rows.Count, 1).End(xlUp).Row
    Call CopiarArrays(ult_update)
    Application.CutCopyMode = False
    Set intervalo = Origem.Range("E2:E" & ult_RF).SpecialCells(xlCellTypeVisible)
    
    ' Redimensionar o array para o tamanho do intervalo visível
    ReDim ResultArray(1 To intervalo.Count, 1 To 1)
    i = 1 ' Inicializar o contador do array
    For Each celula In intervalo
        ' Armazenar o resultado no array
        ResultArray(i, 1) = ExtrairTextoDepois(celula.Value, " ")
        If ResultArray(i, 1) = "" Then
            ResultArray(i, 1) = celula.Value
        End If
        i = i + 1
    Next celula
    RF.Range("F" & ult_update).Resize(UBound(ResultArray, 1), 1).Value = ResultArray
    Application.CutCopyMode = False
    Workbooks(RF_Custodia2).Close False

    ' Atualizar CC Custodia1
    CC.Range("A:M").ClearContents
    Workbooks.Open caminho2 & CC_Custodia1
    ult_CC = Workbooks(CC_Custodia1).Sheets(2).Range("A2").End(xlDown).Row
    Workbooks(CC_Custodia1).Sheets(2).Range("A2:M" & ult_CC).Copy
    CC.Range("A1").PasteSpecial xlPasteValues
    CC.Range("C1").Value = "D0"
    Application.CutCopyMode = False
    Workbooks(CC_Custodia1).Close xlSaveChanges = False

    ' Atualizar CC Custodia2. Essa parte do código exclui os arquivos de conta corrente para não correr o risco de utilizar o mesmo arquivo em próximas atualizações, pois o nome
deste arquivo é sempre o mesmo e a macro busca o arquivo pelo nome
    Workbooks.Open caminho2 & CC_Custodia2
    ult_CC = Workbooks(CC_Custodia2).Sheets(1).Range("A6").End(xlDown).Row
    ult_update = CC.Cells(Rows.Count, 1).End(xlUp).Row + 1
    Workbooks(CC_Custodia2).Sheets(1).Range("A2:C" & ult_CC).Copy
    CC.Range("A" & ult_update).PasteSpecial xlPasteAll
    Application.CutCopyMode = False
    Workbooks(CC_Custodia2).Close xlSaveChanges = False
    Kill caminho2 & CC_Custodia2
    ' Converter números armazenados como texto em números
    Set intervalo = CC.Range("A" & ult_update & ":A" & CC.Cells(Rows.Count, 1).End(xlUp).Row)
    Application.ScreenUpdating = True
    intervalo.TextToColumns Destination:=intervalo, DataType:=xlDelimited, TextQualifier:=xlDoubleQuote, _
                            ConsecutiveDelimiter:=False, Tab:=False, Semicolon:=False, Comma:=False, _
                            Space:=False, Other:=False

    ' Atualizar Fundos. Essa parte de atualizar a posição de fundos é feita por meio do Power Query. Quando mais pessoas passaram a utilizar essa base de dados ficou mais
simples atualizar essa parte dos fundos por meio do Power Query por se tratar de uma junção de vários arquivos, então a macro apenas atualiza as consultas do Power Query
A fórmula é para verificar a qual base de assessor o cliente pertence
   
  ThisWorkbook.RefreshAll
    Fundos.Activate
    Fundos.Cells(Rows.Count, 3).End(xlUp).Select
    ult_assessor = Selection.End(xlUp).Row + 1
    ult_update = Fundos.Cells(Rows.Count, 1).End(xlUp).Row
    Cells(ult_assessor, 3).Formula = "=IFERROR(VLOOKUP([@COD],Clientes!A:D,4,FALSE), ""n/d"")"
    Cells(ult_assessor, 3).AutoFill Destination:=Range("C" & ult_assessor & ":C" & ult_update)

    'Caso não tenha sido encontrado um arquivo de clientes atualizado na pasta, a macro irá pular essa parte e passar para o rótulo fim
    On Error GoTo fim
    ' Atualizar clientes
    Set AUM1 = AUM.Sheets(1)
    clientes.Range("A:F").ClearContents
    AUM1.Range("A1").CurrentRegion.Copy
    clientes.Range("A1").PasteSpecial xlPasteValues
    Application.CutCopyMode = False
    Workbooks(AUM.Name).Close False

fim:
    Sheets(1).Range("A1").Value = "Atualizado em " & Now()
    ThisWorkbook.Save

    ' Atualizar e calcular
Application.Calculate

    ' MsgBox "Atualização concluída!", vbInformation
    ' ThisWorkbook.Close (True)
End Sub
______________________________________________________________________________________________________________________________________________________________________

Function ArquivoMaisRecenteD2(ByVal Diretorio As String) As String
    ' Esta função retorna o caminho do arquivo mais recente em um diretório especificado
    Dim arqSys As Object
    Dim objArq As Object
    Dim minhaPasta As Object
    Dim nomeArq As String
    Dim dataArq As Date, n As Date

    ' Criação do objeto FileSystemObject
    Set arqSys = CreateObject("Scripting.FileSystemObject")
    ' Define a pasta alvo
    Set minhaPasta = arqSys.GetFolder(Diretorio)
    ' Determina a data de dois dias úteis atrás
    dataArq = WorksheetFunction.WorkDay(Date, -2)
    
    ' Iteração sobre todos os arquivos na pasta
    For Each objArq In minhaPasta.Files
        n = FormatDateTime(objArq.datelastmodified, vbShortDate)
        ' Verifica se a data de modificação do arquivo é mais recente que a data determinada
        If n > dataArq Then
            dataArq = objArq.datelastmodified
            nomeArq = objArq.Name
            ' Sai do loop quando encontra o arquivo mais recente
            GoTo fim
        End If
    Next objArq
    
fim:
    ' Libera os objetos da memória
    Set arqSys = Nothing
    Set minhaPasta = Nothing
    ' Retorna o caminho completo do arquivo mais recente
    ArquivoMaisRecenteD2 = Diretorio & "\" & nomeArq
End Function
______________________________________________________________________________________________________________________________________________________________________

Sub CopiarArrays(startRow As Long)
    ' Esta sub-rotina copia dados de um intervalo para arrays e os cola em uma planilha de destino
    Dim ResultArrayA As Variant, ResultArrayB As Variant, ResultArrayC As Variant, ResultArrayD As Variant, ResultArrayE As Variant
    Dim ult_RL As Long
    
    ' Define a planilha de origem e destino
    Set Origem = Workbooks("RF_Custodia2.xlsx").Sheets(1)
    Set Destino = ThisWorkbook.Sheets(2)
    
    ' Determina a última linha da planilha de origem
    ult_RL = Origem.Cells(Rows.Count, 1).End(xlUp).Row
    
    ' Copia e armazena os valores dos intervalos nos arrays correspondentes
    ResultArrayA = CopyRangeToArray(Origem.Range("A2:A" & ult_RL).SpecialCells(xlCellTypeVisible)) ' Código cliente
    ResultArrayB = CopyRangeToArray(Origem.Range("E2:E" & ult_RL).SpecialCells(xlCellTypeVisible)) ' Código produto
    ResultArrayC = CopyRangeToArray(Origem.Range("F2:F" & ult_RL).SpecialCells(xlCellTypeVisible)) ' Valor Atual
    ResultArrayD = CopyRangeToArray(Origem.Range("G2:G" & ult_RL).SpecialCells(xlCellTypeVisible)) ' Quantidade
    ResultArrayE = CopyRangeToArray(Origem.Range("C2:C" & ult_RL).SpecialCells(xlCellTypeVisible)) ' Nome cliente

    ' Cola os arrays na planilha de destino, a partir da linha especificada
    With Destino
        .Range("A" & startRow).Resize(UBound(ResultArrayA, 1), 1).Value = ResultArrayA
        .Range("F" & startRow).Resize(UBound(ResultArrayB, 1), 1).Value = ResultArrayB
        .Range("O" & startRow).Resize(UBound(ResultArrayC, 1), 1).Value = ResultArrayC
        .Range("J" & startRow).Resize(UBound(ResultArrayD, 1), 1).Value = ResultArrayD
        .Range("B" & startRow).Resize(UBound(ResultArrayE, 1), 1).Value = ResultArrayE
    End With
    
End Sub
