from setuptools import setup, find_packages

from setuptools import setup, find_packages

setup(
    name='cognitive_schema',
    version='0.2.0',
    description='An drive CLI tool for downloading database schemas and generating profiles.',
    author='Aitor Oses',
    author_email='aitor.oses@example.com',
    packages=find_packages(),
    install_requires=[
        'click',
        'psycopg2',
        'pandas',
        'openai',
    ],
    entry_points={
        'console_scripts': [
            'cognitive_schema=cognitive_schema.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)