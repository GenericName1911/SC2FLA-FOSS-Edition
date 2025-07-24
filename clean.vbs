' Recursively clean $assets folder except .gitkeep
Set fso = CreateObject("Scripting.FileSystemObject")
Set folder = fso.GetFolder(".\$assets")

For Each file In folder.Files
    If LCase(file.Name) <> ".gitkeep" Then
        On Error Resume Next
        file.Delete True
        On Error GoTo 0
    End If
Next

For Each subfolder In folder.SubFolders
    On Error Resume Next
    subfolder.Delete True
    On Error GoTo 0
Next
