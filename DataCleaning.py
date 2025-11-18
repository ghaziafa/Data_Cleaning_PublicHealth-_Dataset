#Data_cleaning

import pandas as pd
import numpy as np
import re #re stands for regular expressions.
#Regular expressions are a powerful way to search, match, and manipulate text based on patterns.
#In this code, I use it to extract numeric values from messy strings.
df = pd.read_csv(r"C:\Users\User\Downloads\Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System.csv")
print(df.shape)
df.head()
df.info()

#------Checking numerical_columns and converting problemetic values into NaN------
def safe_numeric(x):   #Converts x to numeric only if it looks numeric. Leaves all other text unchanged.
    if pd.isna(x) or x == '': 
        return np.nan  #if x is missing or empty, return NaN immediately. This ensures we don’t try to process missing values — they stay as NaN
    x_clean = str(x).replace(',','').replace('%','').strip()  #it will convert "x" whatever it is into a string+remove commas+remover percentage sign+ extra empty spaces.
### Extracting Numerical Values from strings using "Regex Method"
   
    match = re.search(r'[-+]?\d*\.\d+|\d+', x_clean)  #re.search() looks for the first occurrence of the pattern in the string x_clean
    if match:
        return float(match.group()) #match.group() returns the matched string, e.g., "12.5", float(...) will convert it to a float point.
    else:
        return x
column_to_process = []
for col in df.columns:
    sample = df[col].dropna().astype(str).head(1000)
    numeric_col = sample.str.contains(r'\d').any()   #.str.contains() searches each value for a pattern.\d means "any digit" (0–9)
    if numeric_col:
        column_to_process.append(col)
print("Colunms detected for numeric conversion:", column_to_process)
df.shape

# Converting non_numeric into Nan
for col in column_to_process:
    df[col] = df[col].apply(safe_numeric)
    print(f"Processed column: {col}")

#------Standardise text: e.g Location names------
string_col = df.select_dtypes(include = ['object']).columns
for col in string_col:
    df[col] = df[col].astype(str).str.strip().str.title()
df.shape

#------handeling missing values------
print(df.isna().sum())
#dropping all columns with too many missing values
df = df.dropna(thresh = 0.7*len(df), axis = 1) #axis=1 means column_wise dropping
#dropping rows with missing values from the columns with most missing values
important_cols = ['Data_Value','Sample_Size','Low_Confidence_Limit','High_Confidence_Limit ']
df = df.dropna(subset= important_cols)
df.shape

#------Handeling Duplicates------
df = df.drop_duplicates()
df.shape

#handeling outliners
# Clean column names
df.columns = df.columns.str.strip()

# Drop duplicates
df = df.drop_duplicates()

# Convert numeric columns safely
numeric_cols = ['Data_Value', 'Low_Confidence_Limit', 'High_Confidence_Limit', 'Sample_Size']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove outliers for numeric columns
for col in numeric_cols:
    df = df[(df[col].isna()) | ((df[col] >= 0) & (df[col] <= 100))]

print("Rows remaining:", df.shape[0])
df.shape

#------Standardisation & Nomarlisation------

string_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in string_cols:
    df[col] = df[col].astype(str).str.strip().str.lower()

#------extracting meaningful information into new columns-----
#extract age / gender / race / income / education

df.columns = df.columns.str.strip().str.lower()
df['age_group']=df['stratification1'].where(df['stratificationcategory1']=='age(years)')
df['gender']=df['stratification1'].where(df['stratificationcategory1']=='gender')
df['income_level']=df['stratification1'].where(df['stratificationcategory1']=='income')
df['education_level']= df['stratification1'].where(df['stratificationcategory1']=='education')
df['race_ethnicity'] = df['stratification1'].where(df['stratificationcategory1']=='race/ethnicity')
#cleaning new column e.g, space inbetween or casing
cols = ['age_group','gender','income_level','education_level','race_ethnicity']
for col in cols:
    df[col]= df[col].astype(str).str.strip().str.lower()
    df[col]=df[col].astype('category')


# Check that sample_size is positive
df = df[df['sample_size'] > 0]


# Drop irrelevant columns
cols_to_drop = ['data_value_alt','footnote_symbol','geolocation']  # example
df.drop(columns=cols_to_drop, axis=1, inplace=True, errors='ignore')
df.shape

#EXPORT CLEAN DATA
df.to_csv("BRFSS_nutrition_physical_activity_clean.csv", index=False)
print("✅ Cleaned dataset saved.")
