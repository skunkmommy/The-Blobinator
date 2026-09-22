#Requires AutoHotkey v2.0
#SingleInstance Force

myGui := Gui(, "The Blobinator")
myGui.Add("Text", , "Enter text")
argBox := myGui.Add("Edit", "w250")
btn := myGui.Add("Button", "Default w80", "OK")

btn.OnEvent("Click", RunApp)
myGui.OnEvent("Close", HideGui)
myGui.OnEvent("Escape", (*) => myGui.Hide())

;	Hotkey, change this if you'd rather use something else to open the window
#\:: {
    argBox.Value := ""
    myGui.Show()
    argBox.Focus()
}

HideGui(*) {
    myGui.Hide()
    return true
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

		output := RTrim(StrReplace(output, "`r`n", "`n"), "`n")

		SendText(output)
	}
}
