import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#imported by the suggestion of copilot
import warnings
warnings.filterwarnings('ignore')

# load the data
df = pd.read_csv("./Lab_11_dataset/student_depression_dataset.csv")

# PART 1: Getting to know the data
print("Dataset shape:", df.shape)
print("\nfirst few rows:")
print(df.head())

print("\ndata set information")
print(df.info())

print("\ndesctption:")
print(df.describe())

print("\n missing stuff")
print(df.isnull().sum())

# PART 2: Cleaning stuff up


print("\nWhat genders do we have?")
print(df['Gender'].unique())

print("\nDietary habits in the data:")
print(df['Dietary Habits'].unique())

print("\nSleep duration values:")
print(df['Sleep Duration'].unique())

df['Sleep Duration'] = df['Sleep Duration'].str.replace("'", "")
print("\nSleep duration values after cleaning:")
print(df['Sleep Duration'].unique())

# turning sleep duration into actual numbers
def convert_sleep_duration(sleep):
    is_less_than_5 = sleep == "Less than 5 hours"
    is_5_to_6 = sleep == "5-6 hours"
    is_7_to_8 = sleep == "7-8 hours"
    is_more_than_8 = sleep == "More than 8 hours"
    
    # assign values based on flags (autofilled by copilot)
    value = np.nan  # default value
    value = 4.5 if is_less_than_5 else value
    value = 5.5 if is_5_to_6 else value
    value = 7.5 if is_7_to_8 else value
    value = 8.5 if is_more_than_8 else value
    
    return value

df['Sleep Hours'] = df['Sleep Duration'].apply(convert_sleep_duration)

# make yes/no into 1/0
df['Suicidal Thoughts'] = df['Have you ever had suicidal thoughts ?'].map({'Yes': 1, 'No': 0})
df['Family Mental Illness'] = df['Family History of Mental Illness'].map({'Yes': 1, 'No': 0})

# encoding for categories
gender = pd.get_dummies(df['Gender'], prefix='Gender')
df = pd.concat([df, gender], axis=1)

# PART 3: EDA
# depressed vs not depressed
print("\nDepression counts:")
print(df['Depression'].value_counts())
print(df['Depression'].value_counts(normalize=True).round(2))

plt.figure(figsize=(8, 5))
sns.countplot(x='Depression', data=df)
plt.title('Depression Distribution')
plt.savefig('depression_distribution.png')
plt.close()

# Age 
plt.figure(figsize=(10, 6))
sns.histplot(data=df, x='Age', kde=True)
plt.title('How old are these students?')
plt.savefig('age_distribution.png')
plt.close()

# Depression vs Age 
plt.figure(figsize=(10, 6))
sns.boxplot(x='Depression', y='Age', data=df)
plt.title('Depression vs Age')
plt.savefig('depression_vs_age.png')
plt.close()

# men vs women
plt.figure(figsize=(10, 6))
sns.countplot(x='Gender', hue='Depression', data=df)
plt.title('Depression by Gender')
plt.savefig('depression_by_gender.png')
plt.close()

# academic
plt.figure(figsize=(10, 6))
sns.boxplot(x='Depression', y='Academic Pressure', data=df)
plt.title('Depression vs Academic Pressure')
plt.savefig('depression_vs_academic_pressure.png')
plt.close()

# sleep
plt.figure(figsize=(10, 6))
sns.boxplot(x='Depression', y='Sleep Hours', data=df)
plt.title('Depression vs Sleep Hours')
plt.savefig('depression_vs_sleep.png')
plt.close()

# sleep2
plt.figure(figsize=(12, 6))
sns.countplot(x='Sleep Duration', hue='Depression', data=df)
plt.title('Depression by Sleep Duration')
plt.xticks(rotation=45)  # text was overlapping
plt.savefig('depression_by_sleep_duration.png')
plt.close()

# money
plt.figure(figsize=(10, 6))
sns.boxplot(x='Depression', y='Financial Stress', data=df)
plt.title('Depression vs Financial Stress')
plt.savefig('depression_vs_financial_stress.png')
plt.close()

# study hours
plt.figure(figsize=(10, 6))
sns.boxplot(x='Depression', y='Study Satisfaction', data=df)
plt.title('Depression vs Study Satisfaction')
plt.savefig('depression_vs_study_satisfaction.png')
plt.close()

# thoughts
plt.figure(figsize=(10, 6))
sns.countplot(x='Have you ever had suicidal thoughts ?', hue='Depression', data=df)
plt.title('Depression by Suicidal Thoughts')
plt.savefig('depression_by_suicidal_thoughts.png')
plt.close()

# Family history connection
plt.figure(figsize=(10, 6))
sns.countplot(x='Family History of Mental Illness', hue='Depression', data=df)
plt.title('Depression by Family History of Mental Illness')
plt.savefig('depression_by_family_history.png')
plt.close()

# food vs mood
plt.figure(figsize=(10, 6))
sns.countplot(x='Dietary Habits', hue='Depression', data=df)
plt.title('Depression by Dietary Habits')
plt.savefig('depression_by_dietary_habits.png')
plt.close()

# Correlation
numeric_cols = ['Age', 'Academic Pressure', 'Work Pressure', 'GPA', 
                'Study Satisfaction', 'Job Satisfaction', 'Sleep Hours',
                'Work/Study Hours', 'Financial Stress', 'Suicidal Thoughts',
                'Family Mental Illness', 'Depression']

# Make the correlation matrix (assisted by copilot)
correlation_matrix = df[numeric_cols].corr()

#heatmap
plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.savefig('correlation_heatmap.png')
plt.close()

# Pair plot
selected_vars = ['Age', 'Academic Pressure', 'Sleep Hours', 'Financial Stress', 'Depression']
plt.figure(figsize=(15, 10))
sns.pairplot(df[selected_vars], hue='Depression')
plt.suptitle('Pair Plot of Selected Variables', y=1.02)
plt.savefig('pair_plot.png')
plt.close()