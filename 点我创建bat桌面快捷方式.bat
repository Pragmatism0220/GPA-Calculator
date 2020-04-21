@echo off
for /f "tokens=2,*" %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Desktop"') do (set desk=%%j)
if exist "%desk%\GPA计算器.lnk" (Goto FileExistError) else (Goto CreateShortcut)
:FileExistError
echo "GPA计算器"快捷方式已存在！请检查！
echo(
pause
exit
:CreateShortcut
mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(a.SpecialFolders(""Desktop"") & ""\GPA计算器.lnk""):b.TargetPath=""%~dp0\GPA计算器.bat"":b.WorkingDirectory=""%~dp0"":b.IconLocation=""%~dp0\calculator.ico,0"":b.Save:close")
echo bat桌面快捷方式创建成功！
echo(
pause