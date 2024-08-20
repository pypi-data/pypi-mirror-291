import click
import pymc as pm
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pytensor
import os
import shutil

# Configuration to handle potential issues with PyTensor
def configure_pytensor():
    os.environ['PYTENSOR_LOCK_TIMEOUT'] = '60'  # Set a higher timeout for the file lock
    pytensor.config.on_opt_error = 'ignore'  # Disable on_opt_error
    pytensor.config.optimizer = 'fast_compile'  # Use a safer optimizer

    # Clear PyTensor cache if necessary
    cache_dir = os.path.expanduser("~/.pytensor")
    if os.path.exists(cache_dir):
        try:
            shutil.rmtree(cache_dir)
        except Exception as e:
            print(f"Warning: Unable to clear PyTensor cache: {e}")

# Call the configuration function at the start of your script
configure_pytensor()

def bayesian_mpn(file_path, num_replicates, dilution_levels, counts_start_col, output_path='MPN_results.csv'):
    """
    Calculate MPN using Bayesian inference with pymc.
    """
    df = pd.read_csv(file_path)
    dilution_levels = np.log10(np.array(dilution_levels))
    results = []

    for index, row in df.iterrows():
        positive_counts = row[counts_start_col:].values.astype(int)
        
        with pm.Model() as model:
            log_mpn = pm.Uniform('log_mpn', lower=-5, upper=5)
            probs = 1 - pm.math.exp(-10 ** log_mpn / (10 ** dilution_levels))
            obs = pm.Binomial('obs', n=num_replicates, p=probs, observed=positive_counts)
            trace = pm.sample(2000, tune=2000, chains=4, return_inferencedata=False, cores=1)
            
            mpn_estimate = np.median(10 ** trace['log_mpn'])
            lower_ci = np.percentile(10 ** trace['log_mpn'], 2.5)
            upper_ci = np.percentile(10 ** trace['log_mpn'], 97.5)
            
            results.append((mpn_estimate, lower_ci, upper_ci))
    
    df[['MPN', 'Lower_CI', 'Upper_CI']] = pd.DataFrame(results, index=df.index)
    df.to_csv(output_path, index=False)
    return df

def plot_results(df, id_col, dpi, fig_type):
    plt.figure(figsize=(14, 7))
    sns.barplot(x=id_col, y='MPN', data=df, errorbar=None)
    plt.errorbar(
        x=df[id_col], 
        y=df['MPN'], 
        yerr=[df['MPN'] - df['Lower_CI'], df['Upper_CI'] - df['MPN']], 
        fmt='none', 
        ecolor='black', 
        capsize=5
    )
    plt.xticks(rotation=45)
    plt.title('Bayesian MPN Estimates Across Sites with 95% Credible Intervals')
    plt.xlabel(id_col)
    plt.ylabel('MPN Estimate')
    plt.savefig(f"output_plot.{fig_type}", dpi=dpi, bbox_inches='tight')
    plt.show()

@click.command()
@click.option('--file-path', '-f', required=True, help='Path to the CSV file containing the data.')
@click.option('--num-replicates', '-n', required=True, type=int, help='Number of replicates per dilution level.')
@click.option('--dilution-levels', '-D', required=True, help='Comma-separated dilution levels (e.g., "1,10,100").')
@click.option('--counts-start-col', '-c', required=True, help='The column index or name where the positive counts start.')
@click.option('--output-path', '-o', default='MPN_results.csv', help='Path to save the output CSV file with MPN estimates and credible intervals.')
@click.option('--plot/--no-plot', '-p/-np', default=False, help='Whether to plot the MPN results.')
@click.option('--id-col','-i', required=True, help='Column name for the site identifiers in the CSV file.')
@click.option('--dpi', '-d', default=300, help='DPI for saving the plot.')
@click.option('--fig-type','-ft', default='png', help='File type for saving the plot (e.g., png, jpg).')
def calculate_mpn(file_path, num_replicates, dilution_levels, counts_start_col, output_path, plot, id_col, dpi, fig_type):
    """
    Command-line tool to calculate MPN using Bayesian inference and optionally plot the results.
    """
    dilution_levels = [int(x) for x in dilution_levels.split(',')]
    df_with_results = bayesian_mpn(file_path, num_replicates, dilution_levels, counts_start_col, output_path)
    
    if plot:
        plot_results(df_with_results, id_col, dpi, fig_type)

if __name__ == '__main__':
    calculate_mpn()
