from setuptools import setup

setup(
    name='tools-automator',
    version='0.0.1',
    py_modules=['main'],
    install_requires=[
        'Click',
        'pexpect'
    ],
    entry_points={
        'console_scripts': [
            'create_mysql = mysql:create_mysql',
        ],
    },
)