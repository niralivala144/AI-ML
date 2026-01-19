import nltk
import os

# Optional: custom path for NLTK data (change if needed)
nltk_data_path = r"D:\nltk_data"
if not os.path.exists(nltk_data_path):
    os.makedirs(nltk_data_path)

# Add this path so Python knows where to look
nltk.data.path.append(nltk_data_path)

# Download required NLTK resources
nltk.download('stopwords', download_dir=nltk_data_path)
nltk.download('wordnet', download_dir=nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)

print("✅ All NLTK resources downloaded successfully!")
print("NLTK data paths:", nltk.data.path)
