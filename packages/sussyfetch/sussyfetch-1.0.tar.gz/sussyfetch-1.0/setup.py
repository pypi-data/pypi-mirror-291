from setuptools import setup, find_packages

setup(
    name="sussyfetch",
    version="1.0",
    description="ඞ Fetching system information in style",
    packages=find_packages(),
    install_requires=[
        "rich",
        "psutil",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "sussyfetch = sussyfetch.cli:main",
        ],
    },
    license="MIT",
    author="Zeyu Yao",
    author_email="novodoodle@gmail.com",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cytronicoder/sussyfetch",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
