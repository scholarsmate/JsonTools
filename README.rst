jtools
======

*JSON manipulation tool kit.*

creating a virtual environment
==============================

virtualenv -p python2.6 venv

building
========

virtual env
-----------
source ./venv/bin/activate

python setup.py build

python setup.py test

pip uninstall . && pip install .

deactivate

To deploy this, just tar up the venv directory which will have python, the jtools and all dependent modules installed.

native
------
The jtools works with python 2.6+.  If you don't want to go through the pain of building a complete virtual environment for each
target deployment, it will be easier to just put the jtools package in the PYTHONPATH and put the executable jtools file in the PATH.

python setup.py bdist

rm -rf usr && tar xvf dist/jtools-0.1.0.macosx-10.11-x86_64.tar.gz

PYTHONPATH=./usr/local/lib/python2.7/site-packages/ ./usr/local/bin/jtools hello

