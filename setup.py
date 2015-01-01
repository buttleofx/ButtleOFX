from setuptools import setup

setup(
    name='ButtleOFX',
    version='2.0',
    description='Open source compositing software',
    long_description='',
    author='',
    author_email='buttleofx@googlegroups.com',
    license='LGPL',
    packages=['buttleofx'],
    package_dir={
        'buttleofx': 'buttleofx',
        'quickmamba': 'QuickMamba/quickmamba',
    },
    zip_safe=False,
    install_requires=[
        'PyQt5',
    ],
)

