from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="bhagyashree",
    version="0.0.1",
    author="arpy8",
    description="wassup bbggg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpy8/bhagyashree",
    packages=find_packages(),
    install_requires=["pygame", "termcolor", "pyautogui", "keyboard", "opencv-python"],
    entry_points={
        "console_scripts": [
            "bhxg=bhxg.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'bhagyashree': ['assets/*.mp3', 'assets/*.json']},
    include_package_data=True,
    license="MIT"
)