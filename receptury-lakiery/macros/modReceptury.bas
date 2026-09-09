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
