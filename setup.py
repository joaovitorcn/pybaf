import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybaf", # Replace with your own username
    version="0.0.1.2",
    author="joaovitocn",
    author_email="joaovitor.cn@gmail.com",
    description="Python Distance Calculator Bing Api facilitator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joaovitorcn/pybaf",
    packages=setuptools.find_packages(),
    install_requires=['Pandas'],
    classifiers=[
                    "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)