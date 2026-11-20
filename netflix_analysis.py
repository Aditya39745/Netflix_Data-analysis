# Netflix and Data Analysis Project
# Libraries: NumPy and Pandas Only

import pandas as pd
import numpy as np

# 1. Load Dataset
df = pd.read_csv("netflix_titles.csv")

print("========== NETFLIX DATA ANALYSIS ==========")

# 2. Dataset Information
print("\n1. Dataset Shape:")
print(df.shape)

print("\n2. First 5 Records:")
print(df.head())

print("\n3. Dataset Information:")
print(df.info())

# 3. Check Missing Values
print("\n4. Missing Values:")
print(df.isnull().sum())

# 4. Data Cleaning
df.drop_duplicates(inplace=True)

df['director'] = df['director'].fillna("Unknown")
df['cast'] = df['cast'].fillna("Unknown")
df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Not Rated")
df['date_added'] = df['date_added'].fillna("Not Available")
df['duration'] = df['duration'].fillna("Not Available")
df['listed_in'] = df['listed_in'].fillna("Unknown")
df['description'] = df['description'].fillna("No Description")

# 5. Total Movies and TV Shows
print("\n5. Total Movies and TV Shows:")
print(df['type'].value_counts())

# 6. Movies Released Per Year
print("\n6. Movies Released Per Year:")
print(df['release_year'].value_counts().sort_index())

# 7. Top 10 Countries
print("\n7. Top 10 Countries:")
print(
    df['country'].str.split(',').explode()
    .str.strip().value_counts().head(10)
)

# 8. Most Popular Directors
print("\n8. Top 10 Directors:")
print(df[df['director'] != 'Unknown']['director']
      .value_counts().head(10))

# 9. Most Popular Actors
print("\n9. Top 10 Actors:")
print(df[df['cast'] != 'Unknown']['cast']
      .str.split(',').explode().str.strip()
      .value_counts().head(10))

# 10. Content Ratings
print("\n10. Content Ratings:")
print(df['rating'].value_counts())

# 11. Movies and TV Shows Added
print("\n11. Content Added by Year:")
date = pd.to_datetime(df['date_added'], errors='coerce')
print(date.dt.year.value_counts().sort_index())

# 12. Most Popular Genres
print("\n12. Top 10 Genres:")
print(df['listed_in'].str.split(',').explode()
      .str.strip().value_counts().head(10))

# 13. Movie Duration Analysis
movies = df[df['type'] == 'Movie'].copy()

movies['duration_minutes'] = pd.to_numeric(
    movies['duration'].str.extract(r'(\d+)')[0],
    errors='coerce'
)

print("\n13. Average Movie Duration:")
print(np.mean(movies['duration_minutes'].dropna()))

print("\n14. Longest Movie:")
print(movies.loc[movies['duration_minutes'].idxmax(),
                 ['title', 'duration']])

# 15. TV Show Seasons Analysis
shows = df[df['type'] == 'TV Show'].copy()

shows['seasons'] = pd.to_numeric(
    shows['duration'].str.extract(r'(\d+)')[0],
    errors='coerce'
)

print("\n15. Average TV Show Seasons:")
print(np.mean(shows['seasons'].dropna()))

# 16. Recent Content
print("\n16. Latest 10 Released Titles:")
print(df.sort_values('release_year', ascending=False)
      [['title', 'type', 'release_year']].head(10))

# 17. Movies vs TV Shows Percentage
print("\n17. Content Percentage:")
print(df['type'].value_counts(normalize=True) * 100)

# 18. Final Dataset
print("\n18. Cleaned Dataset:")
print(df.head())

# 19. Save Cleaned Dataset
df.to_csv("netflix_cleaned.csv", index=False)

print("\nProject Completed Successfully!")
print("Cleaned dataset saved as netflix_cleaned.csv")