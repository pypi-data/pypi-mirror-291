from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="vovo",
    version="0.0.2",
    description="A small library package",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="ark",
    author_email="ark.wu@outlook.com",
    url="",
    packages= find_packages(),
    install_requires = [
        'requests>=2.32.3',
        'tqdm>=4.66.4'
    ],
    python_requires=">=3.12",
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
