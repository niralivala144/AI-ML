import pandas as pd
import os

# ✅ Absolute path to CSV (update if needed)
csv_path = "D:/AI_RESUME_ANALYZER/data/cleaned_resume.csv"

# Check if file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found at: {csv_path}")

# Load cleaned CSV
df = pd.read_csv(csv_path)

# ✅ Check your column names
print("Columns in CSV:", df.columns)

# If your resume text column is not 'cleaned_resume', update this variable
# Update this to match your CSV column
resume_col = 'clean_resume'  # correct column name
  # e.g., 'resume_text' if different

# Define common skills list (HR + General)
skills = [
    'recruitment', 'talent acquisition', 'employee relations', 'hr', 'training',
    'payroll', 'performance management', 'ms excel', 'communication', 'leadership',
    'team management', 'project management', 'hiring', 'onboarding', 'benefits',
    'employee engagement', 'analytics', 'hr policies', 'labor laws'
]

# Function to extract skills
def extract_skills(text):
    text = str(text).lower()
    found_skills = [skill for skill in skills if skill in text]
    return ', '.join(found_skills)

# Apply skill extraction
df['extracted_skills'] = df[resume_col].apply(extract_skills)

# ✅ Improved ATS score calculation
df['ats_score'] = df['extracted_skills'].apply(
    lambda x: len([s for s in x.split(',') if s.strip()]) if x else 0
)

# Save final CSV
output_path = "D:/AI_RESUME_ANALYZER/resume_skill_analysis.csv"
df.to_csv(output_path, index=False)

print(f"✅ Skill extraction + ATS score done successfully! Saved at {output_path}")
df.head()
