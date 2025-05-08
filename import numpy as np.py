import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#imported per the suggestion of copilot
import warnings
warnings.filterwarnings('ignore')

# load the data
df = pd.read_csv("./Lab_11_dataset/student_depression_dataset.csv")

# PART 1: Getting to know the data
print("Dataset shape:", df.shape)
print("\nlooking at the first row:")
print(df.head())

print("\nData Set Info")
print(df.info())

print("\nSome stats about our data:")
print(df.describe())

print("\missing values in the data:")
print(df.isnull().sum())

# PART 2: Clean up

# checking what values we have in some columns
print("\nWhat genders do we have?")
print(df['Gender'].unique())

print("\nDietary habits in the data:")
print(df['Dietary Habits'].unique())

print("\nSleep duration values:")
print(df['Sleep Duration'].unique())

# those quotes are annoying, let's remove them
df['Sleep Duration'] = df['Sleep Duration'].str.replace("'", "")
print("\nSleep duration values after cleaning:")
print(df['Sleep Duration'].unique())

# turning sleep duration into actual numbers
def convert_sleep_duration(sleep):
    is_less_than_5 = sleep == "Less than 5 hours"
    is_5_to_6 = sleep == "5-6 hours"
    is_7_to_8 = sleep == "7-8 hours"
    is_more_than_8 = sleep == "More than 8 hours"
    
    # assign values based on flags
    value = np.nan  # default value
    value = 4.5 if is_less_than_5 else value
    value = 5.5 if is_5_to_6 else value
    value = 7.5 if is_7_to_8 else value
    value = 8.5 if is_more_than_8 else value
    
    return value

df['Sleep Hours'] = df['Sleep Duration'].apply(convert_sleep_duration)

# make yes/no into 1/0 - easier for analysis
df['Suicidal Thoughts'] = df['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
df['Family Mental Illness'] = df['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})

# one-hot encoding for categories
gender = pd.get(df['Gender'], prefix='Gender')
df = pd.concat([df, gender], axis=1)

