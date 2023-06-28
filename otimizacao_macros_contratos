Sub Contratopf()
Application.ScreenUpdating = False

Set objword = CreateObject("word.application")

objword.Visible = True

Set arqcontrato = objword.documents.Open("caminho-do-modelo\ContratoPF.docx")
Set conteudoDoc = arqcontrato.Application.Selection

For i = 1 To 11

    conteudoDoc.Find.Text = Cells(i, 2).Value
    conteudoDoc.Find.Replacement.Text = Cells(i, 3).Value
    conteudoDoc.Find.Execute Replace:=2

Next

If Range("A5").Value <> "RG" And Not IsEmpty(Range("A5").Value) Then
    
    With conteudoDoc.Find
    .Text = "RG"
    .Replacement.Text = Range("A5").Value
    .MatchWholeWord = True
    .Execute Replace:=2
    End With
    
End If

arqcontrato.saveas2 ("caminho-do-contrato\ContratoPF" & Cells(1, 3).Value & ".docx")

arqcontrato.Close
objword.Quit

Set objwork = Nothing
Set arqcontrato = Nothing
Set conteudocontrato = Nothing

Range("C1:C5").ClearContents
Range("C7:C8").ClearContents
Range("D6").ClearContents

Application.ScreenUpdating = True

MsgBox ("Contrato gerado com sucesso!")

End Sub
