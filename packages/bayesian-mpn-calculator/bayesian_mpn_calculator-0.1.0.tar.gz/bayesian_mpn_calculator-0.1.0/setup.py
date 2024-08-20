import setuptools

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as readme_file:
    LONG_DESCRIPTION = readme_file.read()

setuptools.setup(
    name="bayesian_mpn_calculator",
    version="0.1.0",
    description="A package to calculate Most Probable Number (MPN) using Bayesian inference.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Clabe Wekesa",
    author_email="simiyu86wekesa@gmail.com",
    url="https://github.com/clabe-wekesa/bayesian-mpn-calculator",  # Replace with your GitHub URL
    keywords=['bayesian inference', 'MPN', 'biostatistics', 'microbiology', 'pymc'],
    install_requires=[
        'Click',
        'pymc',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
    ],
    python_requires='>=3.6',
    packages=['bayesian_mpn_calculator'],
    package_dir={'bayesian_mpn_calculator': 'bayesian_mpn_calculator'},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'calculate-mpn = bayesian_mpn_calculator.mpn_calculator:calculate_mpn',
        ],
    },
    scripts=[],
)
