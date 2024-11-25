from setuptools import setup, find_packages

setup(
    name="pyactuator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'python-can',
    ],
    author="Nathan Adkins",
    author_email="nathanpadkins@gmail.com",
    description="Code for creating messages to control myactuator RMD motors",
    license="MIT",
    keywords="actuator robotics",
    url="https://github.com/nate-adkins/pyactuator",   # project homepage
)
