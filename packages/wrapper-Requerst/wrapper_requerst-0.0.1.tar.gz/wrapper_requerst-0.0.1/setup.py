from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='wrapper-Requerst',
    version='0.0.1',
    license='MIT License',
    author='Serial Tecnologias',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='serial@outlook.com.br',
    keywords='Requerst',
    description=u'Wrapper não oficial do Requerst',
    packages=['requerst_st'],
    install_requires=['requests'],)