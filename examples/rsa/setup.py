from setuptools import setup, find_packages

setup(
    name="rsa",
    version="0.1",
    description="Examples of cryptographic primitives",
    url="https://github.com/Isaac-DeFrain/cryptography/blob/main/src/rsa.py",
    author="Isaac DeFrain",
    author_email="quantifier-tech@protonmail.com",
    packages=find_packages(),
    requires=["crypto", "typing"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">3.7",
)
