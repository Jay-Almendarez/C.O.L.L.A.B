import pandas as pd
import numpy as np


def wrangle():
    '''
    wrangle will pull in the csv files for the dataframes and begin cleaning them by removing columns no longer needed, renaming columns for legibility, and finally bringing the two datasets together based on family composition. 
    '''
    # Acquire kaggle data
    col = pd.read_csv('cost_of_living_us.csv')
    dem = pd.read_csv('county_demographics.csv')

    # Acquire Census Data
    family_income = pd.read_csv('B19126.csv')
    family_count = pd.read_csv('DP02.csv')
    
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
    # rename the first column to 'county'
    family.rename(columns = {'index':'county'}, inplace = True)
    # make the county column lowercase
    family['county'] = family['county'].str.lower()
    # Create a dictionary of state names and their abbreviations
    state_abbreviations = {
        '_alabama': '_al',
        '_alaska': '_ak',
        '_arizona': '_az',
        '_arkansas': '_ar',
        '_california': '_ca',
        '_colorado': '_co',
        '_connecticut': '_ct',
        '_delaware': '_de',
        '_florida': '_fl',
        '_georgia': '_ga',
        '_hawaii': '_hi',
        '_idaho': '_id',
        '_illinois': '_il',
        '_indiana': '_in',
        '_iowa': '_ia',
        '_kansas': '_ks',
        '_kentucky': '_ky',
        '_louisiana': '_la',
        '_maine': '_me',
        '_maryland': '_md',
        '_massachusetts': '_ma',
        '_michigan': '_mi',
        '_minnesota': '_mn',
        '_mississippi': '_ms',
        '_missouri': '_mo',
        '_montana': '_mt',
        '_nebraska': '_ne',
        '_nevada': '_nv',
        '_new_hampshire': '_nh',
        '_new_jersey': '_nj',
        '_new_mexico': '_nm',
        '_new_york': '_ny',
        '_north_carolina': '_nc',
        '_north_dakota': '_nd',
        '_ohio': '_oh',
        '_oklahoma': '_ok',
        '_oregon': '_or',
        '_pennsylvania': '_pa',
        '_rhode_island': '_ri',
        '_south_carolina': '_sc',
        '_south_dakota': '_sd',
        '_tennessee': '_tn',
        '_texas': '_tx',
        '_utah': '_ut',
        '_vermont': '_vt',
        '_west_virginia': '_wv',
        '_virginia': '_va',
        '_washington': '_wa',
        '_wisconsin': '_wi',
        '_wyoming': '_wy'
    }
    # replace county column
    family['county'] = family['county'].str.replace(r'(.+) county, (.+)!!estimate', r'\1_county_\2', regex=True)
    family['county'] = family['county'].str.replace(r'(.+) parish, (.+)!!estimate', r'\1_parish_\2', regex=True)
    family['county'] = family['county'].str.replace(r'(.+) city, (.+)!!estimate', r'\1_city_\2', regex=True)
    family['county'] = family['county'].str.replace(' ', '_')
    # Use the replace function to replace the state names with their abbreviations
    family['county'] = family['county'].replace(state_abbreviations, regex=True)
    # Drop rows in Puerto Rico
    family = family[~family.county.str.contains('puerto_rico')]
    family.county[110] = 'district_of_columbia_dc'
    # change the format of our county columns to be the same for easier merging
    col['county'] = col.county.str.replace(' ', '_').str.lower() + '_' + col.state.str.lower()
    col = col.drop(columns = {'state', 'areaname', 'case_id'})

    # Merge the dataframes
    col_df = pd.merge(col, family, on='county', how='right')
    # Replace 'median_family_income' where 'family_member_count' is '1p0c'
    col_df.loc[col_df['family_member_count'] == '1p0c', 'median_family_income'] = col_df['single_no_kid(income)']
    # Replace 'median_family_income' where 'family_member_count' is '2p0c'
    col_df.loc[col_df['family_member_count'] == '2p0c', 'median_family_income'] = col_df['mar_no_kid']
    # Replace 'median_family_income' where 'family_member_count' is '1p1c', '1p2c', '1p3c', '1p4c'
    for count in ['1p1c', '1p2c', '1p3c', '1p4c']:
        col_df.loc[col_df['family_member_count'] == count, 'median_family_income'] = col_df['single_with_kid']
    # Replace 'median_family_income' where 'family_member_count' is '2p1c', '2p2c', '2p3c', '2p4c'
    for count in ['2p1c', '2p2c', '2p3c', '2p4c']:
        col_df.loc[col_df['family_member_count'] == count, 'median_family_income'] = col_df['mar_with_kid']
        
    col_df['housing_cost'] = col_df['housing_cost'] * 1.0898
    col_df['food_cost'] = col_df['food_cost'] * 1.0898
    col_df['transportation_cost'] = col_df['transportation_cost'] * 1.0898
    col_df['healthcare_cost'] = col_df['healthcare_cost'] * 1.0898
    col_df['other_necessities_cost'] = col_df['other_necessities_cost'] * 1.0898
    col_df['childcare_cost'] = col_df['childcare_cost'] * 1.0898
    col_df['taxes'] = col_df['taxes'] * 1.0898
    col_df['total_cost'] = col_df['total_cost'] * 1.0898
    col_df = col_df.dropna()
    col_df = col_df.drop(columns={'mar_with_kid', 'mar_no_kid', 'single_no_kid(income)', 'single_with_kid'})
    col_df = col_df.rename(columns = {'isMetro': 'is_metro'})
    return col_df