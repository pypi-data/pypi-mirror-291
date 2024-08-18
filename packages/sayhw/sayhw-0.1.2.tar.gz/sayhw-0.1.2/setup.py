from setuptools import setup, find_packages

setup(
    name="sayhw",
    version="0.1.2",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sayhw=sayhw:__main__.say',
        ],
    },
    author="Ethan Xu",
    author_email="ethan@waitblock.simplelogin.com",
    description="Testing package that just prints out hello world.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
