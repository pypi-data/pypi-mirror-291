from setuptools import setup, find_packages

setup(
    name="grapesdb",
    version="1.3.0",
    description="THE way to store data.",
    author="ItsTato",
    author_email="thatpogcomputer@gmail.com",
    url="https://github.com/ItsTato/grapes",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
		"Development Status :: 4 - Beta",
		"Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)