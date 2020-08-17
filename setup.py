from setuptools import setup

setup(
    name="optlib",
    version="0.0.1",
    description="A library to price financial options written in Python.",
    url="http://github.com/bartolomed/optlib",
    author="Davis Edwards & Daniel Rojas",
    packages=["optlib"],
    install_requires=["numpy", "scipy"],
    zip_safe=False
)
