from setuptools import setup, find_packages

setup(
    name="gpio_button",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "RPi.GPIO",
    ],
    description="A simple package to handle button input using RPi.GPIO",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/gpio_button",  # Replace with your actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)