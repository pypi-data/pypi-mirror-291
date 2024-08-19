from setuptools import setup, find_packages

setup(
    name='motherbot',  # Название вашего пакета
    version='0.1',  # Версия пакета
    packages=find_packages(),  # Автоматически находит все пакеты в проекте
    include_package_data=True,  # Включает любые файлы, указанные в MANIFEST.in
    install_requires=[
        'pyfiglet',
        'fuzzywuzzy',
        'tabulate',
        'cfgv',
        'colorama',
        'distlib',
        'Faker',
        'filelock',
        'identify',
        'Levenshtein',
        'markdown-it-py',
        'mdurl',
        'nodeenv',
        'platformdirs',
        'pre-commit',
        'prompt_toolkit',
        'Pygments',
        'python-dateutil',
        'python-Levenshtein',
        'PyYAML',
        'rapidfuzz',
        'rich',
        'six',
        'virtualenv',
        'wcwidth'
    ],
    entry_points={
        'console_scripts': [
            'motherbot=motherbot.main:main',
        ],
    },
    author='Kateryna Tkachenko',
    author_email='tkachenko.city@gmail.com',
    description='Final project for Python course => MotherBot',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Iryna-Holova/goit-pycore-final',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
