from setuptools import setup

setup(
    name="optlib",
    version="0.4.0",
    description="A library for financial options pricing written in Python.",
    url="http://github.com/bartolomed/optlib",
    author="Davis Edwards & Daniel Rojas",
    packages=["optlib"],
    install_requires=["numpy", "scipy"],
    zip_safe=False
)
