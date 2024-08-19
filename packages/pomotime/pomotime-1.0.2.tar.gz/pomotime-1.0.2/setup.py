from setuptools import setup, find_packages

# Загружаем содержимое файла README.md для использования в качестве long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pomotime",
    version="1.0.2",
    author="zabojeb",
    author_email="zabojeb@bk.ru",
    description="Stylish customizable CLI Pomodoro timer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zabojeb/pomotime",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "rich",
        "art",
        "appdirs",
        "toml",
    ],
    entry_points={
        "console_scripts": [
            "pomotime=pomotime.pomotime:pomotime",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.0",
)
