from setuptools import setup, find_packages

setup(
    name='reactsms_sdk_python',  # Nom de votre package
    version='0.3',  # Version initiale
    author='Huberson Kouakou',
    author_email='huberson.kouakou@yahoo.com',
    description='React SMS SDK for Python',
    long_description=open('README.md').read(),  # Description longue depuis un fichier README.md
    long_description_content_type='text/markdown',  # Format du README
    url='https://github.com/hub-coffee/react-sms-sdk-python.git',  # Lien vers le dépôt du code source (ex : GitHub)
    packages=find_packages(),  # Recherche automatique des packages
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Licence du package
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Version minimale de Python requise
    install_requires=[  # Dépendances du package
        'requests==2.32.3',
    ],
)
