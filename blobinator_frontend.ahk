#Requires AutoHotkey v2.0
#SingleInstance Force

myGui := Gui(, "Run app.py")
myGui.Add("Text", , "Enter text")
argBox := myGui.Add("Edit", "w250")
btn := myGui.Add("Button", "Default w80", "OK")

btn.OnEvent("Click", RunApp)
myGui.OnEvent("Close", HideGui)
myGui.OnEvent("Escape", (*) => myGui.Hide())

#\:: {
    argBox.Value := ""
    myGui.Show()
    argBox.Focus()
}

HideGui(*) {
    myGui.Hide()
    return true  ; hide instead of destroying the window
}

RunApp(*) {
    ; Escape any double quotes
    arg := StrReplace(argBox.Value, '"', '\"')
	arg := StrReplace(arg, '<', '^')
	arg := StrReplace(arg, '>', '^')
	if arg != "" {
		cmd := 'python "' A_ScriptDir '\blobspeak.py" "' arg '"'

		myGui.Hide()
		Sleep(32)

		; Run
		shell := ComObject("WScript.Shell")
		shell.CurrentDirectory := A_ScriptDir
		exec := shell.Exec(A_ComSpec ' /c "' cmd ' 2>&1"')
		output := exec.StdOut.ReadAll()

		; Normalize line endings and drop trailing newlines so no extra Enter is typed
		output := RTrim(StrReplace(output, "`r`n", "`n"), "`n")

		; SendText types the output literally (no special-key interpretation)
		SendText(output)
	}
}
