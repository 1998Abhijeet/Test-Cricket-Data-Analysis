import pandas as pd 
import pprint
import sys
import re

# Debugging function
def debu(param):
    pprint.pprint(param)  
    sys.exit()

# Load the dataset
df = pd.read_csv('Cricket_data.csv')
# debu(df)

# Rename the multiple column headers in the dataset
df = df.rename(columns={
    'Mat': 'Matches',
    'Inns': 'Innings',
    'NO': 'Not Out',
    'HS': 'Highest Score',
    'Ave': 'Average',
    'BF': 'Ball Faced',
    'SR': 'Strike Rate',
    '100': '100s',
    '50': '50s',
    '0': '0s'
})
# print(new_name.head())

# Check for null values in the dataset
null_check = df.isnull().any()
# print(null_check)

# Fill 0 where null value is there
df['Ball Faced'] = df['Ball Faced'].fillna(0)
df['Strike Rate'] = df['Strike Rate'].fillna(0)

# Remove '+' sign from 'Ball Faced' column
df['Ball Faced'] = df['Ball Faced'].str.replace('+', '', regex=False)

# Convert 'Ball Faced' and 'Highest Score' to integer
df['Ball Faced'] = pd.to_numeric(df['Ball Faced'], errors='coerce').fillna(0).astype(int)
df['Highest Score'] = pd.to_numeric(df['Highest Score'], errors='coerce').fillna(0).astype(int)
# Now check if the operations worked, e.g., filtering a specific player's data
player_data = df[df['Player'] == 'ED Weekes (WI)']
# print(player_data)

### Remove Duplicate data from dataset
# print("-------------------------- Duplicate Data -----------------------------------")
duplicate_data=df[df['Player'].duplicated()]
# print(duplicate_data)

duplicate=df[df['Player'].isin(['E Paynter (ENG)','ED Weekes (WI)','MJ Clarke (AUS)'])]
# print(duplicate)

##Remove Duplicate data
df=df.drop_duplicates()
# print("------------------------------------------------ Unique Data --------------------------------")
unique_data=df[df['Player'].isin(['E Paynter (ENG)','ED Weekes (WI)','MJ Clarke (AUS)'])]
# print(unique_data)

## Split up 'Span' into 'Start Year' and 'End Year'
df[['Start Year', 'End Year']] = df['Span'].str.split('-', expand=True)

# Remove the 'Span' column
df = df.drop(columns=['Span'])

# Convert 'Start Year' and 'End Year' to integers
df['Start Year'] = df['Start Year'].astype(int)
df['End Year'] = df['End Year'].astype(int)

# Calculate the 'Number_of_Service'
df['Number_of_Service'] = df['End Year'] - df['Start Year']

# Extract country name from 'Player' column and create a new 'Country Name' column
df['Country Name'] = df['Player'].apply(lambda x: re.search(r'\((.*?)\)', x).group(1))

# Remove country name from 'Player' column
df['Player'] = df['Player'].apply(lambda x: re.sub(r'\s*\(.*?\)', '', x))

### Check datatypes
df_types = df.dtypes
print(df_types)

# print(df)
# Save the cleaned DataFrame to a CSV file
# df.to_csv('Cleaned_Cricket_data.csv', index=False)

### Find some important insights from cleaned data
## Insight:1 Calculate average service 
print("----------------------------------------------------------IMPORTANT INSIGHTS ------------------------------------")
average_service=df['Number_of_Service'].mean()
print("Average of Service =",average_service)

## Insight:2 Average Batting Strike Rate for cricketers who played over 10 years
average_strikerate=df[df['Number_of_Service']>10]['Strike Rate'].mean()
print("Average Batting Strike Rate whose service more than 10 years = ",average_strikerate)

## Insight:3 Find Number of players who played before 1960
number_of_players = df[df['Start Year'] < 1960]['Player'].count()
print("Number of players who played before year 1960 =", number_of_players)

## Insight:4 Maximum Highest Innings Score by country
highest_innings = df.groupby('Country Name')['Highest Score'].max().to_frame('High_inn_Score').sort_values('High_inn_Score',ascending=False)
print("Maximum Highest Innings Score by country:\n", highest_innings)

## Insight:5  Hundreds, Fifties, ducks average by country
average=df.groupby('Country Name')[['100s','50s','0s']].mean()
print(average)

## Insight:6 Find player name with highest average from each country
highest_avg_players = df.loc[df.groupby('Country Name')['Average'].idxmax()]
result = highest_avg_players[['Player', 'Average', 'Country Name']]
print("Player with the highest average from each country:\n", result)
