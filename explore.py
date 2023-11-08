import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

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
    
def cluster_dataframes(df_list, features, n_clusters, scaler=MinMaxScaler(), cluster_algo=KMeans(), plot=False):
    # Scale the specified columns
    def scale_columns(df_list, scaler=MinMaxScaler()):
        for df in df_list:
            scaled_columns = df[df.columns.difference(['msa'])]
            scaled_values = scaler.fit_transform(scaled_columns)
            for col, values in zip(scaled_columns.columns, scaled_values.T):
                df[f'{col}_scaled'] = values
        return df_list

    df_list = scale_columns(df_list, scaler)
    
    for df in df_list:
        # Select the features to cluster
        X = df[[f'{feature}_scaled' for feature in features]]
        
        # Fit the clustering algorithm and predict the clusters
        cluster_algo.set_params(n_clusters=n_clusters)
        clusters = cluster_algo.fit_predict(X)
        
        # Add the clusters to the original dataframe
        df['cluster'] = clusters
        
        if plot:
            # Plot the clusters on 'affordability', 'violent_crime', and 'est_commute'
            plt.figure(figsize=(13, 7))
            sns.pairplot(data=df, vars=['affordability_ratio','violent_crime','est_commute'], hue='cluster', palette='RdYlGn')
            plt.show()
    
    return


def cluster_dataframes(df_list, features, df_names, n_clusters=3, scaler=MinMaxScaler(), cluster_algo=KMeans(), plot=False):
    # Scale the specified columns
    def scale_columns(df_list, scaler=MinMaxScaler()):
        for df in df_list:
            scaled_columns = df[df.columns.difference(['msa'])]
            scaled_values = scaler.fit_transform(scaled_columns)
            for col, values in zip(scaled_columns.columns, scaled_values.T):
                df[f'{col}_scaled'] = values
        return df_list

    df_list = scale_columns(df_list, scaler)
    
    for i, df in enumerate(df_list):
        # Select the features to cluster
        X = df[[f'{feature}_scaled' for feature in features]]
        
        # Fit the clustering algorithm and predict the clusters
        cluster_algo.set_params(n_clusters=n_clusters)
        clusters = cluster_algo.fit_predict(X)
        
        # Add the clusters to the original dataframe
        df['cluster'] = clusters
        
        if plot:
            # Plot the clusters on 'affordability', 'violent_crime', and 'est_commute'
            pairplot = sns.pairplot(data=df, vars=['affordability_ratio','violent_crime','est_commute', 'property_crime'], hue='cluster', palette='RdYlGn')
            if df_names:
                pairplot.fig.suptitle(f'Clusters for {df_names[i]}', y=1.02)  # y=1.02 raises the title slightly
            else:
                pairplot.fig.suptitle(f'Clusters for DataFrame {i+1}', y=1.02)
            plt.show()