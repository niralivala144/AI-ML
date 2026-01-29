🎬 Netflix Data Analysis Project
📌 Project Overview

This project focuses on Exploratory Data Analysis (EDA) of the Netflix dataset using Python.
The goal is to clean the data, handle missing values, perform feature engineering, and extract meaningful insights using visualizations.

📂 Dataset Information

Dataset Name: Netflix Titles Dataset

Source: Kaggle

Records: ~8,800

Features: Movies & TV Shows, country, director, cast, release year, date added, rating, duration, etc.

🛠️ Tools & Technologies Used

Python

Pandas

Matplotlib

Google Colab

🔄 Project Workflow
1️⃣ Data Loading

Loaded CSV dataset using Pandas

Inspected initial rows to understand structure

2️⃣ Data Exploration

Used .info() and .isnull() to check data types and missing values

3️⃣ Data Cleaning

Filled missing values in categorical columns (director, cast, country) with "Unknown"

Converted date_added to datetime format

4️⃣ Feature Engineering

Extracted year_added from date_added

Prepared data for time-based analysis

5️⃣ Data Visualization

Pie Chart: Distribution of Movies vs TV Shows

Bar Chart: Top 10 content-producing countries

Line Chart: Year-wise Netflix content release trend

📊 Key Insights

Netflix has more Movies than TV Shows

USA, India, and UK are top content producers

Netflix content releases have increased significantly in recent years

📸 Sample Visualizations

Content Type Distribution (Pie Chart)

Top 10 Countries (Bar Chart)

Release Trend Over Time (Line Chart)


