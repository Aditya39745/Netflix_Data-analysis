import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("output", exist_ok=True)

# Load Dataset
df = pd.read_csv("netflix_titles.csv")

# Data Cleaning
df.drop_duplicates(inplace=True)

df['date_added'] = pd.to_datetime(
    df['date_added'].str.strip(),
    errors='coerce'
)

df['release_year'] = pd.to_numeric(
    df['release_year'], errors='coerce'
)

df['type'] = df['type'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')
df['listed_in'] = df['listed_in'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Not Rated')
df['director'] = df['director'].fillna('Unknown')

# Basic Information
print("\n========== NETFLIX DATA ANALYSIS ==========")

print("\nTotal Records:", len(df))
print("Total Movies:", (df['type'] == 'Movie').sum())
print("Total TV Shows:", (df['type'] == 'TV Show').sum())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

# 1. Movies vs TV Shows
content_count = df['type'].value_counts()

plt.figure(figsize=(8, 5))
plt.bar(content_count.index, content_count.values)
plt.title("Movies vs TV Shows")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("output/content_type.png")
plt.show()

# 2. Top 10 Countries
countries = df[df['country'] != 'Unknown']['country'].str.split(', ').explode()
top_countries = countries.value_counts().head(10)

plt.figure(figsize=(10, 5))
plt.bar(top_countries.index, top_countries.values)
plt.title("Top 10 Countries on Netflix")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/top_countries.png")
plt.show()

# 3. Content Released Each Year
yearly_content = df['release_year'].dropna().astype(int).value_counts().sort_index()

plt.figure(figsize=(12, 5))
plt.plot(yearly_content.index, yearly_content.values)
plt.title("Netflix Content Released Each Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid()
plt.tight_layout()
plt.savefig("output/yearly_content.png")
plt.show()

# 4. Top 10 Genres
genres = df['listed_in'].str.split(', ').explode()
top_genres = genres.value_counts().head(10)

plt.figure(figsize=(10, 5))
plt.barh(top_genres.index, top_genres.values)
plt.title("Top 10 Netflix Genres")
plt.xlabel("Number of Titles")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/top_genres.png")
plt.show()

# 5. Top 10 Directors
directors = df[df['director'] != 'Unknown']['director'].str.split(', ').explode()
top_directors = directors.value_counts().head(10)

plt.figure(figsize=(10, 5))
plt.barh(top_directors.index, top_directors.values)
plt.title("Top 10 Directors on Netflix")
plt.xlabel("Number of Titles")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("output/top_directors.png")
plt.show()

# 6. Rating Distribution
ratings = df['rating'].value_counts().head(10)

plt.figure(figsize=(9, 5))
plt.bar(ratings.index, ratings.values)
plt.title("Netflix Content Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("output/ratings.png")
plt.show()

# 7. Movies and TV Shows Added Per Year
df['added_year'] = df['date_added'].dt.year

added_year = df.groupby(
    ['added_year', 'type']
).size().unstack(fill_value=0)

added_year = added_year.dropna(how='all')

added_year.plot(figsize=(10, 5))
plt.title("Movies and TV Shows Added Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.grid()
plt.tight_layout()
plt.savefig("output/added_per_year.png")
plt.show()

# Final Summary
print("\n========== PROJECT SUMMARY ==========")

print("Most Common Content Type:", content_count.idxmax())
print("Top Country:", top_countries.index[0])
print("Most Popular Genre:", top_genres.index[0])
print("Top Director:", top_directors.index[0])
print("Most Common Rating:", ratings.index[0])

print("\nAll graphs saved in the output folder.")
print("\nNetflix Data Analysis Completed Successfully!")

# 8. Top 10 Countries on Netflix

country_counts = df[
    df['country'] != 'Unknown'
]['country'].dropna().str.split(', ').explode()

top_countries = country_counts.value_counts().head(10)

plt.figure(figsize=(10, 5))
top_countries.plot(kind='bar', color='orange')

plt.title('Top 10 Countries on Netflix')
plt.xlabel('Country')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "output/top_10_countries_orange.png",
    dpi=300,
    bbox_inches='tight'
)

plt.close()

print("All 8 graphs saved successfully!")