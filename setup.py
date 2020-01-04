from setuptools import setup

setup(
    name='pharm-drone',
    version='0.0.0',
    py_modules=['src.entry'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pharm-drone=src.entry:cli
    ''',
)
