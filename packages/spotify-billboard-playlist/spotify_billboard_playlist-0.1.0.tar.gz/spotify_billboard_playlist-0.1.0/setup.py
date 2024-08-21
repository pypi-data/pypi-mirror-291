from setuptools import setup, find_packages

setup(
    name='spotify-billboard-playlist',  # Nome do pacote no PyPI
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Adicione as dependências aqui, se necessário
    ],
    author='Rui Cirilo',
    author_email='ruicirilo1972@gmil.com',
    description='Pacote para criar playlists do Spotify com base nas paradas da Billboard.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ruicirilo4/spotify-billboard-playlist',  # URL do repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
