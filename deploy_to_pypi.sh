python3 setup.py sdist
python3 setup.py bdist_wheel
twine upload dist/*
set -x
rm -rf dist
rm -rf build
rm -rf lxpservice.egg-info
rm -rf LxpApi/__pycache__
