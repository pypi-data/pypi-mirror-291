from setuptools import setup, find_packages


def le_arquivo(nome):
    with open(nome, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="HEXaag",
    version='1.0.0',
    packages=find_packages(),
    author='Alessandro Guarita',
    description='Ferramenta para gerar grid de hexágonos, para a criação de mapas de RPG.',
    long_description=le_arquivo('README.md'),
    long_description_content_type='text/markdown',
    LICENCE='MIT',
    python_requires='>=3.11',
)
