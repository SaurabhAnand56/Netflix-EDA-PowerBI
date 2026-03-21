# 🎬 Netflix Content Analysis — EDA + Power BI Dashboard

> *"I picked Netflix because almost everyone has used it — and I wanted to work on a dataset that actually feels real, not just another iris or titanic."*

This is my **2nd EDA + Power BI project**, built end-to-end from raw CSV to a fully interactive 3-page dashboard. The idea was simple — take a messy real-world dataset, clean it up properly, explore it through Python, and then build something visual that tells a story. No shortcuts.

---

## 🔗 Quick Links

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saurabhanand56/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SaurabhAnand56)
[![Power BI Dashboard](https://img.shields.io/badge/Live%20Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://app.powerbi.com/view?r=eyJrIjoiZDk4YmJmYjQtMjA5NC00NjI4LTg0OTMtOTU5NWMxOGRkYzgxIiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9)

---

## 📁 Project Structure

```
Netflix-EDA/
│
├── dataset/
│   └── netflix_titles.csv               # Raw dataset — 8,808 rows, 12 columns
│
├── notebook/
│   └── Netflix-dataset-eda.ipynb        # Full EDA notebook (10 steps)
│
├── images/
│   ├── content_overview.png             # Dashboard Page 1 screenshot
│   ├── trends_and_growth.png            # Dashboard Page 2 screenshot
│   └── deev_dive.png                    # Dashboard Page 3 screenshot
│
├── powerbi/
│   └── Netflix_Dashboard.pbix           # Power BI file
│
└── README.md
```

---

## 📊 Live Dashboard Preview

### Page 1 — Content Overview
![Content Overview](images/content_overview.png)

### Page 2 — Trends & Growth
![Trends & Growth](images/trends_and_growth.png)

### Page 3 — Deep Dive
![Deep Dive](images/deev_dive.png)

---

## 🗂️ About the Dataset

The dataset is publicly available on Kaggle — it contains every Movie and TV Show available on Netflix up to 2021. 8,808 titles, 12 columns, and a surprising amount of missing data (especially in the `director` column — nearly 30% blank).

| Column | What it holds |
|---|---|
| `show_id` | Unique ID per title |
| `type` | Movie or TV Show |
| `title` | Name |
| `director` | Director (missing for ~30% of titles) |
| `cast` | Main cast |
| `country` | Country of origin |
| `date_added` | When it was added to Netflix |
| `release_year` | Original release year |
| `rating` | Content rating (TV-MA, PG-13, R, etc.) |
| `duration` | Minutes for movies / seasons for shows |
| `listed_in` | Genre tags (comma-separated) |
| `description` | Short plot summary |

---

## 🐍 EDA — What I Did in the Notebook

The notebook follows a structured 10-step flow. I tried to write it in a way that makes sense even if you're new to EDA — each section explains what I'm doing and why, before jumping into code.

| Step | What's covered |
|---|---|
| 1 | Introduction — dataset overview, goals |
| 2 | Import libraries |
| 3 | Load & first look at data |
| 4 | Data cleaning — fix types, extract numbers from text |
| 5 | Missing values — where the gaps are and how I handled them |
| 6 | Univariate analysis — one column at a time |
| 7 | Bivariate analysis — finding relationships between columns |
| 8 | Visualizations — charts that tell the actual story |
| 9 | Key insights — what the data is saying |
| 10 | Conclusion + next steps |

### How to run it locally

```bash
# Clone the repo
git clone https://github.com/SaurabhAnand56/netflix-eda-powerbi.git
cd netflix-eda-powerbi

# Install dependencies
pip install pandas numpy matplotlib seaborn jupyter

# Launch the notebook
jupyter notebook notebook/Netflix-dataset-eda.ipynb
```

> Make sure `netflix_titles.csv` is inside the `dataset/` folder before running.

---

## 📈 Power BI Dashboard

Built a 3-page interactive dashboard in Power BI with a full Netflix dark theme (`#141414` background, `#E50914` red accents). Used Power Query for data transformation and DAX for custom measures.

### What's on each page

**Page 1 — Content Overview**
- 6 KPI cards: Total Titles, Movies, TV Shows, Countries, Titles in 2019, Peak Year
- Donut chart: Movies vs TV Shows split
- Bar chart: Top 10 Genres
- Bar chart: Top 10 Countries
- Slicers: Filter by Rating and Type

**Page 2 — Trends & Growth**
- Line chart: Netflix library growth from 2015 to 2021
- Area chart: Movies vs TV Shows added each year
- Matrix heatmap: Monthly content additions — darker red = more content added
- Year range slicer

**Page 3 — Deep Dive**
- KPI cards: Avg Movie Duration (100 min), Most Common Rating (TV-MA)
- Grouped bar: Content ratings breakdown by type
- Column chart: TV Shows by number of seasons
- Bar chart: Avg movie duration by rating
- Scrollable table: Browse all titles with filters

### DAX Measures I wrote

```dax
Total Titles = COUNTROWS(netflix_titles)

Total Movies = CALCULATE(COUNTROWS(netflix_titles), netflix_titles[type] = "Movie")

Total TV Shows = CALCULATE(COUNTROWS(netflix_titles), netflix_titles[type] = "TV Show")

Total Countries = DISTINCTCOUNT(netflix_titles[country])

Avg Movie Duration =
    ROUND(
        CALCULATE(AVERAGE(netflix_titles[duration_minutes]),
        netflix_titles[type] = "Movie"),
    0)

Titles in 2019 = CALCULATE([Total Titles], netflix_titles[year_added] = 2019)
```

### One thing I learned the hard way

If you unpivot the `listed_in` (genres) column inside your main table, your row count explodes and every KPI doubles. The fix is to create a **separate `netflix_genres` reference table** linked via `show_id`. You also need to set the cross-filter direction to **Both** in the model view — otherwise the genre chart just shows the total count for everything instead of per-genre counts.

---

## 💡 Key Findings

A few things that actually surprised me after going through the data:

- Netflix has **2.3x more Movies than TV Shows** — 69.6% of the library is movies
- **United States dominates** with 32% of all content. India is a strong second at 11% — the global push is real
- **TV-MA is the most common rating** — Netflix clearly builds for adult audiences first
- **2019 was the peak year** — 2,016 titles added in a single year. It dropped after that, likely due to COVID slowing down productions worldwide
- **67% of TV Shows have only 1 season** — most shows don't survive past their debut
- The average movie on Netflix runs about **100 minutes** — right in the sweet spot
- The `director` column is missing for nearly **30% of titles** — mostly TV Shows where directors aren't always individually credited

---

## 🔧 Tools Used

| Tool | Why |
|---|---|
| Python + Pandas | Data cleaning and analysis |
| Matplotlib + Seaborn | Charts in the notebook |
| Jupyter Notebook | Interactive analysis environment |
| Power BI Desktop | Dashboard and visualizations |
| Power Query (M) | Data transformation before loading |
| DAX | Custom measures and calculations |

---

## 🚀 What I'd Do Next

- Run NLP on the `description` column to find common themes across genres
- Build a simple content-based recommendation system using genre + description similarity
- Try forecasting future content additions using a time series model
- Deploy an interactive web version using Streamlit

---

## 📬 Let's Connect

I'm currently looking for Data Analyst opportunities. If you have feedback on this project, spot something I could improve, or just want to connect — feel free to reach out.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Saurabh%20Anand-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saurabhanand56/)
[![GitHub](https://img.shields.io/badge/GitHub-SaurabhAnand56-100000?style=flat&logo=github&logoColor=white)](https://github.com/SaurabhAnand56)

---

## 📄 License

Dataset: [Netflix Shows on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows) — CC0 Public Domain
Code and dashboard: Free to use for learning and reference.

---

*If this helped you or gave you ideas for your own project, a ⭐ would mean a lot — it genuinely keeps me going! 🙌*
