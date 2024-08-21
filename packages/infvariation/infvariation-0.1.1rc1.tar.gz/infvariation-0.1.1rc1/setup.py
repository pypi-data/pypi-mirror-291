from setuptools import setup, find_packages

setup(
    name="infvariation",
    version="0.1.1-rc1",
    description="A Python library for generating information variations, such as typo-squatting domains, leet transformations, and custom text variations.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Fabio Gomes Rocha",
    author_email="gomesrocha@gmail.com",
    url="https://github.com/gomesrocha/infvariation",
    packages=find_packages(),
    install_requires=[
        "ail_typo_squatting",
        "leet",    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: Apache Software License',
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)


