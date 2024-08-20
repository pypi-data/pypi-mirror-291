# install the following to submit the lib on the internet:
# pip install twine tqdm
import setuptools
setuptools.setup(
    name="simcalc",
    version="0.1",
    author="Ali-Rida",
    description="Simple library in python for test",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License "
    ]
)