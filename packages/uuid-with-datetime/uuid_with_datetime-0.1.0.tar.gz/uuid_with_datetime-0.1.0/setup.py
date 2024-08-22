from setuptools import setup, find_packages

setup(
    name="uuid_with_datetime",
    version="0.1.0",
    author="Manikandan AL",
    author_email="manipythonjs@gmail.com",
    description="A package to generate a random UUID with the current date and time.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Manikandanpythonjs/pythonuuiddate",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
