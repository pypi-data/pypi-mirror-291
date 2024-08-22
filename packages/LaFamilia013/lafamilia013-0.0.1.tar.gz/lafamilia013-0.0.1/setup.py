from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='LaFamilia013',
    version='0.0.1',
    license='MIT License',
    author='Matheus Nascimento',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='matheus.mn87@gmail.com',
    keywords='LaFamilia013',
    description=u'Apenas teste',
    packages=['LaFamilia'],
    install_requires=['requests'])