from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [line.strip() for line in open("requirements.txt").readlines()]
requirements_dev = [line.strip() for line in open("requirements-dev.txt").readlines()]
requirements_docs = [line.strip() for line in open("docs/requirements.txt").readlines()]

setup(
    name="statista",
    version="0.6.0",
    description="statistics package",
    author="Mostafa Farrag",
    author_email="moah.farag@gmail.come",
    url="https://github.com/Serapieum-of-alex/statista",
    keywords=[
        "statistics",
        "distributions",
        "extreme-value-analysis",
        "probability",
        "sensitivity-analysis",
    ],
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/markdown",
    license="GNU General Public License v3",
    zip_safe=False,
    packages=find_packages(include=["statista", "statista.*"]),
    test_suite="tests",
    tests_require=requirements_dev,
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "docs": requirements_docs,
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: GIS",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
    ],
)
