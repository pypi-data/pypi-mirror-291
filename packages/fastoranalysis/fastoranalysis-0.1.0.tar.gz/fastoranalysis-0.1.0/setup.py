from setuptools import setup, find_packages

setup(
    name='fastoranalysis',
    version='0.1.0',
    description="A performant factor analysis package for python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="davidq9199",
    packages=find_packages(),
    url="https://github.com/davidq9199/fastoranalyzer",
    install_requires=[
        'numpy',
        'scipy',
        'pytest',
    ],
        classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)