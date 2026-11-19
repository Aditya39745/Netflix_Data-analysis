import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("output", exist_ok=True)

# Load Dataset
df = pd.read_csv("netflix_titles.csv")

# Data Cleaning
df.drop_duplicates(inplace=True)

df["type"] = df["type"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["listed_in"] = df["listed_in"].fillna("Unknown")

df["date_added"] = pd.to_datetime(
    df["date_added"].astype("string").str.strip(),
    errors="coerce"
)

# Calculate KPIs
total_titles = len(df)
total_movies = (df["type"] == "Movie").sum()
total_shows = (df["type"] == "TV Show").sum()

countries = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(",").explode().str.strip()
)

total_countries = countries.nunique()

# Chart Data
content_count = df["type"].value_counts()

top_countries = countries.value_counts().head(10)

genres = (
    df["listed_in"].str.split(",").explode().str.strip()
)
top_genres = genres.value_counts().head(10)

yearly_content = (
    df["date_added"].dt.year.value_counts().sort_index()
)

# Create Dashboard
fig = plt.figure(figsize=(16, 10), facecolor="#141414")

fig.suptitle(
    "NETFLIX ANALYTICS DASHBOARD",
    fontsize=25,
    fontweight="bold",
    color="#E50914",
    y=0.98
)

fig.text(
    0.5, 0.93,
    "Movies | TV Shows | Countries | Genres",
    fontsize=12,
    color="white",
    ha="center"
)

# KPI Cards
kpis = [
    ("TOTAL TITLES", total_titles),
    ("TOTAL MOVIES", total_movies),
    ("TV SHOWS", total_shows),
    ("COUNTRIES", total_countries)
]

for i, (label, value) in enumerate(kpis):

    ax = fig.add_axes([
        0.055 + i * 0.23, 0.78, 0.20, 0.10
    ])

    ax.set_facecolor("#252525")
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_color("#E50914")

    ax.text(
        0.5, 0.68, label,
        color="white",
        fontsize=10,
        ha="center"
    )

    ax.text(
        0.5, 0.25, f"{value:,}",
        color="#E50914",
        fontsize=22,
        fontweight="bold",
        ha="center"
    )

# Create Chart Layout
gs = fig.add_gridspec(
    2, 2,
    left=0.07,
    right=0.96,
    bottom=0.08,
    top=0.72,
    hspace=0.38,
    wspace=0.25
)

# Chart 1: Movies vs TV Shows
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor("#252525")

content_count.plot(
    kind="bar",
    ax=ax1,
    color=["#E50914", "#F5F5F5"]
)

ax1.set_title(
    "Movies vs TV Shows",
    color="white",
    fontsize=14
)

ax1.set_xlabel("Content Type", color="white")
ax1.set_ylabel("Number of Titles", color="white")
ax1.tick_params(colors="white")
ax1.grid(axis="y", alpha=0.2)

# Chart 2: Top 10 Countries
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor("#252525")

top_countries.sort_values().plot(
    kind="barh",
    ax=ax2,
    color="#E50914"
)

ax2.set_title("Top 10 Countries", color="white")
ax2.set_xlabel("Number of Titles", color="white")
ax2.tick_params(colors="white")
ax2.grid(axis="x", alpha=0.2)

# Chart 3: Top 10 Genres
ax3 = fig.add_subplot(gs[1, 0])
ax3.set_facecolor("#252525")

top_genres.sort_values().plot(
    kind="barh",
    ax=ax3,
    color="#E50914"
)

ax3.set_title("Top 10 Genres", color="white")
ax3.set_xlabel("Number of Titles", color="white")
ax3.tick_params(colors="white")
ax3.grid(axis="x", alpha=0.2)

# Chart 4: Content Added Per Year
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor("#252525")

yearly_content.plot(
    kind="line",
    ax=ax4,
    color="#E50914",
    marker="o",
    linewidth=2
)

ax4.set_title(
    "Netflix Content Added Per Year",
    color="white"
)

ax4.set_xlabel("Year", color="white")
ax4.set_ylabel("Number of Titles", color="white")
ax4.tick_params(colors="white")
ax4.grid(alpha=0.2)

# Style Charts
for ax in [ax1, ax2, ax3, ax4]:
    for spine in ax.spines.values():
        spine.set_color("#555555")

# Save Dashboard
plt.savefig(
    "output/netflix_dashboard.png",
    dpi=300,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)

plt.close()

# Final Output
print("\n==============================")
print("NETFLIX DASHBOARD CREATED!")
print("==============================")

print("Total Titles:", total_titles)
print("Total Movies:", total_movies)
print("Total TV Shows:", total_shows)
print("Total Countries:", total_countries)

print("\nDashboard saved successfully!")
print("Location: output/netflix_dashboard.png")