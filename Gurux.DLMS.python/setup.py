import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gurux_dlms",
    version="1.0.45",
    author="Gurux Ltd",
    author_email="gurux@gurux.org",
    description="Gurux DLMS library for Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gurux/gurux.dlms.python",
    packages=setuptools.find_packages(),
    package_data={'gurux_dlms': ['OBISCodes.txt', 'India.txt', 'Italy.txt', 'SaudiArabia.txt']},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    install_requires=['python-dateutil', 'pytz'],
)
