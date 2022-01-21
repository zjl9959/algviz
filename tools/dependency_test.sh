#!/usr/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: <python version> <lib1_name==lib1_version,lib2_name==lib2_version,...>
            example: ./dependency_test.sh graphviz==0.13.2,ipython==7.0.0"
    exit -2
fi

# Check python3 version in the system.
PYTHON=$1
if [[ `$PYTHON -V | grep -c "Python 3"` -eq 0 ]]; then
    echo "Can't find Python3 in your system."
    exit -1
fi
echo "Python version: "`$PYTHON -V`

DEPENDENCY_LIBS="\""${2//","/"\",\""}"\""

clean_up_env()
{
    if [ -d "venv" ]; then
        rm -rf venv
    fi
}

BASEDIR=$(dirname "$0")
cd $BASEDIR"/.."

# Create virtual environment for test.
clean_up_env
$PYTHON -m venv venv
if [ ! -d "venv" ]; then
    echo "Create virtual environment failed."
    exit -1
fi
source venv/bin/activate

# Copy package into venv.
cp -rf algviz venv/
cat <<EOF >>"venv/setup.py"
from setuptools import setup

setup(
    name="algviz",
    version="0.0.0",
    author="0",
    author_email="0",
    description=("0"),
    license="GPLv3",
    keywords="0",
    url="0",
    packages=['algviz'],
    install_requires=[
        $DEPENDENCY_LIBS
    ],
    python_requires='>=3',
    classifiers=[],
    zip_safe=False
)
EOF

# Install algviz and it's dependency modules into virtual environment.
cd venv
sudo $PYTHON setup.py sdist

sudo chown -R $USER dist algviz.egg-info
if [ ! -f "dist/algviz-0.0.0.tar.gz" ]; then
    echo "Build algviz package failed."
    cd ".."
    clean_up_env
    exit -3
fi
pip install wheel
pip install dist/algviz-0.0.0.tar.gz

# Run benchmark test.
pip list
cd ".."
$PYTHON tests/run.py
TEST_RETURN=`echo $?`
clean_up_env
exit $TEST_RETURN
