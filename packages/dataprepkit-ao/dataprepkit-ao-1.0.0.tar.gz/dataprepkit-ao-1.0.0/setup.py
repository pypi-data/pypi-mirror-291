import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="dataprepkit-ao", 
    version="1.0.0",        
    author="Abdalrahman Osama",
    author_email="abdalrahman.osama01@gmail.com", 
    description="A streamlined data preprocessing toolkit for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dataprepkit-ao",  
    packages=setuptools.find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
    install_requires=[
        'pandas', 
        'numpy',
        'scikit-learn',
    ], 
)