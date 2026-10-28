# Project Report

*The project will be structured using the CRISP-DM framework. Details about the framework can be found [here](https://www.datascience-pm.com/crisp-dm-2/). We will not conduct the deployment step. This page will serve as your project report. The current content provides a rough structure and helps you keep track of the deadlines for each deliverable. The first- and second-level headings should remain as provided in the template. All other content can be freely edited and adapted to your project.*

## Project Details

> ⚠️ **Deliverable - 24.09.2026:** Add the names of all team members and their non-binding tasks. Invite all coaches to your repositories.

### Team Members

| Name | Major task |
|--------|------------|
| Simon |            |
| Luka |            |


### Project Name

> ⚠️ **Deliverable - 15.10.2026:** Define a project name.

The Duck Curve Forecaster

### Pitch

> ⚠️ **Deliverable - 15.10.2026:** Write a short pitch.

*Write a 3 to 5 sentence pitch using [this](https://www.linkedin.com/posts/maabrahams_how-to-make-a-compelling-quick-pitch-activity-7179128237782970369-Qa6o/) as a guideline.*

**Our Pitch:**
What if energy planners could anticipate tomorrow’s midday dip and evening rise in Switzerland’s residual electricity demand? We will use machine learning, historical electricity data and archived weather forecasts to predict hourly demand remaining after solar generation, helping planners assess when flexible resources may be needed. For example, our dashboard will highlight the predicted midday trough and evening ramp, allowing storage and generation planners to prepare for changing power requirements. Beyond displaying forecasts, we will compare our model with a simple previous-week baseline and show its accuracy and limitations on unseen data.

---

# 1. Business Understanding

## Problem Statement

> ⚠️ **Deliverable - 22.10.2026:** Write a short problem statement.

Due to the rapid expansion of photovoltaics in Switzerland, the residual load (grid load minus solar generation) drops massively at midday on sunny days, posing critical challenges for grid operators regarding grid stability and balancing power planning. Since the magnitude of this so-called "duck curve" effect depends heavily on short-term weather fluctuations, without precise day-ahead forecasting models based on weather forecasts, a reliable planning basis for operational congestion management on the following day is lacking.

## Goals

> ⚠️ **Deliverable - 22.10.2026:** Formulate goals for you project.

- **Data Pipeline & Preprocessing:** Build an automated Python pipeline that merges hourly national electricity data (Fraunhofer Energy-Charts) with historical day-ahead weather forecasts (temperature_2m and shortwave_radiation from Open-Meteo/ECMWF IFS) from March 2024 to present, achieving 100% UTC timestamp alignment and handling missing values (null) across >14,000 hourly records.

- **Predictive Modeling & Benchmarking:** Train and evaluate a regression model to predict Switzerland’s 24-hour day-ahead residual load, reducing the Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) on unseen test data by at least 10% compared to a naive previous-week baseline (same hour, 7 days prior).

- **Interactive Dashboard Deployment:** Develop and deploy a functional Streamlit dashboard that visualizes the 24-hour predicted residual load curve alongside the baseline model, automatically highlighting the daily midday trough (minimum MW) and evening ramp rate (MW/h change), accompanied by a real-time error metric comparison table.

---

# 2. Data Understanding

## Data Sources

> ⚠️ **Deliverable - 12.11.2026:** Define data sources.

*You are free to choose any data source. As a starting point you might consider [Kaggle](https://www.kaggle.com/datasets) or Swiss open data platforms (e.g. Open Government Data [Zurich](https://www.stadt-zuerich.ch/de/politik-und-verwaltung/statistik-und-daten/open-government-data.html), [Luzern](https://www.stadtluzern.ch/opengovernmentdata), or [Switzerland](https://opendata.swiss/de)) as potential data sources.*

| Data source | Description |
|-------------|-------------|
|             |             |
|             |             |


## Exploratory Data Analysis

> ⚠️ **Deliverable - 12.11.2026:** Conduct an exploratory data analysis.

*A hands-on definition of EDA can be found [here](https://www.geeksforgeeks.org/data-analysis/what-is-exploratory-data-analysis/). The implementation of the EDA should be contained in a dedicated notebook.*

- Notebook to run the EDA: [01_data_understanding.ipynb](notebooks/01_data_understanding.ipynb)

### Data Quality

*Short description of the results from the EDA with respect to data quality issues, such as coverage, data types, missing values, etc.*

### Insights

*List insights from the EDA with respect to the problem statement. Is the data suitable for reaching your goals?*

### Visualizations

The entire set of visualizations can be found in `figures/eda`.

---

# 3. Data Preparation
*Data preparation (also known as feature engineering) consists of steps such as cleaning, filtering, joining, [aggregating](https://www.geeksforgeeks.org/python/grouping-and-aggregating-with-pandas/), [normalizing](https://www.geeksforgeeks.org/python/data-normalization-with-pandas/), and transforming the data. The goal is to have one dataset that contains all features and is ready to be used in the follow-up data modeling. All data preparation is contained in one notebook that may use modular code. Data preparation is not a deliverable but goes hand in hand with the follow-up step of data modeling.*

- Notebook to run the data preparation: [02_data_preparation.ipynb](notebooks/02_data_preparation.ipynb)
- Reusable, modular code is outsourced to separate `.py` files: [src/data_preparation.py](src/data_preparation.py)

## Features

*List and describe each feature.*

| Feature | Description |
|---------|-------------|
|         |             |
|         |             |
|         |             |

---

# 4. Data Modeling

> ⚠️ **Deliverable - 03.12.2026:** Summarize the data modeling approach.

## Concept
*Describe the data modeling approach in a few sentences. Which major tasks have to be performed? Which types of models are used (why)? What are the results? The goal of DSPRO1 is not to implement complex ML algorithms but to tell a coherent data story. A dashboard visualisation or a classical statistical analysis cab be sufficient in terms of data modeling.*

## Implementation
*Make a reference to the notebook and scripts used for performing the data modeling. Sketch a diagram that contains all major tasks and notes for the corresponding implementation.*

- Notebook to run the data modeling: [03_modeling.ipynb](notebooks/03_modeling.ipynb)
- Reusable, modular code is outsourced to separate `.py` files: [src/data_modeling.py](src/data_modeling.py)


# 5. Evaluation

> ⚠️ **Deliverable - 10.12.2026:** Discuss your results in the light of the project goals.

- Notebook to run the evaluation: [04_evaluation.ipynb](notebooks/04_evaluation.ipynb)

- All visualizations can be found in `figures/eval`.


## Results
*List major results. Results often come in the form of evaluation metrics.  A short introduction can be found [here](https://www.ibm.com/think/topics/model-evaluation).*

## Interpretation
*Interpret results in the light of the problem statement. Could you solve the problem? An important issue in the interpretation is practical applicability. Is your solution generalizable?*

## Limitations
*Describe weaknesses of your approach or the underlying data.*

---

# 6. Sustainable Development Goals

> ⚠️ **Deliverable - 17.12.2026:** Describe your results in the light of sustainability.

*The United Nations distinguishes 17 Sustainable Development Goals ([link](https://sdgs.un.org/goals)). Put the results of your project in relation to at least one of these goals. A four-sentence description is sufficient.*
