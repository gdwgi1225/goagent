@echo off

set uploaddir=python

( 
    echo ===============================================================
    echo  GoAgent����˲������, ��ʼ�ϴ�%uploaddir%�����
    echo  �����Ҫ�ϴ�golang�����, ���޸ı��ļ���uploaddir��ֵΪgolang
    echo ===============================================================
    echo.
    echo ����������appid, ���appid����^|�Ÿ���
) && (
    @cd /d "%~dp0" 
) && (
    set PYTHONSCRIPT="import sys;sys.path.insert(0, 'uploader.zip');import appcfg;appcfg.main()"
) && (
    "..\local\proxy.exe"
) && (
    echo.
    echo �ϴ��ɹ�����༭proxy.ini�����appid���ȥ��лл���밴������˳�����
)

@pause>NUL

  
  
@echo off