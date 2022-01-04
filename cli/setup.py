from setuptools import setup, find_packages
import os
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='tools-automator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=os.environ['RELEASE_VERSION'],
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
    author="João André Simões",
    author_email="jarpsimoes@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages=find_packages(exclude="tests"),
    include_package_data=True,

)
