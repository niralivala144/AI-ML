import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer  # <- replace word_tokenize

# Load dataset
df = pd.read_csv("data/Resume.csv")

# Rename columns according to your CSV
df.rename(columns={
    'Category': 'job_role',
    'Resume_str': 'resume_text'
}, inplace=True)

print("Columns:", df.columns)

# NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()  # <- Safe tokenizer

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = tokenizer.tokenize(text)  # <- Use Treebank tokenizer
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words and len(word) > 2]
    return " ".join(tokens)

# Apply cleaning
df['clean_resume'] = df['resume_text'].apply(clean_text)

# Keep only useful columns
final_df = df[['job_role', 'resume_text', 'clean_resume']]

# Save cleaned CSV
final_df.to_csv("data/cleaned_resume.csv", index=False)

print("✅ cleaned_resume.csv created successfully!")
