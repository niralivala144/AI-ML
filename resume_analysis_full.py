import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------
# Step 1: Load CSV
# -----------------------
df = pd.read_csv("D:/AI_RESUME_ANALYZER/resume_skill_analysis.csv")

# -----------------------
# Step 2: Top Candidates
# -----------------------
top_candidates = df.sort_values(by='ats_score', ascending=False)
print("Top 10 candidates:")
print(top_candidates[['job_role', 'ats_score', 'extracted_skills']].head(10))

# -----------------------
# Step 3: Save Top Candidates CSV
# -----------------------
top_candidates.to_csv("D:/AI_RESUME_ANALYZER/top_candidates.csv", index=False)
print("✅ Top candidates saved at D:/AI_RESUME_ANALYZER/top_candidates.csv")

# -----------------------
# Step 4: Skill Counts
# -----------------------
# Handle NaN values
all_skills = ','.join(df['extracted_skills'].dropna().astype(str)).split(',')
skill_counts = Counter([s.strip() for s in all_skills if s.strip()])

# Convert to DataFrame
skill_df = pd.DataFrame(skill_counts.items(), columns=['Skill', 'Count'])
skill_df.to_csv("D:/AI_RESUME_ANALYZER/skill_counts.csv", index=False)
print("✅ Skill counts saved at D:/AI_RESUME_ANALYZER/skill_counts.csv")

# -----------------------
# Step 5: Visualizations (Optional)
# -----------------------
# Top 10 skills
skills, counts = zip(*skill_counts.most_common(10))
sns.barplot(x=list(counts), y=list(skills))
plt.title("Top 10 Skills in Resumes")
plt.xlabel("Count")
plt.ylabel("Skill")
plt.show()

# ATS Score Distribution
sns.histplot(df['ats_score'], bins=10)
plt.title("ATS Score Distribution")
plt.xlabel("ATS Score")
plt.ylabel("Number of Candidates")
plt.show()
