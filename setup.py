from setuptools import setup
from LxpApi.utils import NAME, VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("lxpservice.md", "r") as fh:
    long_description += '\n' + fh.read()

setup(
    name=NAME,
    version=VERSION,
    license='LGPL2',
    description='Command line tool and library to manage LetterXpress print jobs.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Winfried Simon',
    author_email='winfried.simon@gmail.com',
    url='https://github.com/Simsys/LxpApi',
    packages=['LxpApi'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='comman-line-tool library print-service',
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'keyring'
    ],
    entry_points={'console_scripts': ['lxpservice=LxpApi:main',],},
)
