from setuptools import find_packages, setup

setup(
    name='opendict-korean-fetcher',
    version='0.1.0',
    author='Tri-Cycle',
    description='opendict fetcher to extract related words',
    url='https://github.com/Tri-Cycle/opendict-korean-fetcher',
    packages=find_packages(),
    install_requires=['requests', 'urllib3', 'beautifulsoup4', 'neo4j'],
    python_requires='>=3',
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
