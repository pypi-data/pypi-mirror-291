from setuptools import setup, find_packages

setup(
    name='QuickColab',  # 將名稱更改為 QuickColab
    version='0.9.5',  
    packages=find_packages(),  
    install_requires=[
        'ipywidgets',
        'python-dotenv' 
    ],
    description='A package for Google Colab utility functions.',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    author='TimmyLai',
    author_email='lyyhkcc@gmail.com', # 更新為新的網址
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
