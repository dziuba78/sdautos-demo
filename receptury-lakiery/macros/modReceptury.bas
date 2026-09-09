REM ***** LibreOffice Basic — system receptur lakierów *****
REM Moduł: modReceptury
REM Działa w LibreOffice Calc. Nie wykonuje operacji sieciowych.

Option Explicit

Const R0 As Integer = 12
Const R1 As Integer = 51
Const HIST_START As Integer = 9
Const HIST_END As Integer = 208
Const POS_START As Integer = 9
Const POS_END As Integer = 508
Const HASLO As String = "lakier"

Global gSelListener As Object
Global gMouseListener As Object
Global gInitLista As Boolean
Global gBusyLista As Boolean
Global gLastNrAddr As String
Global gOtworzonoListe As Boolean


Function Arkusz(nazwa As String) As Object
    Arkusz = ThisComponent.Sheets.getByName(nazwa)
End Function


Sub Odblokuj(oSheet As Object)
    If oSheet.IsProtected Then
        oSheet.unprotect(HASLO)
    End If
End Sub


Sub Zablokuj(oSheet As Object)
    REM Ochrona arkuszy wyłączona — plik roboczy ma dać się edytować i zapisać bez hasła.
    REM Nie zakładaj ponownie ochrony po makrach NowaReceptura / KopiujDoWlasnej / ZapiszWersje.
End Sub


Sub Przelicz()
    ThisComponent.calculateAll()
End Sub


Sub WyczyscZakres(oSheet As Object, kol As Integer, wierszOd As Integer, wierszDo As Integer)
    Dim i As Integer
    For i = wierszOd To wierszDo
        oSheet.getCellByPosition(kol, i - 1).String = ""
    Next i
End Sub


Sub NowaReceptura
    Dim oStart As Object, oOryg As Object, oWlas As Object, oUst As Object
    oStart = Arkusz("START")
    oOryg = Arkusz("RECEPTURA_ORYGINALNA")
    oWlas = Arkusz("RECEPTURA_WLASNA")
    oUst = Arkusz("USTAWIENIA")
    Odblokuj(oStart) : Odblokuj(oOryg) : Odblokuj(oWlas) : Odblokuj(oUst)

    Dim nr As Long
    nr = CLng(oUst.getCellRangeByName("B12").Value)
    If nr < 1 Then nr = 1
    Dim prefiks As String
    prefiks = oUst.getCellRangeByName("B13").String
    If prefiks = "" Then prefiks = "RC-"

    oStart.getCellRangeByName("C5").String = ""
    oStart.getCellRangeByName("C6").String = prefiks & Format(nr, "0000")
    oStart.getCellRangeByName("C7").String = ""
    oStart.getCellRangeByName("C8").String = ""
    oStart.getCellRangeByName("C9").String = ""
    oStart.getCellRangeByName("C11").Value = 1
    oStart.getCellRangeByName("C14").String = ""
    oStart.getCellRangeByName("C15").Value = 100
    oStart.getCellRangeByName("C13").Formula = "=TODAY()"

    Dim i As Integer
    For i = R0 To R1
        oOryg.getCellByPosition(1, i - 1).String = ""
        oOryg.getCellByPosition(2, i - 1).String = ""
        oOryg.getCellByPosition(4, i - 1).String = ""
        oOryg.getCellByPosition(7, i - 1).String = ""
        oWlas.getCellByPosition(1, i - 1).String = ""
        oWlas.getCellByPosition(2, i - 1).String = ""
        oWlas.getCellByPosition(5, i - 1).String = ""
        oWlas.getCellByPosition(11, i - 1).String = ""
    Next i

    oUst.getCellRangeByName("B12").Value = nr + 1
    Przelicz()
    Zablokuj(oStart) : Zablokuj(oOryg) : Zablokuj(oWlas) : Zablokuj(oUst)
    MsgBox "Utworzono nową recepturę " & prefiks & Format(nr, "0000") & ". Wybierz system bazowy i wpisz skład na arkuszu RECEPTURA_ORYGINALNA.", 64, "Nowa receptura"
End Sub


Sub KopiujDoWlasnej
    Dim oOryg As Object, oWlas As Object
    oOryg = Arkusz("RECEPTURA_ORYGINALNA")
    oWlas = Arkusz("RECEPTURA_WLASNA")
    Odblokuj(oWlas)
    Dim i As Integer
    Dim sys As String, nr As String
    For i = R0 To R1
        sys = Trim(oOryg.getCellByPosition(1, i - 1).String)
        nr = Trim(oOryg.getCellByPosition(2, i - 1).String)
        oWlas.getCellByPosition(1, i - 1).String = sys
        oWlas.getCellByPosition(2, i - 1).String = nr
        If nr <> "" Then
            oWlas.getCellByPosition(5, i - 1).Value = oOryg.getCellByPosition(4, i - 1).Value
        Else
            oWlas.getCellByPosition(5, i - 1).String = ""
        End If
        oWlas.getCellByPosition(11, i - 1).String = oOryg.getCellByPosition(7, i - 1).String
    Next i
    Przelicz()
    Zablokuj(oWlas)
    MsgBox "Skopiowano skład oryginalny do receptury własnej. Możesz zmieniać ilości i dodawać pigmenty z drugiego systemu.", 64, "Kopia"
End Sub


Sub ZastosujPrzeliczenie
    Dim oWlas As Object
    oWlas = Arkusz("RECEPTURA_WLASNA")
    Odblokuj(oWlas)
    Dim i As Integer
    Dim nr As String
    Dim nowa As Double
    For i = R0 To R1
        nr = Trim(oWlas.getCellByPosition(2, i - 1).String)
        If nr <> "" Then
            nowa = oWlas.getCellByPosition(12, i - 1).Value
            oWlas.getCellByPosition(5, i - 1).Value = nowa
        End If
    Next i
    Przelicz()
    Zablokuj(oWlas)
    MsgBox "Zapisano przeliczone ilości do kolumny ILOŚĆ WŁASNA. Poprzednie wartości nie trafiają automatycznie do HISTORIA — użyj ZapiszWersje.", 64, "Przeliczenie masy"
End Sub


Sub ZapiszWersje
    Dim oStart As Object, oHist As Object, oPoz As Object, oWlas As Object
    oStart = Arkusz("START")
    oHist = Arkusz("HISTORIA")
    oPoz = Arkusz("HISTORIA_POZYCJE")
    oWlas = Arkusz("RECEPTURA_WLASNA")
    Odblokuj(oHist) : Odblokuj(oPoz) : Odblokuj(oStart)

    Dim wiersz As Integer
    wiersz = HIST_START
    Do While wiersz <= HIST_END
        If Trim(oHist.getCellByPosition(0, wiersz - 1).String) = "" Then Exit Do
        wiersz = wiersz + 1
    Loop
    If wiersz > HIST_END Then
        MsgBox "Brak miejsca w HISTORIA. Zwiększ zakres lub zarchiwizuj plik.", 16, "Historia"
        Zablokuj(oHist) : Zablokuj(oPoz) : Zablokuj(oStart)
        Exit Sub
    End If

    Dim idr As String, wersja As Double
    idr = oStart.getCellRangeByName("C6").String
    wersja = oStart.getCellRangeByName("C11").Value
    Przelicz()

    oHist.getCellByPosition(0, wiersz - 1).String = idr
    oHist.getCellByPosition(1, wiersz - 1).Value = oStart.getCellRangeByName("C13").Value
    oHist.getCellByPosition(2, wiersz - 1).String = oStart.getCellRangeByName("C5").String
    oHist.getCellByPosition(3, wiersz - 1).String = oStart.getCellRangeByName("C10").String
    oHist.getCellByPosition(4, wiersz - 1).Value = wersja
    oHist.getCellByPosition(5, wiersz - 1).String = oStart.getCellRangeByName("C12").String
    oHist.getCellByPosition(6, wiersz - 1).Value = oStart.getCellRangeByName("I6").Value
    oHist.getCellByPosition(7, wiersz - 1).String = oStart.getCellRangeByName("C8").String
    oHist.getCellByPosition(8, wiersz - 1).Value = oStart.getCellRangeByName("I8").Value
    oHist.getCellByPosition(9, wiersz - 1).String = oStart.getCellRangeByName("C14").String
    oHist.getCellByPosition(10, wiersz - 1).String = oStart.getCellRangeByName("I11").String
    oHist.getCellByPosition(11, wiersz - 1).String = "ZAPIS " & Format(Now, "YYYY-MM-DD HH:MM")

    Dim p As Integer, i As Integer, lp As Integer
    p = POS_START
    Do While p <= POS_END
        If Trim(oPoz.getCellByPosition(0, p - 1).String) = "" Then Exit Do
        p = p + 1
    Loop
    lp = 0
    For i = R0 To R1
        If Trim(oWlas.getCellByPosition(2, i - 1).String) <> "" Then
            If p > POS_END Then Exit For
            lp = lp + 1
            oPoz.getCellByPosition(0, p - 1).String = idr
            oPoz.getCellByPosition(1, p - 1).Value = wersja
            oPoz.getCellByPosition(2, p - 1).Value = lp
            oPoz.getCellByPosition(3, p - 1).String = oWlas.getCellByPosition(1, i - 1).String
            oPoz.getCellByPosition(4, p - 1).String = oWlas.getCellByPosition(2, i - 1).String
            oPoz.getCellByPosition(5, p - 1).String = oWlas.getCellByPosition(3, i - 1).String
            oPoz.getCellByPosition(6, p - 1).Value = oWlas.getCellByPosition(4, i - 1).Value
            oPoz.getCellByPosition(7, p - 1).Value = oWlas.getCellByPosition(5, i - 1).Value
            oPoz.getCellByPosition(8, p - 1).String = oWlas.getCellByPosition(10, i - 1).String
            p = p + 1
        End If
    Next i

    oStart.getCellRangeByName("C11").Value = wersja + 1
    Zablokuj(oHist) : Zablokuj(oPoz) : Zablokuj(oStart)
    MsgBox "Zapisano wersję " & idr & " v" & wersja & " w HISTORIA. Kolejna edycja będzie v" & (wersja + 1) & ".", 64, "Historia"
End Sub


Sub ScalDuplikaty
    Dim oWlas As Object
    oWlas = Arkusz("RECEPTURA_WLASNA")
    Odblokuj(oWlas)
    Dim i As Integer, j As Integer
    Dim klucz1 As String, klucz2 As String
    Dim suma As Double
    Dim scalono As Integer
    scalono = 0
    For i = R0 To R1
        klucz1 = Trim(oWlas.getCellByPosition(15, i - 1).String)
        If klucz1 <> "" Then
            suma = oWlas.getCellByPosition(5, i - 1).Value
            For j = i + 1 To R1
                klucz2 = Trim(oWlas.getCellByPosition(15, j - 1).String)
                If klucz2 = klucz1 Then
                    suma = suma + oWlas.getCellByPosition(5, j - 1).Value
                    oWlas.getCellByPosition(1, j - 1).String = ""
                    oWlas.getCellByPosition(2, j - 1).String = ""
                    oWlas.getCellByPosition(5, j - 1).String = ""
                    scalono = scalono + 1
                End If
            Next j
            oWlas.getCellByPosition(5, i - 1).Value = suma
        End If
    Next i
    Przelicz()
    Zablokuj(oWlas)
    If scalono = 0 Then
        MsgBox "Nie znaleziono duplikatów klucza SYSTEM|NR.", 64, "Duplikaty"
    Else
        MsgBox "Zsumowano " & scalono & " powtórzeń. Ilości dodane do pierwszej pozycji.", 64, "Duplikaty"
    End If
End Sub


Sub IdzStart
    ThisComponent.CurrentController.setActiveSheet(Arkusz("START"))
End Sub

Sub IdzOryginalna
    ThisComponent.CurrentController.setActiveSheet(Arkusz("RECEPTURA_ORYGINALNA"))
End Sub

Sub IdzWlasna
    ThisComponent.CurrentController.setActiveSheet(Arkusz("RECEPTURA_WLASNA"))
End Sub

Sub IdzAnaliza
    ThisComponent.CurrentController.setActiveSheet(Arkusz("ANALIZA"))
End Sub

Sub IdzRaport
    ThisComponent.CurrentController.setActiveSheet(Arkusz("RAPORT"))
End Sub


REM ===== Lista rozwijana NR PIGMENTU (zależna od SYSTEM w wierszu) =====
REM Calc pokazuje strzałkę TYLKO przy zwykłym zakresie ($T$9:$T$n / $U$9:$U$n).
REM INDIRECT w Validity nie rysuje dropdownu — nie używać jako źródła listy.

Sub PrzyOtwarciu
    On Error Resume Next
    UstawWalidacjeWszystkichNr
    If gInitLista Then Exit Sub
    gSelListener = CreateUnoListener("Sel_", "com.sun.star.view.XSelectionChangeListener")
    ThisComponent.CurrentController.addSelectionChangeListener(gSelListener)
    gMouseListener = CreateUnoListener("Mysz_", "com.sun.star.awt.XEnhancedMouseClickHandler")
    Arkusz("RECEPTURA_ORYGINALNA").addEnhancedMouseEventListener(gMouseListener)
    Arkusz("RECEPTURA_WLASNA").addEnhancedMouseEventListener(gMouseListener)
    Arkusz("DOBARWIANIE").addEnhancedMouseEventListener(gMouseListener)
    gInitLista = True
End Sub


Sub OnWyborKomorki
    REM Zdarzenie arkusza on-select (wstrzyknięte do ODS).
    Dim oSel As Object
    If gBusyLista Then Exit Sub
    On Error Resume Next
    oSel = ThisComponent.CurrentSelection
    If IsNull(oSel) Then Exit Sub
    If Not oSel.SupportsService("com.sun.star.sheet.SheetCell") Then Exit Sub
    If CzyKomorkaNrPigmentu(oSel) Then
        ObsluzKomorkeNr oSel, True
    ElseIf CzyKomorkaSystemu(oSel) Then
        UstawWalidacjeKomorkiNr KomorkaNrZWiersza(oSel), UCase(Trim(oSel.String))
    End If
End Sub


Sub OnZmianaKomorki
    REM Po wyborze SYSTEM w kolumnie B — ustaw źródło listy NR w tym wierszu.
    Dim oSel As Object
    If gBusyLista Then Exit Sub
    On Error Resume Next
    oSel = ThisComponent.CurrentSelection
    If IsNull(oSel) Then Exit Sub
    If Not oSel.SupportsService("com.sun.star.sheet.SheetCell") Then Exit Sub
    If CzyKomorkaSystemu(oSel) Then
        UstawWalidacjeKomorkiNr KomorkaNrZWiersza(oSel), UCase(Trim(oSel.String))
    End If
End Sub


Sub Sel_disposing(oEvt)
End Sub


Sub Sel_selectionChanged(oEvt)
    Dim oSel As Object
    If gBusyLista Then Exit Sub
    On Error Resume Next
    oSel = ThisComponent.CurrentSelection
    If IsNull(oSel) Then Exit Sub
    If Not oSel.SupportsService("com.sun.star.sheet.SheetCell") Then
        gLastNrAddr = ""
        Exit Sub
    End If
    If CzyKomorkaSystemu(oSel) Then
        gLastNrAddr = ""
        UstawWalidacjeKomorkiNr KomorkaNrZWiersza(oSel), UCase(Trim(oSel.String))
        Exit Sub
    End If
    If Not CzyKomorkaNrPigmentu(oSel) Then
        gLastNrAddr = ""
        Exit Sub
    End If
    If oSel.AbsoluteName = gLastNrAddr Then Exit Sub
    gLastNrAddr = oSel.AbsoluteName
    ObsluzKomorkeNr oSel, True
    gOtworzonoListe = True
End Sub


Function Mysz_mousePressed(oEvt As Object) As Boolean
    gOtworzonoListe = False
    Mysz_mousePressed = False
End Function


Function Mysz_mouseReleased(oEvt As Object) As Boolean
    Dim oCell As Object
    Mysz_mouseReleased = False
    If gBusyLista Then Exit Function
    If gOtworzonoListe Then
        gOtworzonoListe = False
        Exit Function
    End If
    On Error Resume Next
    oCell = oEvt.Target
    If IsNull(oCell) Then Exit Function
    If Not oCell.SupportsService("com.sun.star.sheet.SheetCell") Then Exit Function
    If CzyKomorkaSystemu(oCell) Then
        UstawWalidacjeKomorkiNr KomorkaNrZWiersza(oCell), UCase(Trim(oCell.String))
        Exit Function
    End If
    If Not CzyKomorkaNrPigmentu(oCell) Then Exit Function
    gLastNrAddr = oCell.AbsoluteName
    ObsluzKomorkeNr oCell, True
End Function


Sub Mysz_disposing(oEvt)
End Sub


Function CzyKomorkaNrPigmentu(oCell As Object) As Boolean
    Dim s As String
    Dim col As Long
    Dim row As Long
    CzyKomorkaNrPigmentu = False
    On Error Resume Next
    s = oCell.Spreadsheet.Name
    col = oCell.CellAddress.Column
    row = oCell.CellAddress.Row + 1
    If s = "RECEPTURA_ORYGINALNA" Or s = "RECEPTURA_WLASNA" Then
        If col = 2 And row >= R0 And row <= R1 Then CzyKomorkaNrPigmentu = True
    ElseIf s = "DOBARWIANIE" Then
        If col = 1 And row = 5 Then CzyKomorkaNrPigmentu = True
    End If
End Function


Function CzyKomorkaSystemu(oCell As Object) As Boolean
    Dim s As String
    Dim col As Long
    Dim row As Long
    CzyKomorkaSystemu = False
    On Error Resume Next
    s = oCell.Spreadsheet.Name
    col = oCell.CellAddress.Column
    row = oCell.CellAddress.Row + 1
    If s = "RECEPTURA_ORYGINALNA" Or s = "RECEPTURA_WLASNA" Then
        If col = 1 And row >= R0 And row <= R1 Then CzyKomorkaSystemu = True
    ElseIf s = "DOBARWIANIE" Then
        If col = 1 And row = 4 Then CzyKomorkaSystemu = True
    End If
End Function


Function KomorkaNrZWiersza(oSys As Object) As Object
    Dim s As String
    s = oSys.Spreadsheet.Name
    If s = "DOBARWIANIE" Then
        KomorkaNrZWiersza = oSys.Spreadsheet.getCellRangeByName("B5")
    Else
        KomorkaNrZWiersza = oSys.Spreadsheet.getCellByPosition(2, oSys.CellAddress.Row)
    End If
End Function


Function SystemZKomorkiNr(oCell As Object) As String
    Dim s As String
    Dim row As Long
    s = oCell.Spreadsheet.Name
    row = oCell.CellAddress.Row
    If s = "DOBARWIANIE" Then
        SystemZKomorkiNr = UCase(Trim(oCell.Spreadsheet.getCellByPosition(1, 3).String))
    Else
        SystemZKomorkiNr = UCase(Trim(oCell.Spreadsheet.getCellByPosition(1, row).String))
    End If
End Function


Function AdresListyPigmentow(oSheet As Object, sys As String) As String
    Dim n As Long
    Dim oL As Object
    AdresListyPigmentow = ""
    On Error Resume Next
    oL = Arkusz("LISTY")
    sys = UCase(Trim(sys))
    If sys = "DUXONE" Then
        n = CLng(oL.getCellRangeByName("K10").Value)
        If n < 1 Then n = 79
        AdresListyPigmentow = "$U$9:$U$" & CStr(8 + n)
    ElseIf sys = "AUTOCOLOR" Then
        n = CLng(oL.getCellRangeByName("J10").Value)
        If n < 1 Then n = 107
        AdresListyPigmentow = "$T$9:$T$" & CStr(8 + n)
    End If
End Function


Sub UstawWalidacjeKomorkiNr(oCell As Object, sys As String)
    Dim oVal As Object
    Dim adres As String
    If IsNull(oCell) Then Exit Sub
    adres = AdresListyPigmentow(oCell.Spreadsheet, sys)
    If adres = "" Then Exit Sub
    On Error Resume Next
    oVal = oCell.Validation
    oVal.Type = com.sun.star.sheet.ValidationType.LIST
    oVal.ShowList = com.sun.star.sheet.TableValidationVisibility.UNSORTED
    oVal.IgnoreBlankCells = True
    oVal.ShowErrorMessage = False
    oVal.ShowInputMessage = True
    oVal.InputTitle = "NR PIGMENTU"
    oVal.InputMessage = "Lista pigmentów " & sys & " — wybierz z listy, nie wpisuj kodu."
    oVal.Formula1 = adres
    oCell.Validation = oVal
End Sub


Sub ObsluzKomorkeNr(oCell As Object, bOtworz As Boolean)
    Dim sys As String
    Dim wybrane As String
    If gBusyLista Then Exit Sub
    gBusyLista = True
    On Error Resume Next
    sys = SystemZKomorkiNr(oCell)
    If sys <> "AUTOCOLOR" And sys <> "DUXONE" Then
        gBusyLista = False
        If bOtworz Then
            MsgBox "Najpierw kliknij SYSTEM w tym wierszu i wybierz AUTOCOLOR albo DUXONE.", 64, "NR PIGMENTU"
        End If
        Exit Sub
    End If
    UstawWalidacjeKomorkiNr oCell, sys
    If bOtworz Then
        wybrane = DialogListaPigmentow(oCell.Spreadsheet, sys, Trim(oCell.String))
        If wybrane <> "" Then
            oCell.String = wybrane
            Przelicz()
        End If
    End If
    gBusyLista = False
End Sub


Function DialogListaPigmentow(oSheet As Object, sys As String, biezace As String) As String
    REM Widoczna lista (kod | nazwa). Zwraca etykietę albo "".
    Dim oDlgModel As Object
    Dim oDlg As Object
    Dim oLstM As Object
    Dim oOkM As Object
    Dim oAnM As Object
    Dim oTk As Object
    Dim oList As Object
    Dim col As Integer
    Dim i As Integer
    Dim n As Long
    Dim txt As String
    Dim sel As Integer
    Dim oL As Object
    DialogListaPigmentow = ""
    On Error Resume Next
    oL = Arkusz("LISTY")
    If UCase(sys) = "DUXONE" Then
        col = 20
        n = CLng(oL.getCellRangeByName("K10").Value)
        If n < 1 Then n = 79
    Else
        col = 19
        n = CLng(oL.getCellRangeByName("J10").Value)
        If n < 1 Then n = 107
    End If
    oDlgModel = CreateUnoService("com.sun.star.awt.UnoControlDialogModel")
    oDlgModel.Title = "Pigmenty " & sys & " — wybierz z listy"
    oDlgModel.Width = 240
    oDlgModel.Height = 220
    oDlgModel.Closeable = True
    oLstM = oDlgModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")
    oLstM.Name = "Lista"
    oLstM.PositionX = 6
    oLstM.PositionY = 6
    oLstM.Width = 228
    oLstM.Height = 190
    oLstM.Dropdown = False
    oLstM.MultiSelection = False
    oDlgModel.insertByName("Lista", oLstM)
    oOkM = oDlgModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    oOkM.Name = "OK"
    oOkM.PositionX = 124
    oOkM.PositionY = 200
    oOkM.Width = 50
    oOkM.Height = 14
    oOkM.Label = "OK"
    oOkM.PushButtonType = 1
    oOkM.DefaultButton = True
    oDlgModel.insertByName("OK", oOkM)
    oAnM = oDlgModel.createInstance("com.sun.star.awt.UnoControlButtonModel")
    oAnM.Name = "Anuluj"
    oAnM.PositionX = 178
    oAnM.PositionY = 200
    oAnM.Width = 50
    oAnM.Height = 14
    oAnM.Label = "Anuluj"
    oAnM.PushButtonType = 2
    oDlgModel.insertByName("Anuluj", oAnM)
    oDlg = CreateUnoService("com.sun.star.awt.UnoControlDialog")
    oDlg.setModel(oDlgModel)
    oTk = CreateUnoService("com.sun.star.awt.Toolkit")
    oDlg.createPeer(oTk, oTk.getDesktopWindow())
    oList = oDlg.getControl("Lista")
    For i = 0 To n - 1
        txt = Trim(oSheet.getCellByPosition(col, 8 + i).String)
        If txt <> "" Then
            oList.addItem(txt, oList.getItemCount())
            If txt = biezace Then oList.selectItemPos(oList.getItemCount() - 1, True)
        End If
    Next i
    If oDlg.execute() = 1 Then
        sel = oList.getSelectedItemPos()
        If sel >= 0 Then DialogListaPigmentow = oList.getItem(sel)
    End If
    oDlg.dispose()
End Function


Sub OtworzListeRozwijana
    Dim oDisp As Object
    Dim oFrame As Object
    On Error Resume Next
    oDisp = createUnoService("com.sun.star.frame.DispatchHelper")
    oFrame = ThisComponent.CurrentController.Frame
    oDisp.executeDispatch(oFrame, ".uno:DataSelect", "", 0, Array())
End Sub


Sub UstawWalidacjeWszystkichNr
    Dim i As Integer
    Dim oOryg As Object
    Dim oWlas As Object
    Dim oDob As Object
    Dim sys As String
    On Error Resume Next
    oOryg = Arkusz("RECEPTURA_ORYGINALNA")
    oWlas = Arkusz("RECEPTURA_WLASNA")
    oDob = Arkusz("DOBARWIANIE")
    For i = R0 To R1
        sys = UCase(Trim(oOryg.getCellByPosition(1, i - 1).String))
        If sys = "AUTOCOLOR" Or sys = "DUXONE" Then
            UstawWalidacjeKomorkiNr oOryg.getCellByPosition(2, i - 1), sys
        End If
        sys = UCase(Trim(oWlas.getCellByPosition(1, i - 1).String))
        If sys = "AUTOCOLOR" Or sys = "DUXONE" Then
            UstawWalidacjeKomorkiNr oWlas.getCellByPosition(2, i - 1), sys
        End If
    Next i
    sys = UCase(Trim(oDob.getCellRangeByName("B4").String))
    If sys = "AUTOCOLOR" Or sys = "DUXONE" Then
        UstawWalidacjeKomorkiNr oDob.getCellRangeByName("B5"), sys
    End If
End Sub
