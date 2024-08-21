import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="check_cuda",
    version="0.0.3",
    author="wangruihua",
    author_email="wangruihua@163.cn",
    description="check cuda version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangruihua/checkcuda",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'torch>=1.7.0',
    ],
    python_requires='>=3.6',
)