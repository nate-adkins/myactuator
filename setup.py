from setuptools import setup, find_packages

setup(
    name="myactuator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'python-can',
        'pymodbus==2.5.2 '
    ],
    author="Nathan Adkins",
    author_email="nathanpadkins@gmail.com",
    description="Defines classes for controlling myactuator RMD motor",
    license="MIT",
    keywords="actuator robotics",
    url="https://github.com/nate-adkins/myactuator",   # project homepage
)
