Set shell = CreateObject("WScript.Shell")
shell.Run "cmd /c del /f /q .\$assets\* & for /d %i in ("".\$assets\*"") do rmdir /s /q ""%i""", 0, True