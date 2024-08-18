import pathlib
import setuptools


setuptools.setup(
    name="PyNeura",
    version="0.1.0",
    description="An opensource library for low code deep learning using Python.",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/shravan-18/PyNeura",
    author="Shravan Venkatraman",
    author_email="vshravan180803@gmail.com",
    license="MIT",
    project_urls={
        "Homepage": "https://github.com/shravan-18/PyNeura",
        "Documentation": "https://github.com/shravan-18/PyNeura",
        "Source": "https://github.com/shravan-18/PyNeura",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["pyneura = pyneura.cli:main"]
    }
)
