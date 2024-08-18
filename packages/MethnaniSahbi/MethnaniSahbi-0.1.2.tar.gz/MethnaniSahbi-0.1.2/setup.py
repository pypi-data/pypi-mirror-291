from setuptools import setup, find_packages

setup(
    name='MethnaniSahbi',
    version='0.1.2',  # Mettez à jour la version pour refléter les modifications
    author='Sahbi Methnani',
    author_email='sahbimethnani3@gmail.com',
    description='Une bibliothèque pour la gestion des employés avec une interface graphique en PyQt5 et SQLite',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Sahbimethnani/MethnaniSahbi',  # Remplacez par l'URL de votre dépôt GitHub
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'MethnaniSahbi': ['image.png'],  # Inclure les fichiers spécifiques ici
    },
    install_requires=[
        'PyQt5',
        'pandas',
        'openpyxl',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
