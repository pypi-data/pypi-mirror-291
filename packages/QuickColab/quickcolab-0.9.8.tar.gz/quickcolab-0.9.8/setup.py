from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='QuickColab',
    version='0.9.8',
    packages=find_packages(),
    install_requires=[
        'ipywidgets',
        'python-dotenv',
        'openai',
        'datasets',
        'transformers',
        'huggingsound',
        'pillow'
    ],
    description='A package for Google Colab utility functions.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='TimmyLai',
    author_email='lyyhkcc@gmail.com',
    url='https://github.com/yourusername/QuickColab',  # 替換為你的 GitHub 倉庫 URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'quickcolab=QuickColab.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'QuickColab': ['/*']
    },
)
