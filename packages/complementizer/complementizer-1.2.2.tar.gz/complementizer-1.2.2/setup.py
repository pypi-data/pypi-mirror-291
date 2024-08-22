from setuptools import setup, find_packages

setup(
    name="complementizer",
    version="1.2.2",
    description="Complementizer makes it easy to create and fill out automated forms for interactions with APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ismael Guedes",
    author_email="ismael.basic@gmail.com",
    url="https://github.com/ismaelvguedes/Complementizer",
    packages=find_packages(),
    install_requires=[
        'requests',
        'faker',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)