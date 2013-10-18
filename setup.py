import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name = "clamped",
    version = "0.1",
    packages = find_packages(),
    package_data = {
        "clamped": ["data/*.txt"],
    },
    install_requires = ["clamp>=0.2"],
    clamp = ["clamped"],
)
