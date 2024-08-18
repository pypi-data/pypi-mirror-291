from setuptools import setup, find_packages

setup(
    name='phoneTUIapp', 
    version='0.1.1',    
    packages=find_packages(),  
    install_requires=[
        'npyscreen', 
    ],  
    entry_points={ 
        'console_scripts': [
            'phoneTUI = phoneTUIapp.phoneTUI:main', 
        ],
    },

    author='Anurag Kanase',
    author_email='anuwrag@gmail.com',
    description='A TUI for interacting with phone calls and SMS',
    long_description='',
    long_description_content_type='text/markdown', 
    url='https://github.com/x07sh/phone/',  
    classifiers=[
        'Development Status :: 3 - Alpha', 
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6', 

)
