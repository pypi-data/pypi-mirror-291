from setuptools import setup, find_packages

setup(
    name="palette-gen",
    version="0.1.0",
    author="auth-xyz",
    author_email="smmc.auth@gmail.com",
    description="A simple tool to extract and display color palettes from images.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/auth-xyz/palette",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "rich",
        "scikit-learn",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'color_palette=color_palette.color_palette:main',
        ],
    },
)