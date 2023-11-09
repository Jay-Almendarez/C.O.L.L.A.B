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
    # Acquire Commute Data
    commute = pd.read_csv('B08303_2022_commute.csv')
    
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
    family.msa = family.msa.str.replace('Nashville-Davidson--Murfreesboro--Franklin, TN MSA', 'Nashville-Davidson–Murfreesboro–Franklin, TN MSA')
    family.msa = family.msa.str.replace('Scranton--Wilkes-Barre, PA MSA',
                                        'Scranton–Wilkes-Barre, PA MSA')
    
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
    
    # add affordability ratio column to col_df
    col_df['affordability_ratio'] = round(col_df.median_family_income / col_df.total, 2)

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
    cost = col_df[['msa', 'parents', 'children', 'housing', 'food', 'transportation', 'healthcare', 'other', 'childcare', 'taxes', 'total', 'median_family_income', 'affordability_ratio']]
    
    ####### Prep commute data #######
    commute = commute.T
    commute.reset_index(inplace=True)
    commute.columns = commute.iloc[0]
    commute = commute.iloc[1:]
    commute.rename(columns={'Label (Grouping)':'msa',
                            'Total:':'total_commute',
                            '\xa0\xa0\xa0\xa0Less than 5 minutes': 'under_5',
                            '\xa0\xa0\xa0\xa05 to 9 minutes': '5-9',
                            '\xa0\xa0\xa0\xa010 to 14 minutes': '10-14',
                            '\xa0\xa0\xa0\xa015 to 19 minutes': '15-19',
                            '\xa0\xa0\xa0\xa020 to 24 minutes': '20-24',
                            '\xa0\xa0\xa0\xa025 to 29 minutes': '25-29',
                            '\xa0\xa0\xa0\xa030 to 34 minutes': '30-34',
                            '\xa0\xa0\xa0\xa035 to 39 minutes': '35-39',
                            '\xa0\xa0\xa0\xa040 to 44 minutes': '40-44', 
                            '\xa0\xa0\xa0\xa045 to 59 minutes': '45-59',
                            '\xa0\xa0\xa0\xa060 to 89 minutes': '60-89',
                            '\xa0\xa0\xa0\xa090 or more minutes': '90+'}, inplace=True)
    commute.msa = commute.msa.str.replace('Metro Area!!Estimate', 'MSA')
    commute.msa = commute.msa.str.replace('Micro Area!!Estimate', 'MSA')

    columns = ['total_commute', 'under_5', '5-9', '10-14', '15-19', '20-24',
       '25-29', '30-34', '35-39', '40-44', '45-59', '60-89', '90+']
    for col in columns:
        commute[col] = commute[col].str.replace(',', '').astype(float)
    
    # Estimate an average commute time for each MSA by multiply the count of commuters by the midpoint of the range and dividing by the total number of commuters  
    commute['est_commute'] = (commute['under_5'] * 2.5 + commute['5-9'] * 7 + commute['10-14'] * 12 + commute['15-19'] * 17 + commute['20-24'] * 22 + commute['25-29'] * 27 + commute['30-34'] * 32 + commute['35-39'] * 37 + commute['40-44'] * 42 + commute['45-59'] * 52 + commute['60-89'] * 74.5 + commute['90+'] * 90)/commute['total_commute']
    ## Merge commute to cost
    cost = pd.merge(cost, commute, on='msa', how='left')
    
    ####### Clean the FBI Data #######
    # acquire fbi data
    fbi = pd.read_csv('fbi_table6_2019.csv')
    # Make column names of fbi lowercase
    fbi.columns = fbi.columns.str.lower()
    # Rename columns
    fbi.rename(columns= {'metropolitan statistical area': 'msa',
                     'violent\ncrime': 'violent_crime',
                     'murder and\nnonnegligent\nmanslaughter': 'murder_and_nonnegligent_manslaughter',
                     'rape1': 'rape',
                     'aggravated\nassault':'aggravated_assault',
                     'property\ncrime': 'property_crime',
                     'larceny-\ntheft': 'larceny_theft',
                     'motor\nvehicle\ntheft':'motor_vehicle_theft'}, inplace=True)
    # Ffill msa
    fbi['msa'].fillna(method='ffill', inplace=True)

    # drop all rows from fbi where fbi['counties/principal cities'] != Rate per 100,000 inhabitants
    fbi = fbi[fbi['counties/principal cities'] == 'Rate per 100,000 inhabitants']
    # format fbi.msa to merge onto cost
    fbi.msa = fbi.msa.str.replace('M.S.A.', 'MSA')
    fbi.msa = fbi.msa.str.replace('M.S.A', 'MSA')
    fbi['msa'] = fbi['msa'].replace(r'MSA\d+$', 'MSA', regex=True)
    fbi.msa = fbi.msa.str.replace('MSA2, 3', 'MSA')
    fbi.msa = fbi.msa.str.replace('MSA3, 4', 'MSA')
    fbi.msa = fbi.msa.str.replace('Poughkeepsie-Newburg-Middletown', 'Poughkeepsie-Newburgh-Middletown')
    

    ####### Merge FBI to Cost #########
    epi_census = cost.copy()
    cost = pd.merge(cost, fbi, on='msa', how='left')
    cost = cost[cost.violent_crime.notnull()]
    
    # fix dtypes for the columns from FBI
    cost = cost.drop(columns = {'counties/principal cities'})
    columns = ['violent_crime', 'murder_and_nonnegligent_manslaughter', 'rape', 'robbery', 'aggravated_assault', 'property_crime', 'burglary', 'larceny_theft', 'motor_vehicle_theft']

    for col in columns:
        cost[col] = cost[col].str.replace(',', '').astype(float)
    
    ####### Internet #########
    intern = pd.read_csv('internet.csv')
    intern = intern.T

    # make the index of intern the first column
    intern.reset_index(inplace = True)

    # rename the first column to 'msa'
    intern.rename(columns = {'index':'msa'}, inplace = True)

    # in family.msa replace Metro Area!!Estimate with MSA
    intern['msa'] = intern['msa'].str.replace('Metro Area!!Percent', 'MSA')

    # in col.msa replace HUD Metro FMR Area with MSA
    intern.msa = intern.msa.str.replace('HUD Metro FMR Area', 'MSA')

    intern = intern.T
    internet = intern[171:173]
    edu_above_25 = intern[68:77]
    edu_enrolled = intern[61:66]
    joined_intern = pd.concat([internet, edu_above_25, edu_enrolled], ignore_index=True, axis = 0).T
    intern = pd.concat([intern.T.msa, joined_intern], ignore_index=True, axis = 1)
    intern.columns = intern.iloc[0]
    intern = intern.drop(intern.index[0])
    intern.columns = intern.columns.str.lower().str.replace(',', '').str.replace(' ', '_').str.strip().str.replace('(', '').str.replace(')', '').str.replace("'", "")
    intern = intern.rename(columns={'label_grouping':'msa'})
    intern= intern.fillna(0)
    numerical_columns = intern.columns[1:]
    for um in numerical_columns:
        intern[um] = intern[um].str.strip('%').astype(float)
    intern['less_than_high_school'] = intern['less_than_9th_grade']	+ intern['9th_to_12th_grade_no_diploma']
    intern['highschool_grad_rate'] = 100 - intern['less_than_high_school']
    intern['high_school_to_associates'] = intern['high_school_graduate_includes_equivalency'] + intern['some_college_no_degree'] + intern['associates_degree']
    intern['bachelors_plus'] = intern['bachelors_degree'] + intern['graduate_or_professional_degree']
    intern = intern.drop(columns = {'less_than_9th_grade', '9th_to_12th_grade_no_diploma',
           'high_school_graduate_includes_equivalency', 'some_college_no_degree',
           'associates_degree', 'bachelors_degree',
           'graduate_or_professional_degree', 'high_school_graduate_or_higher',
           'bachelors_degree_or_higher'})
    intern = intern.rename(columns = {'label_grouping':'msa', 'with_a_computer':'homes_with_computer',
                             'with_a_broadband_internet_subscription':'homes_with_internet',  
                             'nursery_school_preschool': 'in_preschool', 'kindergarten': 'in_kindergarten', 'elementary_school_grades_1-8': 'in_junior_high', 
                             'high_school_grades_9-12': 'in_high_school', 'college_or_graduate_school': 'in_college_plus' })

    
    
    ####### Merge intern to Cost #########
    cost = pd.merge(cost, intern, on='msa', how='left')
    cost = cost[cost.violent_crime.notnull()]

    cost = cost.drop(columns = {'population'})
    cost = cost.dropna()
    
    
    ####### Population #########
    pop = pd.read_csv('pop.csv')
    pop.rename(columns = {'Geographic Area Name (Grouping)' :'msa'}, inplace=True)
    pop.msa = pop.msa.str.replace('Micro Area','MSA')
    pop.msa = pop.msa.str.replace('Metro Area','MSA')
    pop = pop.drop(columns = {'4/1/2010 population estimates base!!Population', '4/1/2010 Census population!!Population'})
    pop = pop.T
    pop.index = pop.index.str.replace('estimate!!Population','')
    pop.index = pop.index.str.replace('7/1/','')
    pop = pop.T
    
    ####### Merge Population to Cost #########
    cost = pd.merge(cost, pop, on='msa', how='left')
    
    return cost, epi_census, fbi, intern, commute, pop