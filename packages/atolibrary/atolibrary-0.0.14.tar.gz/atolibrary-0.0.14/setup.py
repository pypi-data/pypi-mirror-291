from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
readme =  os.path.join(this_directory, "README.md")  #(this_directory / "README.md").read_text()
with open(readme, encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="atolibrary",
    version="0.0.14",
    author="ATO JEON",
    author_email="atto.jeon@gmail.com",
    description="A utility library for image processing and random number generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/attojeon/atolibrary",  # GitHub 저장소 URL을 여기에 넣으세요
    packages=find_packages(),
    install_requires=[
        'Pillow>=9.0.0',
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