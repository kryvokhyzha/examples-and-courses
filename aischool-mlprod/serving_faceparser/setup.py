import setuptools
import os


os.system("rm -rf *.egg-info && rm -rf dist && rm -rf build")

setuptools.setup(
    name='face_parser',
    version="0.0.1",
    author="Demo",
    description="Package for face parser",
    packages=setuptools.find_packages(exclude=['bento*']),
    package_data={'face_parser': ['weights/*.pth']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3"
    ]
)

