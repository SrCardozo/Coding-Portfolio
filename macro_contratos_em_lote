Sub contratos_em_lote()
Application.ScreenUpdating = False

ifinal = Sheets("Dados Cadastrais").Range("A4").End(xlDown).Row

For i = 5 To ifinal
    
    Sheets("Dados Cadastrais").Activate
    
    estado = Cells(i, 15).Value
    emissor = Cells(i, 7).Value
    tipo_doc = Cells(i, 14).Value
    
    Range("B" & i & ":F" & i).Copy
    Sheets("Contrato_PF").Range("C1").PasteSpecial Paste:=xlPasteValues, Transpose:=True
    Range("H" & i & ":L" & i).Copy
    Sheets("Contrato_PF").Range("C7").PasteSpecial Paste:=xlPasteValues, Transpose:=True
    
     If emissor = "SECRETARIA DE SEGURANCA PUBLICA" Then
        Sheets("Contrato_PF").Range("C6").Value = "SSP/" & estado
        
    
    ElseIf emissor = "INSTITUTO FELIX PACHECO" Then
        Sheets("Contrato_PF").Range("C6").Value = "IFP/" & estado
        
    Else
        Sheets("Contrato_PF").Range("C6").Value = ActiveSheet.Cells(i, 7).Value & "/" & estado
        
    End If
    
    If tipo_doc = "REGISTRO GERAL" Then
        Sheets("Contrato_PF").Range("A5").Value = "RG"

        ElseIf tipo_doc = "CARTEIRA NACIONAL DE HABILITACAO" Then
        Sheets("Contrato_PF").Range("A5").Value = "CNH"
        Sheets("Contrato_PF").Range("C6").Value = "DETRAN/" & estado
        
        
        ElseIf tipo_doc = "ORDEM DOS ADVOGADOS DO BRASIL" Then
        Sheets("Contrato_PF").Range("A5").Value = "CARTEIRA OAB"
        Sheets("Contrato_PF").Range("C6").Value = "OAB/" & estado
        
        Else
        Sheets("Contrato_PF").Range("A5").Value = Cells(i, 7).Value
        Sheets("Contrato_PF").Range("C6").Value = Cells(i, 7).Value & "/" & estado
        
    End If
        
    Sheets(1).Activate
    Call Contratopf
    
Next i

MsgBox "Contratos gerados e salvos na pasta!", vbInformation

Application.ScreenUpdating = True
Application.CutCopyMode = False
End Sub
