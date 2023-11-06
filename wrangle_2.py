import pandas as pd
import numpy as np


def wrangle():
    '''
    wrangle will pull in the csv files for the dataframes and begin cleaning them by removing columns no longer needed, renaming columns for legibility, and finally bringing the two datasets together based on family composition. 
    '''
    # Acquire epi data
    col = pd.read_csv('cost_of_living_msa.csv')
    # Acquire Census Data
    family_income = pd.read_csv('B19126_msa_2022.csv')
    family_count = pd.read_csv('DP02_msa_2022.csv')
    
    # grab the indices 6 and 7 from the dataset and store as male
    male = family_count[6:8]
    # grab the indices 10 and 11 from the dataset and store as female
    female = family_count[10:12]
    # join the two dataframes
    family_count = pd.concat([female, male], ignore_index=True, axis = 0)
    # since we have unnecessary columns in between the ones we want, let's skip every other column
    columns = family_count.columns[2::2]
    # now let's drop every other column
    family_count.drop(columns, axis = 1, inplace = True)
    # for legibility, let's rename the index into named columns
    family_count = family_count.T.rename(columns = {0:'fem_total(count)', 1:'fem_with_kid(count)', 2:'male_total(count)', 3:'male_with_kid(count)'})
    # we still have a row that is full of the old title, let's remove that
    family_count = family_count.drop(family_count.index[0])

    # now we can remove null values and remove commas from our numbers
    family_count = family_count.fillna('0')
    family_count['fem_total(count)'] = family_count['fem_total(count)'].str.replace(',', '').astype(int)
    family_count['fem_with_kid(count)'] = family_count['fem_with_kid(count)'].str.replace(',', '').astype(int)
    family_count['male_total(count)'] = family_count['male_total(count)'].str.replace(',', '').astype(int)
    family_count['male_with_kid(count)'] = family_count['male_with_kid(count)'].str.replace(',', '').astype(int)

    # transform strings into floats
    family_count['fem_no_kid(count)'] = family_count['fem_total(count)'] - family_count['fem_with_kid(count)']
    family_count['male_no_kid(count)'] = family_count['male_total(count)'] - family_count['male_with_kid(count)']

    # grab the associated indices for male, female, and total
    tot = family_income[4:6]
    male = family_income[10:12]
    female = family_income[14:16]
    # bring those together
    family_income = pd.concat([tot, female, male], ignore_index=True, axis = 0)
    # for legibility, let's rename the index into named columns
    family_income = family_income.T.rename(columns = {0:'mar_with_kid', 1:'mar_no_kid', 2:'fem_with_kid(income)', 
                                                      3:'fem_no_kid(income)', 4:'male_with_kid(income)', 5:'male_no_kid(income)'})
    family_income = family_income.drop(family_income.index[0])

    # let's remove special characters from our strings
    family_income['mar_with_kid'] = family_income['mar_with_kid'].str.replace('+', '')
    family_income['male_no_kid(income)'] = family_income['male_no_kid(income)'].str.replace('+', '').replace('-', '')
    family_income['male_with_kid(income)'] = family_income['male_no_kid(income)'].str.replace('+', '').replace('-', '')

    # now let's remove all other special characters and fill some of our blank values with 0 to be dropped later
    family_income['mar_with_kid'] = family_income['mar_with_kid'].replace('', '0').str.replace(',', '').astype(int)
    family_income['mar_no_kid'] = family_income['mar_no_kid'].replace('', '0').str.replace(',', '').astype(int)
    family_income['fem_no_kid(income)'] = family_income['fem_no_kid(income)'].replace('', '0').str.replace(',', '').astype(int)
    family_income['fem_with_kid(income)'] = family_income['fem_with_kid(income)'].replace('', '0').str.replace(',', '').astype(int)
    family_income['male_no_kid(income)'] = family_income['male_no_kid(income)'].replace('', '0').str.replace(',', '').astype(int)
    family_income['male_with_kid(income)'] = family_income['male_with_kid(income)'].replace('', '0').str.replace(',', '').astype(int)

    # finally let's bring these two together
    family = pd.concat([family_income, family_count], axis = 1)
    
    # make the column names of col lowercase
    col.columns = col.columns.str.lower()
    col.rename(columns = {'areaname' :'msa'}, inplace=True)


    # Calculate income for each family type
    family['single_no_kid(income)'] = (family['fem_no_kid(income)'] * family['fem_no_kid(count)'] + family['male_no_kid(income)'] * family['male_no_kid(count)'])/(family['fem_no_kid(count)'] + family['male_no_kid(count)'])
    family['single_with_kid'] = ((family['fem_with_kid(income)'] * family['fem_with_kid(count)']) + (family['male_with_kid(income)'] * family['male_with_kid(count)']))/(family['fem_with_kid(count)'] + family['male_with_kid(count)'])
    # Drop unnecessary columns from family
    family = family[['mar_with_kid', 'mar_no_kid', 'single_no_kid(income)', 'single_with_kid']]
    # replace NaN with 0
    family = family.fillna(0)
    # Round values to the nearest integer and convert to int
    family['mar_with_kid'] = round(family['mar_with_kid']).astype(int)
    family['mar_no_kid'] = round(family['mar_no_kid']).astype(int)
    family['single_no_kid(income)'] = round(family['single_no_kid(income)']).astype(int)
    family['single_with_kid'] = round(family['single_with_kid']).astype(int)

    # make the index of family the first column
    family.reset_index(inplace = True)
   
    # rename the first column to 'msa'
    family.rename(columns = {'index':'msa'}, inplace = True)
    
    # in col.msa replace HUD Metro FMR Area with MSA
    col.msa = col.msa.str.replace('HUD Metro FMR Area', 'MSA')
    
    # in family.msa replace Metro Area!!Estimate with MSA
    family['msa'] = family['msa'].str.replace('Metro Area!!Estimate', 'MSA')
    
    # merge col and family
    col_df = pd.merge(col, family, on = 'msa', how = 'right')
    
    # Replace 'median_family_income' where 'family_member_count' is '1p0c'
    col_df.loc[col_df['family'] == '1p0c', 'median_family_income'] = col_df['single_no_kid(income)']
    # Replace 'median_family_income' where 'family_member_count' is '2p0c'
    col_df.loc[col_df['family'] == '2p0c', 'median_family_income'] = col_df['mar_no_kid']
    # Replace 'median_family_income' where 'family_member_count' is '1p1c', '1p2c', '1p3c', '1p4c'
    for count in ['1p1c', '1p2c', '1p3c', '1p4c']:
        col_df.loc[col_df['family'] == count, 'median_family_income'] = col_df['single_with_kid']
    # Replace 'median_family_income' where 'family_member_count' is '2p1c', '2p2c', '2p3c', '2p4c'
    for count in ['2p1c', '2p2c', '2p3c', '2p4c']:
        col_df.loc[col_df['family'] == count, 'median_family_income'] = col_df['mar_with_kid']
    
    # adjusting values for inflation since original data from 2020 and new data from 2022 (Jan 2020 - Jan 2022; 8.98% inflation)
    col_df['housing'] = col_df['housing'] * 1.0898
    col_df['food'] = col_df['food'] * 1.0898
    col_df['transportation'] = col_df['transportation'] * 1.0898
    col_df['healthcare'] = col_df['healthcare'] * 1.0898
    col_df['other'] = col_df['other necessities '] * 1.0898
    col_df['childcare'] = col_df['childcare'] * 1.0898
    col_df['taxes'] = col_df['taxes'] * 1.0898
    col_df['total'] = col_df['total'] * 1.0898

    # dropping null values and columns no longer needed
    col_df = col_df.dropna()
    col_df = col_df.drop(columns={'mar_with_kid', 'mar_no_kid', 'single_no_kid(income)', 'single_with_kid'})
    
    # changing values into integers
    col_df.housing = round(col_df.housing).astype(int)
    col_df.food = round(col_df.food).astype(int)
    col_df.transportation = round(col_df.transportation).astype(int)
    col_df.healthcare = round(col_df.healthcare).astype(int)
    col_df.other = round(col_df.other).astype(int)
    col_df.childcare = round(col_df.childcare).astype(int)
    col_df.taxes = round(col_df.taxes).astype(int)
    col_df.total = round(col_df.total).astype(int)
    col_df.median_family_income = col_df.median_family_income.astype(int)

    # Separate family_member_count into parents and children
    col_df['parents'] = col_df['family'].str[0].astype(int)
    col_df['children'] = col_df['family'].str[2].astype(int)

    # Reorder Columns
    cost = col_df[['msa', 'parents', 'children', 'housing', 'food', 'transportation', 'healthcare', 'other', 'childcare', 'taxes', 'total', 'median_family_income']]
    
    return cost