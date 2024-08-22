from setuptools import setup, find_packages
import os

def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

setup(
    name='PyGame-Platformer-Fin',
    version='1.0.1',
    description='A simple pygame platformer',
    author='Yogiram',
    author_email='yogiramkv@gmail.com',
    packages=find_packages(),  # Automatically finds the packages
    install_requires=read_requirements('requirements.txt'),  # Read dependencies from requirements.txt
    include_package_data=True,
    package_data={
        'PyGame-Platformer-Fin': ['platformer/assets/Background/*.png','platformer/assets/Items/Checkpoints/End*.png','platformer/assets/MainCharacters/MaskDude/*.png','platformer/assets/Terrain/*.png','platformer/assets/Traps/Fire/*.png'],  # Include other necessary files
    },
    entry_points={
        'console_scripts': [
            'start_game=platformer.game:main',  # Adjust to match your package structure
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
