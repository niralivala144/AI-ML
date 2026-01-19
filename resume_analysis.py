import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load processed CSV
df = pd.read_csv("D:/AI_RESUME_ANALYZER/resume_skill_analysis.csv")

# Step 2: Top candidates by ATS score
top_candidates = df.sort_values(by='ats_score', ascending=False)
print("Top 10 candidates:")
print(top_candidates[['job_role', 'ats_score', 'extracted_skills']].head(10))

# Convert all values to string first
all_skills = ','.join(df['extracted_skills'].dropna().astype(str)).split(',')
skill_counts = Counter([s.strip() for s in all_skills if s.strip()])

print("\nTop 10 most common skills:")
print(skill_counts.most_common(10))

# Step 4: Visualize top skills
skills, counts = zip(*skill_counts.most_common(10))
sns.barplot(x=list(counts), y=list(skills))
plt.title("Top 10 Skills in Resumes")
plt.xlabel("Count")
plt.ylabel("Skill")
plt.show()

# Step 5: Visualize ATS score distribution
sns.histplot(df['ats_score'], bins=10)
plt.title("ATS Score Distribution")
plt.xlabel("ATS Score")
plt.ylabel("Number of Candidates")
plt.show()
