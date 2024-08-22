from setuptools import setup, find_packages

setup(
    name="febedatasets",
    version="1.8",
    packages=[
        "febedatasetswits",
        "lab01",
        "lab02",
        "lab03",
        "lab04",
        "lab05",
        "lab06",
        "lab07",
        "lab08",
        "lab09",
        "lab10",
        "BonusLab",
    ],
    include_package_data=True,
    install_requires=["pandas", "Pillow", "otter-grader"],
    package_data={
        "": ["data/*.csv", "images/*.png", "tests/*.py", "data/*.txt"],
    },
    author="Isaiah Chiraira",
    author_email="itchiraira@gmail.com",
    description="A package to load different datasets used in a Wits University First Year engineering datascince course",
    url="https://github.com/Tech-Gui/febe1004Datasets",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",
)
