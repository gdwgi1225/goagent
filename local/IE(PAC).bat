@echo off
CLS
@title IE自动配置脚本(PAC)

:MENU
echo.          =-=-=-=-=IE自动配置脚本菜单=-=-=-=-= 
echo.
echo. 1 http://127.0.0.1:1999/flora_pac.pac（推荐使用这个）
echo.
echo. 2 file://地址\flora_pac.pac
echo.

echo. 请输入选择项目的序号并按回车键运行：
set /p XUANXIANG= 
if "%XUANXIANG%"=="1" goto 1
if "%XUANXIANG%"=="2" goto 2

:1
echo.
echo 正在更新，请稍等...
@reg add "HKCU\SOFTWARE\Microsoft\windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d "http://127.0.0.1:1999/flora_pac.pac" /f
exit

:2
echo.
echo 正在更新，请稍等...
@reg add "HKCU\SOFTWARE\Microsoft\windows\CurrentVersion\Internet Settings" /v AutoConfigURL /t REG_SZ /d "file://%cd%\flora_pac.pac" /f
exit
