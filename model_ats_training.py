import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
import joblib

# 1️⃣ Load data
df = pd.read_csv("resume_skill_analysis.csv")

# Safety check
df = df.dropna(subset=['clean_resume', 'ats_score'])

# 2️⃣ Features & target
X = df['clean_resume']
y = df['ats_score']

# 3️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4️⃣ Text → Numbers
vectorizer = TfidfVectorizer(max_features=3000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5️⃣ Model (Regression)
model = LinearRegression()
model.fit(X_train_vec, y_train)

# 6️⃣ Prediction
y_pred = model.predict(X_test_vec)

# 7️⃣ Evaluation
mae = mean_absolute_error(y_test, y_pred)
print("✅ Mean Absolute Error:", mae)

# 8️⃣ Save model
joblib.dump(model, "ats_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

print("🎉 ATS Score Prediction Model Saved Successfully!")
