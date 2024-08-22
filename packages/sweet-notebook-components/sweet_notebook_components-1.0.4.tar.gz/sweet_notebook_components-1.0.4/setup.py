from setuptools import setup, find_packages

setup(
    name="sweet_notebook_components",
    version="1.0.4",
    packages=find_packages(),
    install_requires=["IPython"],
    author="Christoffer Artmann",
    author_email="Artgaard@gmail.com",
    description="A Streamlit-like component library for Notebooks.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/artmann/sweet_components",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
