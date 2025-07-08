from setuptools import setup, find_packages

setup(
    name="landuse_rb",  
    version="0.0.1",     
    packages=find_packages(),
    description="Пакет `landuse-rb` реализует пространственный классификатор типов землепользования",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Roman Bashirov",
    author_email="bashiroff.roman@gmail.com",
    url="https://github.com/romanroff/landuse-lib",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)