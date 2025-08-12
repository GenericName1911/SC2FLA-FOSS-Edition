Set fso = CreateObject("Scripting.FileSystemObject")
Set assetsFolder = fso.GetFolder(".\$assets")
Set libFolder = fso.GetFolder(".\lib")

For Each file In assetsFolder.Files
    If LCase(file.Name) <> ".gitkeep" Then
        On Error Resume Next
        file.Delete True
        On Error GoTo 0
    End If
Next

Sub CleanAssetsFolder(fld)
    Dim subfolder
    For Each subfolder In fld.SubFolders
        CleanAssetsFolder subfolder
        On Error Resume Next
        subfolder.Delete True
        On Error GoTo 0
    Next
End Sub

Sub CleanLibFolder(fld)
    Dim subfolder
    For Each subfolder In fld.SubFolders
        name = LCase(subfolder.Name)
        If name = "__pycache__" Or name = "cache" Then
            On Error Resume Next
            subfolder.Delete True
            On Error GoTo 0
        Else
            CleanLibFolder subfolder
        End If
    Next
End Sub

CleanAssetsFolder assetsFolder
CleanLibFolder libFolder
