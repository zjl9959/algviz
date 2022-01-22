@echo off

set PYTHON=%1
if [%2]==[] (
    echo "Usage: <python version> <lib1_name==lib1_version,lib2_name==lib2_version,...>"
    echo "       example: dependency_test.bat D:\\Python\\bin\\python3.7 graphviz-0.8.4--ipykernel-6.7.0"
    call :exit_code -2
)
set SCILENT=%3

echo Python version:
call %PYTHON% --version

set input_libs=%2
set DEPENDENCY_LIBS=%input_libs:--=','%
set DEPENDENCY_LIBS='%DEPENDENCY_LIBS:-===%'

cd /d %~dp0
cd ..

:: Create virtual environment for test.
call :clean_up_env
call %PYTHON% -m venv venv
if not exist venv\\Scripts\\activate.bat (
    echo "Create virtual environment failed."
    call :clean_up_env
    call :exit_code -1
)
call venv\\Scripts\\activate.bat

:: Copy package into venv.
md venv\\algviz
xcopy algviz venv\\algviz\\ /q /e /r /S /Y
echo from setuptools import setup >> venv\\setup.py
echo setup( >> venv/setup.py
echo    name="algviz", >> venv\\setup.py
echo    version="0.0.0", >> venv\\setup.py
echo    author="0", >> venv\\setup.py
echo    author_email="0", >> venv\\setup.py
echo    description=("0"), >> venv\\setup.py
echo    license="GPLv3", >> venv\\setup.py
echo    keywords="0", >> venv\\setup.py
echo    url="0", >> venv\\setup.py
echo    packages=['algviz'], >> venv\\setup.py
echo    install_requires=[ >> venv\\setup.py
echo        %DEPENDENCY_LIBS% >> venv\\setup.py
echo    ], >> venv\\setup.py
echo    python_requires=">=3", >> venv\\setup.py
echo    classifiers=[], >> venv\\setup.py
echo    zip_safe=False >> venv\\setup.py
echo ) >> venv\\setup.py

:: Install algviz and it's dependency modules into virtual environment.
cd venv
call %PYTHON% setup.py sdist
if not exist dist\\algviz-0.0.0.tar.gz (
    echo "Build algviz package failed."
    cd ..
    call :clean_up_env
    call :exit_code -3
)

call pip install wheel
call pip install dist\\algviz-0.0.0.tar.gz

:: Run benchmark test.
call pip list
cd ..
call %PYTHON% tests\\run.py
set TEST_RETURN=%errorlevel%
::call :clean_up_env
call :exit_code %TEST_RETURN%

:clean_up_env
if exist venv (
    echo "Clean up venv."
    set WHAT_SHOULD_BE_DELETED=venv
    for /r . %%a in (%WHAT_SHOULD_BE_DELETED%) do (  
        if exist %%a (  
        echo "remove"%%a
        rd /s /q "%%a"  
        )  
    )
)
EXIT /B 0

:: Exit with code.
:exit_code
if "%SCILENT%" == "s" (
    exit %~1
) else (
    echo "Exit with code:" %~1
    pause
    exit %~1
)
