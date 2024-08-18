from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="poselib-v2",
    version="0.0.1",
    author="-T.K.-",
    author_email="t_k_233@outlook.email",
    description="Library for loading, manipulating, and retargeting skeleton poses and motions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/T-K-233/PoseLib",
    project_urls={
        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
    package_dir={"": "src/"},
    packages=find_packages(where="src/"),
    python_requires=">=3.8",
)