import setuptools
import asso

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asso",
    version="0.0.1",
    author="Penny Han",
    author_email="lynnpen@gmail.com",  
    description="AWS command wrapper script",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/lynnpen58/asso.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML >= 6.0',
        'inquirer >= 2.9.1',
        'boto3 >= 1.21.19',
        'argcomplete >= 2.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points='''
        [console_scripts]
        asso=asso:main
    ''',
)
