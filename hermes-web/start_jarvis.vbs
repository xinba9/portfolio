' Jarvis Web Chat Auto-Start Script
' Runs Node.js server in hidden window, then opens browser

Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Paths
nodeExe = "C:\Users\EDY\.workbuddy\binaries\node\versions\22.22.2\node.exe"
workDir = "C:\Users\EDY\WorkBuddy\2026-06-15-16-18-44\hermes-web"
serverScript = workDir & "\server.js"

' Check if server already running (port 8765)
Set exec = WshShell.Exec("netstat -ano | findstr ""8765""")
output = exec.StdOut.ReadAll()

If InStr(output, "LISTEN") > 0 Then
    ' Server already running, just open browser
    WshShell.Run "http://localhost:8765"
Else
    ' Start server in hidden window
    serverCmd = """" & nodeExe & """ """ & serverScript & """"
    WshShell.Run "cmd /c cd /d """ & workDir & """ && " & serverCmd, 0, False
    
    ' Wait for server to start (3 seconds)
    WScript.Sleep 3000
    
    ' Open browser
    WshShell.Run "http://localhost:8765"
End If
