@echo off
CLS
@title IE�Զ����ýű�(PAC)

:MENU
echo.          =-=-=-=-=IE�Զ����ýű��˵�=-=-=-=-= 
echo.
echo. 1 http://127.0.0.1:1999/flora_pac.pac���Ƽ�ʹ�������
echo.
echo. 2 file://��ַ\flora_pac.pac
echo.

echo. ������ѡ����Ŀ����Ų����س������У�
set /p XUANXIANG= 
if "%XUANXIANG%"=="1" goto 1
if "%XUANXIANG%"=="2" goto 2

:1
echo.
echo ���ڸ��£����Ե�...
@reg add "HKCU\SOFTWARE\Microsoft\windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d "http://127.0.0.1:1999/flora_pac.pac" /f
exit

:2
echo.
echo ���ڸ��£����Ե�...
@reg add "HKCU\SOFTWARE\Microsoft\windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d "file://%cd%\flora_pac.pac" /f
exit
