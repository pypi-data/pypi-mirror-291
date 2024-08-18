from setuptools import setup, find_packages

setup(
    name="sayhw",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sayhello=sayhello:__main__.greet',
        ],
    },
    author="Ethan Xu",
    author_email="ethan@waitblock.simplelogin.com",
    description="Testing package that just prints out hello world.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sayhello",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
