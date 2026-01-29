💳 Credit Card Fraud Detection using Machine Learning 📌 Project Overview

This project focuses on detecting fraudulent credit card transactions using Machine Learning. A Logistic Regression model is trained on real-world transaction data to accurately classify fraudulent vs non-fraudulent transactions while handling highly imbalanced data.

🎯 Problem Statement

Credit card fraud is a major financial risk, and fraud cases are rare compared to normal transactions, making detection challenging. The goal of this project is to build a reliable fraud detection system that maximizes fraud identification while minimizing false alarms.

📂 Dataset Description

Dataset: Credit Card Transactions Dataset

Records: ~284,000 transactions

Features: PCA-transformed features (V1–V28), Time, Amount

Target Column:

Class = 0 → Non-Fraud

Class = 1 → Fraud

🛠️ Tech Stack

Programming Language: Python

Libraries: Pandas, NumPy

Machine Learning: Scikit-learn

Visualization: Matplotlib, Seaborn

Platform: Google Colab

🔄 Project Workflow 1️⃣ Data Loading & Inspection

Loaded CSV dataset using Pandas

Inspected data structure, data types, and basic statistics

2️⃣ Exploratory Data Analysis (EDA)

Analyzed class imbalance in the target variable

Visualized transaction time and amount distributions

Compared transaction amounts for fraudulent vs non-fraudulent cases

3️⃣ Data Preprocessing

Checked and handled missing values

Applied StandardScaler to scale Time and Amount

Dropped original unscaled columns

Split data into training (70%) and testing (30%) using stratified sampling

4️⃣ Model Building

Implemented Logistic Regression

Used class_weight='balanced' to handle imbalanced classes

5️⃣ Model Evaluation

Evaluated model using:

Precision, Recall, F1-Score

Accuracy

ROC-AUC Score

Visualized:

Confusion Matrix

ROC Curve

📊 Results & Insights

Successfully detected fraudulent transactions

ROC-AUC used as a reliable metric for imbalanced data

Logistic Regression provided interpretable and stable performance

📈 Visualizations

Transaction Time Distribution

Transaction Amount Distribution (Log scale)

Fraud vs Non-Fraud Amount Comparison

Confusion Matrix

ROC Curve


