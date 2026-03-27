# 🎬 Netflix EDA Dashboard

<div align="center">

![Netflix](https://img.shields.io/badge/Netflix-E50914?style=for-the-badge&logo=netflix&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![PowerBI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**The complete Netflix data analysis project — Jupyter EDA → Power BI Dashboard → Streamlit Web App.**

[🚀 Live Demo](#) · [📊 Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows) · [👤 Author](#-author)

</div>

---

## 🔄 Project Evolution

```
v1.0  ──►  notebook/                  Step-by-step EDA in Jupyter
              │
              │  same insights · richer visuals
              ▼
v2.0  ──►  powerbi_dashboard/         Static PowerBI dashboard
              │
              │  same charts · now interactive + deployed
              ▼
v3.0  ──►  streamlit_app/             Live filterable web app
```

Each version builds on the last — the same dataset, the same 10-step analysis, progressively more interactive.

---

## 🗂️ Project Structure
```
netflix-eda-dashboard/               ← repo root
│
├── dataset/
│   └── netflix_titles.csv           # Source data (8,807 titles)
│
├── images/                          # Screenshots & chart exports
│
├── notebook/
│   └── Netflix_EDA.ipynb            # v1.0 — Full EDA notebook
│
├── powerbi_dashboard/               # v2.0 — Power BI dashboard files
│
├── streamlit_app/                   # v3.0 — Interactive web app (NEW)
│   │
│   ├── app.py                       # ← Entry point: streamlit run app.py
│   │
│   ├── src/
│   │   ├── __init__.py
│   │   │
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── theme.py             # Netflix palette, CSS, Plotly helpers
│   │   │   └── data_loader.py       # Load, clean & filter logic (cached)
│   │   │
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── sidebar.py           # Author profile card + sidebar filters
│   │   │   └── ui_components.py     # KPI card, insight card, rec card, header
│   │   │
│   │   └── tabs/
│   │       ├── __init__.py
│   │       ├── tab_overview.py      # Tab 1 — Overview
│   │       ├── tab_content.py       # Tab 2 — Content analysis
│   │       ├── tab_geography.py     # Tab 3 — Geography
│   │       ├── tab_timeline.py      # Tab 4 — Timeline
│   │       ├── tab_deepdive.py      # Tab 5 — Deep Dive
│   │       └── tab_recommender.py   # Tab 6 — Recommender engine
│   │
│   └── .streamlit/
│       └── config.toml              # Netflix dark-theme config
│
├── requirements.txt                 # ← All deps: notebook + dashboard
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📸 What's Inside

### v3.0 — Streamlit Web App *(this release)*
> Netflix dark theme · 6 interactive tabs · Global sidebar filters · Content Recommender

| Tab | What It Shows |
|---|---|
| 📊 **Overview** | KPI cards, content-mix donut, top genres, ratings, duration histogram |
| 🎭 **Content** | Rating breakdown, TV seasons, box plots, avg duration per rating |
| 🌍 **Geography** | Choropleth world map, top 10 countries, Movies vs TV Shows by country |
| 📅 **Timeline** | Library growth line chart, release year bars, monthly additions heatmap |
| 🔍 **Deep Dive** | Missing values, correlation heatmap, browsable data table, key insights |
| 🔮 **Recommender** | TF-IDF + cosine similarity with ranked similarity score bars |

### v2.0 — Power BI Dashboard
> Static Netflix-themed Power BI report with pre-built visuals and slicers

See `powerbi_dashboard/` folder.

### v1.0 — Jupyter Notebook
> Step-by-step EDA with detailed markdown explanations — ideal for understanding the analysis logic

| Step | Content |
|---|---|
| 1–3 | Introduction, imports, load dataset |
| 4–5 | Data cleaning, missing values analysis |
| 6–7 | Univariate & bivariate analysis |
| 8 | Visualisations (bar, pie, line, heatmap, word cloud) |
| 9–10 | Key insights & conclusion |
| + | Random Forest classifier · K-Means clustering · PCA · Content Recommender |

---

## ⚡ Quick Start

### v3.0 — Streamlit App

```bash
# 1. Clone
git clone https://github.com/SaurabhAnand56/netflix-eda-dashboard.git
cd netflix-eda-dashboard

# 2. Virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r streamlit_app/requirements.txt

# 4. Run (dataset is already in dataset/ folder)
cd streamlit_app
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

### v1.0 — Jupyter Notebook

```bash
pip install jupyter pandas numpy matplotlib seaborn scikit-learn wordcloud
jupyter notebook notebook/Netflix_EDA.ipynb
```

---

## 🛠️ Tech Stack

| Library | Version | Used In |
|---|---|---|
| [Streamlit](https://streamlit.io) | ≥ 1.32 | v3.0 — web app framework |
| [Plotly](https://plotly.com/python/) | ≥ 5.20 | v3.0 — all interactive charts & map |
| [Pandas](https://pandas.pydata.org) | ≥ 2.0 | v1.0, v3.0 — data manipulation |
| [NumPy](https://numpy.org) | ≥ 1.26 | v1.0, v3.0 — numerical operations |
| [scikit-learn](https://scikit-learn.org) | ≥ 1.4 | v1.0, v3.0 — TF-IDF, cosine sim, RF, K-Means |
| [Matplotlib](https://matplotlib.org) | ≥ 3.7 | v1.0 — static plots |
| [Seaborn](https://seaborn.pydata.org) | ≥ 0.13 | v1.0 — statistical charts |
| [WordCloud](https://github.com/amueller/word_cloud) | ≥ 1.9 | v1.0 — description word cloud |
| Power BI Desktop | — | v2.0 — dashboard |

---

## 📊 Dataset

| Field | Value |
|---|---|
| Source | [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) |
| File | `dataset/netflix_titles.csv` |
| Rows | 8,807 |
| Columns | 12 — `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description` |
| Coverage | Netflix catalogue as of 2021 |

---

## 🔀 Version Comparison

| Feature | Notebook v1.0 | Power BI v2.0 | Streamlit v3.0 |
|---|---|---|---|
| Missing values chart | ✅ Static | ✅ Slicer | ✅ Interactive Plotly |
| Content mix | ✅ Bar + Pie | ✅ Donut | ✅ Animated donut |
| Genre analysis | ✅ H-bar | ✅ Bar | ✅ Colour-scaled bar |
| Rating breakdown | ✅ Bar | ✅ Bar | ✅ Grouped + box plots |
| Country analysis | ✅ Bar | ✅ Map | ✅ Choropleth + stacked |
| Timeline / growth | ✅ Line | ✅ Line | ✅ Filled area + heatmap |
| Movie duration | ✅ Histogram | ✅ Histogram | ✅ With mean/median lines |
| Content recommender | ✅ Console | ❌ | ✅ Full UI + score bars |
| Live filters | ❌ | ✅ Slicers | ✅ Sidebar filters |
| Correlation heatmap | ✅ Seaborn | ❌ | ✅ Interactive Plotly |
| Word cloud | ✅ | ❌ | 🔜 v3.1 |
| K-Means clustering | ✅ | ❌ | 🔜 v3.1 |
| Deployable | ❌ | ❌ | ✅ |

---

## 🗺️ Roadmap

- [x] **v1.0** — Jupyter EDA notebook
- [x] **v2.0** — Power BI dashboard
- [x] **v3.0** — Streamlit interactive web app
- [ ] **v3.1** — Word cloud + K-Means cluster explorer tab
- [ ] **v3.2** — Deploy to Streamlit Community Cloud
- [ ] **v3.3** — Dark / light theme toggle

---

## 👤 Author

**Saurabh Anand**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saurabhanand56/)
[![GitHub](https://img.shields.io/badge/GitHub-24292e?style=flat&logo=github&logoColor=white)](https://github.com/SaurabhAnand56)

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, fork, and build on it.

---

<div align="center">
  <sub>v1.0 → Notebook &nbsp;·&nbsp; v2.0 → Power BI &nbsp;·&nbsp; v3.0 → Streamlit &nbsp;·&nbsp; Built with ❤️ and ☕ by Saurabh Anand</sub>
</div>
