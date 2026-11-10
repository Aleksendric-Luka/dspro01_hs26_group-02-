# Project Report

*The project will be structured using the CRISP-DM framework. Details about the framework can be found [here](https://www.datascience-pm.com/crisp-dm-2/). We will not conduct the deployment step. This page will serve as your project report. The current content provides a rough structure and helps you keep track of the deadlines for each deliverable. The first- and second-level headings should remain as provided in the template. All other content can be freely edited and adapted to your project.*

## Project Details

> ⚠️ **Deliverable - 24.09.2026:** Add the names of all team members and their non-binding tasks. Invite all coaches to your repositories.

### Team Members

| Name | Major task |
|--------|------------|
| Simon | Focus on energy data preparation and EDA; shared responsibility for modelling, evaluation, and the Streamlit dashboard.           |
| Luka | Focus on weather data preparation and EDA; shared responsibility for modelling, evaluation, and the Streamlit dashboard.           |


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

- **Data Preparation:** Create a reproducible dataset containing 8,760 complete hourly records for 2025 by combining Swiss electricity data with equally weighted weather data from seven locations, aligning timestamps in Europe/Zurich, and calculating residual load as load - solar.

- **Model Training & Testing:** Train a regression model to predict hourly residual load using weather and calendar features, applying a chronological 80/20 split and evaluating predictions on the unseen test period using MAE and RMSE.

- **Presentation & Interpretation:** Present predicted and observed residual-load curves and test metrics in an interactive Streamlit dashboard, compare performance with a previous-week baseline, and explain prediction errors and limitations, particularly that historical weather inputs do not establish operational day-ahead forecasting performance.

---

# 2. Data Understanding

## Data Sources

> ⚠️ **Deliverable - 12.11.2026:** Define data sources.

The project combines hourly Swiss electricity data with hourly weather data from seven Swiss locations.

| Data source | Description |
|-------------|-------------|
| Fraunhofer ISE Energy-Charts – Public Power API            | Country-level electricity data for Switzerland (country=ch). We retain the Unix timestamp (unix_seconds), electricity load (load, MW), and solar generation (solar, MW). The request covers 1 January 2024–28 October 2026; the downloaded CSV contains 24,752 rows and ends at 07:00 on 28 October 2026, Swiss local time.            |
| Open-Meteo – Historical Weather API            | Hourly historical weather data for 2025: air temperature at 2 m (temperature_2m, °C) and shortwave radiation (shortwave_radiation, W/m²). The raw dataset contains 61,320 records: 8,760 per location across seven locations.            |

API requests used:
- [Energy-Charts request](https://api.energy-charts.info/public_power?country=ch&start=2024-01-01&end=2026-10-28)
- [Open-Meteo request](https://archive-api.open-meteo.com/v1/archive?latitude=47.37,47.55,46.94,46.20,46.23,46.00,46.85&longitude=8.54,7.59,7.44,6.14,7.36,8.95,9.53&start_date=2025-01-01&end_date=2025-12-31&hourly=temperature_2m,shortwave_radiation&timezone=auto)

The requested coordinates correspond approximately to Zurich, Basel, Bern, Geneva, Sion, Lugano, and Chur

## Exploratory Data Analysis

> ⚠️ **Deliverable - 12.11.2026:** Conduct an exploratory data analysis.

The EDA checks data structure, completeness, exact duplicate rows, numerical ranges, and temporal patterns. It is currently implemented in two dedicated notebooks:
- notebooks/01_data_understanding_energy.ipynb
- notebooks/01_data_understanding_weather.ipynb

### Data Quality

| Aspect | Result |
|---------|-------------|
| Coverage        | Both prepared datasets contain all 8,760 expected hourly records for 2025, with no gaps or unexpected timestamps.            |
| Data types        | Measurements are numeric, and timestamps are converted from Unix seconds or strings to timezone-aware datetimes and exported in ISO 8601 format.            |
| Missing values        | Filtering to 2025 excludes all missing energy values, while weather and merged data are complete without imputation.            |
| Duplicates        | Neither raw dataset contains exact duplicate rows, and timestamps are unique after weather aggregation.            |
| Plausibility        | Temperature (−12.4–37.1 °C) and radiation (0–966 W/m²) show plausible ranges, with valid nighttime zeros and no automatic outlier removal.            |
| Time alignment and merge        | Both datasets are aligned to Europe/Zurich, accounting for daylight saving time, and merged one-to-one into 8,760 complete rows.            |

### Insights

1. **Electricity load:** The daily load pattern provides the demand baseline from which solar generation is subtracted to investigate midday residual-load troughs and evening ramps.

2. **Solar generation:** The midday peak and substantial variation between days support investigating the duck-curve effect, although residual-load plots are still needed to quantify it.

3. **Temperature:** Pronounced seasonal temperature variation motivates its inclusion as a potential predictor of electricity demand, although its relationship with load remains to be tested.

4. **Radiation:** The strong daily radiation cycle makes it a relevant candidate predictor of solar generation and the resulting midday reduction in residual load.

5. **Suitability:** The 8,760 complete hourly records support initial residual-load modelling, but one year and equal regional weighting limit representativeness, while operational day-ahead performance requires evaluation with weather forecasts available at prediction time.

### Visualizations

The EDA notebooks contain four boxplots:
- Swiss electricity load by local hour of day, 2025.
- Swiss solar generation by local hour of day, 2025.
- Monthly air temperature across seven Swiss locations, 2025.
- Shortwave radiation by recorded hour across seven Swiss locations, 2025.

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
| timestamp        | 	Hourly time key in ISO 8601 format with an explicit Swiss winter/summer offset. Used for joining, ordering, and chronological evaluation.            |
| load        | 	Historical Swiss electricity load in MW            |
| solar        | 	Historical Swiss solar generation in MW.            |
| temperature_2m        | 	Arithmetic mean of air temperature at 2 m across the seven locations, in °C, rounded to four decimal places.            |
| shortwave_radiation        | Arithmetic mean of shortwave radiation across the seven locations, in W/m², rounded to four decimal places.            |
| residual_load        | Calculated as load - solar, in MW. This is the quantity to predict, not an input feature            |


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
