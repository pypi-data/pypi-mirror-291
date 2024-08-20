from setuptools import setup, find_packages

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='kgitest', #pip download project name
    version='0.0.2',
    description='Test project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='KGI',
    author_email='Teste@kgi.com',
    packages=find_packages(),
    package_data={
    },
    install_requires=[
    ]
)