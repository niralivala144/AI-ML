
# Customer Segmentation System

## About the Project

This project is a Customer Segmentation System built using Machine Learning and Streamlit.

The main idea of this project is simple: instead of treating every customer in the same way, we group customers based on their income and spending behavior. This can help a business understand different types of customers and plan suitable marketing strategies for each group.

The project uses the `Mall_Customers.csv` dataset and K-Means Clustering to create 5 customer segments.

I also added a small application layer where a new customer can enter their details, get a predicted segment, and save their information separately in a SQLite database.

---

## What This Project Does

The application can:

- Analyze the original customer dataset
- Divide customers into 5 groups using K-Means
- Show customer segment statistics
- Display charts for the different customer groups
- Look up existing customers
- Take details of a new customer
- Predict which segment the new customer belongs to
- Show information about the predicted segment
- Save new customer records in SQLite
- Export saved application customers as CSV

The original `Mall_Customers.csv` is only used for the machine learning analysis. New customers are not added to this CSV file.

---

## Dataset

The project uses the `Mall_Customers.csv` dataset.

The dataset contains 200 customers and 5 columns:

| Column | Description |
|---|---|
| CustomerID | Unique customer identifier |
| Gender | Customer gender |
| Age | Customer age |
| Annual Income (k$) | Annual income in thousands |
| Spending Score (1-100) | Spending score assigned to the customer |

During the analysis, `CustomerID` was not used for clustering because it is only an identifier.

`Gender` was also not used as a clustering feature.

The final clustering model uses:

- `Annual Income (k$)`
- `Spending Score (1-100)`

---

## Why These Two Features?

I tested different feature combinations before building the final model.

The combination of Annual Income and Spending Score gave the clearest customer groups.

Income gives an idea about the customer's purchasing capacity, while the spending score gives an idea about their spending behavior.

Adding Age to the clustering features did not improve the clustering results, so Age was kept for customer profiling instead of using it to train the clustering model.

---

## Machine Learning Model

The project uses **K-Means Clustering**.

Before applying K-Means, the selected features are standardized using `StandardScaler`.

### Final Model

- Algorithm: K-Means
- Number of clusters: 5
- Features:
  - Annual Income (k$)
  - Spending Score (1-100)
- Scaling: StandardScaler
- Random State: 42
- Number of Initializations: 10

The final model is saved and reused by the application.

The application does not retrain the model when a new customer is entered. It uses the already trained scaler and K-Means model to predict the customer's cluster.

---

## Choosing K = 5

I tested K-Means with different values of K from 2 to 10.

The models were compared using:

- Inertia / WCSS
- Silhouette Score
- Davies-Bouldin Index

K = 5 gave the best overall result for the selected features.

Final evaluation:

- Inertia: approximately 65.57
- Silhouette Score: approximately 0.55
- Davies-Bouldin Index: approximately 0.57

Because of this, K = 5 was selected for the final application.

---

## Customer Segments

The final model produced five customer groups.

### Cluster 0 - Moderate Income, Moderate Spending

- Customers: 81
- Percentage: 40.5%
- Average Income: about $55.3k
- Average Spending Score: about 49.5
- Average Age: about 42.7 years

This is the largest group. These customers have fairly balanced income and spending behavior.

A business can focus on regular offers, loyalty programs and seasonal promotions for this group.

---

### Cluster 1 - High Income, High Spending

- Customers: 39
- Percentage: 19.5%
- Average Income: about $86.5k
- Average Spending Score: about 82.1
- Average Age: about 32.7 years

These customers have both high purchasing capacity and high spending scores.

This group can be targeted with premium products, VIP offers, exclusive launches and loyalty benefits.

---

### Cluster 2 - Low Income, High Spending

- Customers: 22
- Percentage: 11.0%
- Average Income: about $25.7k
- Average Spending Score: about 79.4
- Average Age: about 25.3 years

These customers have lower income but a high spending score.

Affordable products, limited-time offers and trend-based promotions can be useful for this group.

---

### Cluster 3 - High Income, Low Spending

- Customers: 35
- Percentage: 17.5%
- Average Income: about $88.2k
- Average Spending Score: about 17.1
- Average Age: about 41.1 years

This group has the highest average income but a very low spending score.

This makes them an interesting group for targeted campaigns. Instead of simply giving discounts, businesses can focus on product value, quality and services that may encourage them to spend more.

---

### Cluster 4 - Low Income, Low Spending

- Customers: 23
- Percentage: 11.5%
- Average Income: about $26.3k
- Average Spending Score: about 20.9
- Average Age: about 45.2 years

These customers have both lower income and lower spending scores.

Value-based offers, discounts and essential products are more suitable for this group.

---

## Streamlit Application

The project includes a Streamlit dashboard for interacting with the segmentation results.

The dashboard contains:

### Executive Dashboard

Provides an overview of the customer dataset and segmentation results.

### Customer Segmentation Plot

Shows the different customer groups based on income and spending score.

### Segment Profiles

Displays statistics and information about each cluster.

### Customer Lookup & Predictor

There are two options:

**Existing Customer**

An existing customer from the original dataset can be searched and their segment can be viewed.

**Add New Customer**

A new customer can enter:

- Name
- Gender
- Age
- Annual Income
- Spending Score

After clicking **Analyze Customer**, the application uses the saved scaler and K-Means model to predict the customer's segment.

The application then displays the predicted cluster and the related segment information.

---

## Saving New Customers

New customers are not added to `Mall_Customers.csv`.

Instead, they are stored in a separate SQLite database:

```text
customer_segmentation.db
```

The database contains a `customers` table with information such as:

- ID
- Name
- Gender
- Age
- Annual Income
- Spending Score
- Cluster
- Segment Name
- Created At

This keeps the original training dataset separate from application users.

---

## Exporting Application Customers

The **Export & Raw Data** section contains the customers who were added through the application.

These records can be viewed and downloaded as a CSV file.

The original `Mall_Customers.csv` is not changed.

---

## Project Structure

The exact files may vary depending on the final project folder, but the main structure is similar to:

```text
Customer-Segmentation/
│
├── app.py
├── Mall_Customers.csv
├── requirements.txt
├── README.md
│
├── customer_segmentation.db
│
├── scaler.pkl
├── kmeans_model.pkl
│
└── assets/
    └── charts and images
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Streamlit
- SQLite
- Joblib

---

## Installation

First, clone or download the project.

Then open the project folder in the terminal.

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Application

Start the Streamlit application using:

```bash
streamlit run app.py
```

After that, Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open that URL in your browser.

---

## How to Use the Application

1. Open the Streamlit dashboard.
2. Check the customer segmentation overview.
3. Explore the different customer segments.
4. Go to Customer Lookup & Predictor.
5. Select Existing Customer to check an existing customer.
6. Select Add New Customer to enter a new customer's details.
7. Click Analyze Customer.
8. Check the predicted cluster and segment information.
9. Click Save Customer if you want to store the customer.
10. Go to Export & Raw Data to view or download saved application customers.

---

## Important Point About the Data

The original dataset is kept separate from the customers entered through the application.

This is intentional.

The machine learning model is based only on the original `Mall_Customers.csv` dataset. New customers are only used for prediction and application records. They are not automatically added to the training data and the model is not retrained when a new customer is submitted.

---

## Future Improvements

Some possible improvements for this project are:

- Add customer login and authentication
- Add a customer history page
- Add more detailed marketing reports
- Add monthly customer spending tracking
- Add database search and filtering
- Add an admin dashboard
- Deploy the application online
- Connect the system with a real customer database
- Add automatic model monitoring and retraining as a separate process

---

## Project Goal

The main goal of this project is to combine a Machine Learning clustering model with a simple real-world application.

The project starts with customer data, finds meaningful groups using K-Means, explains those groups, and then allows a business user to enter a new customer and immediately see which segment they are most similar to.

This makes the project more than just a clustering notebook and gives it a practical application.

---

## Disclaimer

This project is created for educational and demonstration purposes.

The customer segments and business recommendations are based on the available dataset and should not be treated as universal customer behavior rules.

---

## Author

**Nirali Vala**

Machine Learning / Data Science Project
