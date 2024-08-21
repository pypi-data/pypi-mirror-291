from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="msteamsadaptivecardbuilder",
    version="1.0.1",
    description="Easily Build and Export Multilingual Adaptive Cards Through Python",
    py_modules=["msteamsadaptivecardbuilder"],
    package_dir={"": "src"},
    data_files=[("", ["LICENSE.txt"])],
    url="https://github.com/NandovdK/AdaptiveCardBuilder",
    author="Nando van der Kant",
    author_email="njvdkant@gmail.com",
    install_requires=["aiohttp", "requests"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
    ],
)
