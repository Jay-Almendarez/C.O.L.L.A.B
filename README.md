# C.O.L.L.A.B
<hr style="border:2px solid black">

## <u>Project Description</u>
The United States of America is a huge place, full of countless areas unique in culture and brimming with city life. For our project, we wanted to give prospective movers a tool to guide them to the best areas to live for them and their families. To accomplish this, we took data from various government agencies like the Economic Policy Institute, the FBI and the Census Bureau. With this data collected, we will allow families to make selections that matter the most to them and suggest areas in the US that best fit those criteria. 

## Goals: 
* Create an interactive dashboard to assist families with moving
* Create and implement additional fetures like safety measure, commute time, and internet accessibility 

<hr style="border:2px solid black">

# Initial Thoughts
 
* Areas with high affordability will have lower safety scores
* Just because somewhere is cheaper doesn't imply affordability
 
<hr style="border:2px solid black"> 


# Data Dictionary
| Feature               | Definition |
|:----------------------|:-----------|
| msa | Metropolitan Statistical Area |
| parents | Number of parents in family |
| children | Number of children in family |
| housing | Estimated housing costs for each family type |
| food | Estimated food costs for each family type |
| transportation | Estimated transportation costs for each family type |
| healthcare | Estimated healthcare costs for each family type |
| other | Estimated miscellaneous costs  for each family type |
| childcare | Estimated childcare costs for each family type |
| taxes | Estimated taxes for each family type |
| total | Total of estimated costs for each family type |
| median_family_income | Median income for each family type |
| affordability_ratio | Ratio comparing family income to total costs associated with family type|
| total_commute | Total Commute time on MSA level |
| under_5 | Count of how many people's commute time is less than 5 minutes |
| 5-9 | Count of how many people's commute time is between 5 and 9 minutes |
| 10-14 | Count of how many people's commute time is between 10 and 14 minutes |
| 15-19 | Count of how many people's commute time is between 15 and 19 minutes |
| 20-24 | Count of how many people's commute time is between 20 and 24 minutes |
| 25-29 | Count of how many people's commute time is between 25 and 29 minutes |
| 30-34 | Count of how many people's commute time is between 30 and 34 minutes |
| 35-39 | Count of how many people's commute time is between 35 and 39 minutes |
| 40-44 | Count of how many people's commute time is between 40 and 44 minutes |
| 45-59 | Count of how many people's commute time is between 45 and 59 minutes |
| 60-89 | Count of how many people's commute time is between 60 and 89 minutes |
| 90+ | Count of how many people's commute time is greater than 90 minutes |
| est_commute | Average commute time |
| violent_crime | Total occurences of violent crimes (i.e murder, rape, aggravated assault) per 100,000 people |
| murder_and_nonnegligent_manslaughter | Reported cases of murder per 100,000 people |
| rape | Reported cases of rape per 100,000 people |
| robbery | Reported cases of robbery per 100,000 people |
| aggravated_assault | Reported cases of aggracated assault per 100,000 people |
| property_crime | Total occurences of property crimes (i.e burglary, robbery, larceny theft, motor vehicle theft) per 100,000 people |
| burglary | Reported cases of burglary per 100,000 people |
| larceny_theft | Reported cases of larceny per 100,000 people |
| motor_vehicle_theft | Reported cases of vehicle theft per 100,000 people |
| homes_with_computer | Percent of households with at least one computer |
| homes_with_internet | Percent of households with broadband internet |
| in_preschool | Percent of area population currently in preschool |
| in_kindergarten | Percent of area population currently in kindergarten |
| in_junior_high | Percent of area population currently in junior high |
| in_high_school | Percent of area population currently in high school |
| in_college_plus | Percent of area population currently in college |
| less_than_high_school | Percent of area population with less than high school education |
| high_school_to_associates | Percent of area population with high school or some college education |
| bachelors_plus | Percent of area population with bachelors or higher education |
| family_type | Unique family type breakdown for MSA |

<hr style="border:2px solid black"> 


# The Plan
 
Plan --> Acquire --> Prepare --> Explore --> Model --> Deliver
 

#### Acquire
    * Determine additional dataframes to increase selectable features
    * Confirm viability of merging with original dataframe
    * Store additional dataframes as csv to bring into notebook
#### Prepare
    * Clean dataframes in anticipation of merging datasets
    * Create aggregate features from listed features
    * Merge dataframes
    * Apply MinMax Scaler to data
#### Explore
##### Before Clustering
    * Begin feature selection and narrow down on target(s)
    * Perform initial comparisons to determine meaningful pairs of features
##### After Clustering
    * Perform comparisons on clustered data 
    * Determine statistical signifance of pairings as a result of defined clusters
#### Deliver
    * Develop an interactive dashboard where families can select features they deem the most important

<hr style="border:2px solid black"> 

# Steps to Reproduce
>1) Download collab_csv.zip and wrangle.py into same folder
>2) Open zipped file and run wrangle function in notebook
<hr style="border:2px solid black"> 
 
### <u>Recommendations:</u>

>* Affordability is extremely important, but considering outside factors can help shape the ideal community for you.
>* Families should keep an open mind when looking at ideal places to move to. (Maybe what's best for your family is somewhere you never imagined yourself living)

### <u>Next Steps:</u>

>* Find additional dataframes to continue adding possible features for families to select
>* Take analysis to county level for increased granularity
>* Develop dashboard into website or app for easier access
