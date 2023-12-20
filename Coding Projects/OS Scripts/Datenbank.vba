VBA Code


Option Compare Database
Option Explicit

Sub InsertIntoX1()
    Dim dbs As DAO.Database

    dbs.Execute "INSERT INTO U_T_Bodenprobe " & _
                    "SELECT * Proben_Nr FROM [T_Probennahme]"
                    "WHERE Zweck_Probennahme = 'Bodenprobe_Schlaemmen';
    dbs.Close
End Sub



Private Sub Bezeichnungsfeld37_Click()

End Sub

Private Sub btnEditDateiEndung_Click()
   DoCmd.OpenForm "F_DateiEndung", , , , , acDialog
End Sub

Private Sub btnEinlesen1_Click()
  If MsgBox("Wollen Sie alle Dateien des Ordners als Link speichern??", vbQuestion + vbYesNo, "Links von Dateien speichern") = vbYes Then
     Call OrdnerEinlesen
  End If
End Sub

Private Sub btnEinlesenSingle_Click()
' Menue: Extras -> Verweise Microsoft Office yy.x Object Library
'                           muss aktiv sein!
    Dim fDialog As Office.FileDialog 'ab 2007 muss es Office.Filedialog heissen
    Dim i       As Long
    Dim rs As DAO.Recordset
    Dim db As DAO.Database
    Set db = CurrentDb
    Set rs = db.OpenRecordset("T_Dateien", dbOpenDynaset)

    Set fDialog = Application.FileDialog(msoFileDialogFilePicker)
    With fDialog
        .Filters.Clear
        .Filters.Add "Dokumente", "*.doc; *.xls", 1
        .Filters.Add "Bilder", "*.jpg; *.jpeg; *.bmp; *.tif", 2
        .Filters.Add "Sounds", "*.wav; *.mp3", 3
        .Filters.Add "Alle", "*.*", 4
        .AllowMultiSelect = True
        .Title = "Bitte Datei wählen"
'           .InitialFileName = Application.CurrentProject.Path & "\"
           .InitialFileName = Nz(Me.Parent!txtOrdnerpfad, "")
        .InitialView = msoFileDialogViewDetails
        .ButtonName = "In FotoLink übernehmen"
        .Show
        If .SelectedItems.Count > 0 Then
            For i = 1 To .SelectedItems.Count
                 rs.AddNew
                 rs!DokuLink = .SelectedItems(i)
                 rs!DokuName = Mid(.SelectedItems(i), InStrRev(.SelectedItems(i), "\"))
                 rs.Update
            Next i
          Else
'            MsgBox "kein Pfad ausgewählt."
        End If
    End With
    Me.Requery
End Sub

Private Sub btnLoescheMultiselected_Click()
   Dim sSQL    As String
   Dim varElem As Variant
   If MsgBox("Wollen Sie den angewählten Datensatz unwiderbringbar aus der Tabelle löschen?", vbQuestion + vbYesNo, _
                   "Datensatz löschen") = vbYes Then
                 sSQL = "DELETE FROM T_Dateien " & _
                             "WHERE doku_id =" & Me!Doku_id
                On Error Resume Next
                CurrentDb.Execute sSQL, dbFailOnError
        Me.Requery
   End If
End Sub

Private Sub btnSchliessen_Click()
   DoCmd.Close
End Sub

Private Sub btnTabelle_löschen_Click()
   If MsgBox("Wollen Sie die komplette Tabelle unwiderbringbar löschen?", vbQuestion + vbYesNo, _
                    "Datensatz löschen") = vbYes Then
        DoCmd.SetWarnings False
        DoCmd.RunSQL "DELETE FROM T_Dateien"
        DoCmd.SetWarnings True
        Me.Requery
    End If
End Sub

Sub OrdnerEinlesen()
    Dim objOrdner As Object
    Dim objFile As Object
    Dim fso As Object
    Dim rs As DAO.Recordset
    Dim db As DAO.Database
    Set db = CurrentDb
    Set rs = db.OpenRecordset("T_Dateien", dbOpenDynaset)
    Set fso = CreateObject("Scripting.FileSystemObject")
            If Me.Parent!txtOrdnerpfad <> "\" Then
               If Me!cbxDateiEndung.Column(1) <> "" Then
                    Set objOrdner = fso.GetFolder(Me.Parent!txtOrdnerpfad)
                    For Each objFile In objOrdner.Files
                         If InStr(1, objFile.Name, Me!cbxDateiEndung.Column(1)) > 0 Then
                             rs.AddNew

                             rs!DokuLink = objOrdner & "\" & objFile.Name
                             rs!DokuName = objFile.Name
                             rs.Update
                         End If
                    Next objFile
                 Else
                    Set objOrdner = fso.GetFolder(Me.Parent!txtOrdnerpfad)
                    For Each objFile In objOrdner.Files
                             rs.AddNew
                             rs!DokuLink = objOrdner & "\" & objFile.Name
                             rs!DokuName = objFile.Name
                             rs.Update
                    Next objFile
                End If
             Else
                MsgBox "Kein Ordnerpfad gewählt"
            End If
    Set db = Nothing
    rs.Close
    Set rs = Nothing
    Set objOrdner = Nothing
    Me.Requery
End Sub

Private Sub btnStartpfadBilder_Click()
' Menue: Extras -> Verweise Microsoft Office yy.x Object Library
'                           muss aktiv sein!
    Dim fDialog As Office.FileDialog 'ab 2007 muss es Office.Filedialog heissen
    Dim db      As DAO.Database
    Dim rs      As DAO.Recordset
    Dim i       As Long
    Set fDialog = Application.FileDialog(msoFileDialogFolderPicker)
    With fDialog
        .AllowMultiSelect = False
        .Title = "Bitte Ordner wählen"
        If DCount("StartpfadBilder", "T_Startpfad") > 0 Then
           .InitialFileName = DLookup("StartpfadBilder", "T_Startpfad") & "\"
         Else
           .InitialFileName = Application.CurrentProject.Path & "\"
        End If
        .InitialView = msoFileDialogViewDetails
        .ButtonName = "als Standardpfad übernehmen"
        .Show
        If .SelectedItems.Count > 0 Then
                Set db = CurrentDb()
                Set rs = db.OpenRecordset("T_Startpfad", dbOpenDynaset)
                If rs.RecordCount > 0 Then
                   rs.Edit
                   rs!StartpfadBilder = .SelectedItems(1)
                   rs.Update
                 Else
                   rs.AddNew
                   rs!StartpfadBilder = .SelectedItems(1)
                   rs.Update
                End If
            rs.Close
            Set rs = Nothing
            Set db = Nothing
            Me!txtOrdnerpfad = DLookup("StartpfadBilder", "T_Startpfad") & "\"
          Else
            MsgBox "kein Pfad ausgewählt."
        End If
    End With
End Sub

Private Sub cbxDateiEndung_Enter()
   Me!cbxDateiEndung.Requery
End Sub

Private Sub DokuName_DblClick(Cancel As Integer)
   FollowHyperlink Me!DokuLink
End Sub


Private Sub btnErsterDS_Click()
    On Error Resume Next
    DoCmd.GoToRecord , , acFirst
End Sub

Private Sub btnLetzterDS_Click()
    On Error Resume Next
    DoCmd.GoToRecord , , acLast
End Sub

Private Sub btnNaechsterDS_Click()
    On Error Resume Next
    DoCmd.GoToRecord , , acNext
End Sub

Private Sub btnVorherigerDS_Click()
    On Error Resume Next
    DoCmd.GoToRecord , , acPrevious
End Sub

Private Sub btnNeuerDS_Click()
   DoCmd.GoToRecord , , acNewRec
End Sub

Private Sub btnAbbrechen_Click()
   Me.Undo
End Sub

Private Sub btnDatensatzLoeschen_Click()
'Vorsichtsmassnahme..wenn man einen Datensatz angefangen hat, kann dieser nicht gelöscht werden
If Me.NewRecord Then
     MsgBox "warum sollte auch ein angefangener Datensatz löschbar sein? Denk nach!"
     Exit Sub

   Else

    'ansonsten Löschabfrage mit Abbruchmöglichkeit
    'sicherheitshalber noch eine Fehlerbereinigung..es wird zur nächsten ausführbaren Codezeile gegangen
     On Error Resume Next
     If MsgBox("Wollen Sie das Dokument wirklich löschen?", vbQuestion + vbYesNo, "Datensatz löschen?") = vbYes Then
          'Löschen des angewählten Datensatz
          DoCmd.RunCommand acCmdDeleteRecord
          'Die Datensatzherkunft wird neu berechnet
          Me.Requery
          'Es wird auf den letzten vorhandenen Datensatz gesprungen
          DoCmd.GoToRecord , , acLast
          'alternativ
          'DoCmd.GoToRecord , , acFirst  '
      End If

End If

End Sub

Private Sub Form_Current()
On Error Resume Next

  With Me.Form.RecordsetClone

   If Not (.BOF And .EOF) Then .MoveLast

    If Me.CurrentRecord <= 1 Then
        Me!btnErsterDS.Enabled = False
        Me!btnVorherigerDS.Enabled = False
      Else
        Me!btnErsterDS.Enabled = True
        Me!btnVorherigerDS.Enabled = True
    End If

    If Me.CurrentRecord >= .RecordCount Then
        Me!btnNaechsterDS.Enabled = False
        Me!btnLetzterDS.Enabled = False
      Else
        Me!btnNaechsterDS.Enabled = True
        Me!btnLetzterDS.Enabled = True
    End If

    Me!lblDS.Caption = Me.CurrentRecord & " von " & .RecordCount & " Dokumente"
  End With

End Sub
