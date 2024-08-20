import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HMautogroup",
    version="0.4.1",
    author="KDPark",
    author_email="k602511@gmail.com",
    description="auto-cleaning-grouping-process",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kdpark0284/HM_titledescription_filtering",
    project_urls={
        "Bug Tracker": "https://github.com/kdpark0284/HM_titledescription_filtering/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "openpyxl", 
        "numpy", 
        "pandas", 
        "regex",  
        "konlpy", 
        "setuptools",
        "mecab-python",
        "mecab-python3",
        "rapidfuzz",
        "jamo",
        "wheel"
    ],
    entry_points={
        'console_scripts': [
            'hmautogroup=HMautogroup.main:main',  
        ],
    },
    package_dir={"HMautogroup": "lib/HMautogroup"},
    packages=["HMautogroup"],
    package_data={'': ['LICENSE.txt', 'requirements.txt']},
    include_package_data=True,
    python_requires=">=3.10",
)

# python setup.py sdist bdist_wheel
# twine upload dist/*