@echo off
for /f "tokens=2,*" %%i in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Desktop"') do (set desk=%%j)
if exist "%desk%\GPA������.lnk" (Goto FileExistError) else (Goto CreateShortcut)
:FileExistError
echo "GPA������"��ݷ�ʽ�Ѵ��ڣ����飡
echo(
pause
exit
:CreateShortcut
mshta VBScript:Execute("Set a=CreateObject(""WScript.Shell""):Set b=a.CreateShortcut(a.SpecialFolders(""Desktop"") & ""\GPA������.lnk""):b.TargetPath=""%~dp0\GPA������.bat"":b.WorkingDirectory=""%~dp0"":b.IconLocation=""%~dp0\calculator.ico,0"":b.Save:close")
echo bat�����ݷ�ʽ�����ɹ���
echo(
pause