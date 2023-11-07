import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_family_histograms(dataframes, column_name):
    single_types = [f'single_{i}_child' for i in range(5)]
    married_types = [f'married_{i}_child' for i in range(5)]

    fig, axs = plt.subplots(5, 2, figsize=(15, 30))

    for i in range(5):
        df_single = dataframes[single_types[i]].replace([np.inf, -np.inf], np.nan)
        axs[i, 0].hist(df_single[column_name], bins=30, edgecolor='black')
        axs[i, 0].set_title(f'{column_name} for {single_types[i]}')
        axs[i, 0].set_xlabel(column_name)
        axs[i, 0].set_ylabel('Frequency')
        x_min, x_max = cost[column_name].min(), cost[column_name].max()
        x_max = x_max
        axs[i, 0].set_xlim(x_min, x_max)

        df_married = dataframes[married_types[i]].replace([np.inf, -np.inf], np.nan)
        axs[i, 1].hist(df_married[column_name], bins=30, edgecolor='black')
        axs[i, 1].set_title(f'{column_name} for {married_types[i]}')
        axs[i, 1].set_xlabel(column_name)
        axs[i, 1].set_ylabel('Frequency')
        x_min, x_max = cost[column_name].min(), cost[column_name].max()
        x_max = x_max
        axs[i, 1].set_xlim(x_min, x_max)

    plt.tight_layout()
    plt.show()
    
    
def plot_COST_histograms(df, columns):
    fig, axs = plt.subplots(len(columns), 1, figsize=(10, 5*len(columns)))

    for i, column_name in enumerate(columns):
        df_column = df[column_name].replace([np.inf, -np.inf], np.nan)
        axs[i].hist(df_column.dropna(), bins=30, edgecolor='black')
        axs[i].set_title(f'{column_name}')
        axs[i].set_xlabel(column_name)
        axs[i].set_ylabel('Frequency')
        x_min, x_max = df_column.min(), df_column.max()
        axs[i].set_xlim(x_min, x_max)

    plt.tight_layout()
    plt.show()