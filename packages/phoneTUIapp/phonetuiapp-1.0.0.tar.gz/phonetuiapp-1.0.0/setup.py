from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="phoneTUIapp",
    version="1.0.0",
    author="Anurag Kanase",
    author_email="anuwrag@gmail.com",
    description="A TUI application for viewing calls and SMS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x07sh/phone/phoneTUIapp",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "npyscreen", ],
    entry_points={  
        'console_scripts': [
            'phoneTUIapp = phoneTUIapp.MyTUI:main'  
        ]
    },
    python_requires='>=3.6',  
)

