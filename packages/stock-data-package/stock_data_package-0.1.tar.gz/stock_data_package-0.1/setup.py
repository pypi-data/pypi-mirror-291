from setuptools import setup, find_packages
setup(
    name='stock_data_package',  # Replace with your package name
    version='0.1',
    packages=find_packages(),
    install_requires=['pandas'],  # List any dependencies here
    author='Florence Idowu',
    author_email='idowuflorence93@gmail.com',
    description='This package is for downloading stock market data of companies',
    #url='https://github.com/yourusername/my_python_package',  # Add your GitHub repo if applicable
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
)
