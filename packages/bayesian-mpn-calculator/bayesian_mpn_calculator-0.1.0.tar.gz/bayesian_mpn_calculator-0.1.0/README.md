# Bayesian MPN Calculator
This Python application calculates the Most Probable Number (MPN) using Bayesian inference, leveraging the PyMC library for robust statistical modeling. It enables users to estimate MPN and its credible intervals from microbiological data, typically used in determining the concentration of viable microorganisms in a sample.

The application is command-line driven, making it easy to integrate into automated workflows or larger data analysis pipelines. Users can input data from a CSV file, specify the number of replicates and dilution levels, and optionally generate plots of the MPN estimates with their credible intervals.

### Purpose of the Package

The Bayesian MPN Calculator is tailored for microbiologists and data scientists who need a reliable and statistically sound method for calculating MPN. The package uses Bayesian inference to provide more robust estimates compared to traditional methods, along with credible intervals that offer a clear measure of uncertainty.

### Features

- **Bayesian Inference**: Utilizes PyMC to perform Bayesian inference for MPN estimation, providing robust and credible results.
- **Customizable Input**: Allows users to specify the number of replicates, dilution levels, and the location of positive count data within the CSV file.
- **Output Options**: Exports the MPN estimates and credible intervals to a CSV file for further analysis.
- **Optional Plotting**: Generates plots showing MPN estimates with 95% credible intervals, aiding in visualization and interpretation of results.

### Input Data Format

The input data must be in a CSV file format. The file should contain:

- **Site Identifiers**: A column containing unique identifiers for each site or sample (e.g., Site).
- **Positive Count Data**: Several columns with the number of positive tubes or wells for each dilution level. The first column for positive counts is specified using the --counts-start-col option.

**Example of Input Data (CSV File)**
```shell
Site,Dilution_1,Dilution_2,Dilution_3,Dilution_4,Dilution_5,Dilution_6,Dilution_7,Dilution_8
Site_1,0,1,3,5,7,7,7,7
Site_2,0,0,1,4,6,7,7,7
Site_3,0,0,0,3,5,6,7,7
```
- `Site`: This column contains the identifiers for each site (e.g., Site_1, Site_2, Site_3).
- `Dilution_1 to Dilution_8`: These columns contain the count of positive results for each dilution level.

### Installation Instructions

**1. Python Environment**  
Ensure that you have [Python 3.8+](https://www.python.org/) installed.

```shell
pip install bayesian-mpn-calculator
```
**2. Dependencies**  
The following dependencies will be installed automatically:

- Click (for command-line interface)
- PyMC (for Bayesian inference)
- NumPy (for numerical operations)
- Pandas (for data manipulation)
- Matplotlib and Seaborn (for plotting)

### Usage
Once installed, the tool can be executed from the command line. Below is an example usage:

```shell
calculate-mpn --file-path 'path/to/MPN.csv' \
              --num-replicates 7 \
              --dilution-levels 1,10,100,1000,10000,100000,1000000,10000000 \
              --counts-start-col 'Dilution_1' \
              --output-path 'MPN_results.csv' \
              --plot \
              --id-col 'Site' \
              --dpi 300 \
              --fig-type 'png'
```

Command-Line Options
ommand-Line Options
- `-f, --file-path`: Path to the CSV file containing the data. (required)
- `-n, --num-replicates`: Number of replicates per dilution level. (required)
- `-D, --dilution-levels`: Comma-separated dilution levels (e.g., --dilution-levels 1,10,100). (required)
- `-c, --counts-start-col`: The column index or name where the positive counts start. (required)
- `-o, --output-path`: Path to save the output CSV file with MPN estimates and credible intervals. Default is 'MPN_results.csv'.
- `-p, --plot/--no-plot`: Whether to generate a plot of the MPN results. Default is no plot.
- `-i, --id-col`: Column name for the site identifiers in the CSV file. (required if --plot is used)
- `-d, --dpi`: DPI for saving the plot. Default is 300.
- `-ft, --fig-type`: File type for saving the plot (e.g., png, jpg). Default is 'png'.

### Acknowledgment
The development of this application builds on the capabilities of various Python libraries, especially PyMC for Bayesian inference and Pandas for data manipulation. These libraries provide the essential tools needed for robust statistical modeling and analysis in microbiological research.) 

