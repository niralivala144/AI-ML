
# Mall Customer Segmentation

A small end-to-end project where I took the classic Mall Customers dataset and used K-Means clustering to split customers into groups based on how they actually behave — their age, income, and spending habits — instead of treating everyone the same.

The idea is simple: a mall (or any retailer) doesn't have one type of customer. Some people have money and spend it freely, some have money and barely spend, some are young and impulsive, and some are just... average. Marketing to all of them the same way wastes money. This project figures out who's who, automatically, from the data.

## What's in the data

The dataset is the standard `Mall_Customers.csv` — 200 customers, 5 columns: CustomerID, Gender, Age, Annual Income, and a Spending Score (a made-up 1-100 score the mall assigns based on customer behavior). No missing values, nothing messy to clean.

## How the project is organized

```
customer_segmentation_project/
├── data/
│   └── Mall_Customers.csv
├── src/
│   └── customer_segmentation.py     <- run this file
├── outputs/
│   ├── charts/                      <- all the plots get saved here
│   ├── segmented_customers.csv      <- final labeled data
│   └── cluster_profile_summary.csv
├── report/
│   └── Mall_Customer_Segmentation_Report.docx
├── requirements.txt
└── README.md
```

## What I did, step by step

**1. Loaded and checked the data.** Renamed a couple of columns to be easier to work with in code, checked for nulls and duplicates (there weren't any).

**2. Did some basic EDA.** Plotted histograms for age, income, and spending score just to see what the distribution actually looks like, plus a correlation heatmap and a quick gender breakdown. Nothing fancy, just enough to know the data isn't weird before throwing a clustering algorithm at it.

**3. Scaled the features.** This part matters more than it sounds — K-Means is based on distance, and income (which ranges up to 137) would completely overpower spending score (which only goes to 100) if left unscaled. Used `StandardScaler` to put everything on the same footing.

**4. Figured out how many clusters made sense.** I didn't just pick a number — ran K-Means for k=2 through k=9 and looked at both the elbow curve (inertia) and the silhouette score. Both pointed toward 5 clusters being a solid choice, and 5 also matches the natural income/spending pattern you can literally see if you plot the data.

**5. Ran K-Means with k=5.** Got a silhouette score of 0.417, which for real-world (non-synthetic) data like this is genuinely a good separation — the clusters aren't overlapping mush.

**6. Visualized it.** Used PCA to squash everything into 2D for a cluster plot, but honestly the more useful chart here is just Income vs. Spending Score directly — you can see the 5 groups almost with your bare eyes once they're colored in.

**7. Named the segments.** Instead of eyeballing "cluster 3 seems kind of rich" I set up target profiles for 5 typical customer personas and used the Hungarian algorithm (`scipy.optimize.linear_sum_assignment`) to match each cluster to its best-fitting persona automatically. This avoids the situation where two clusters accidentally get the same label or a cluster gets a name that doesn't really fit.

**8. Exported everything** — labeled customer data, cluster summary stats, and all the charts — into the `outputs/` folder.

**9. Put together a proper report.** A Word doc in `report/` that lays out the whole thing for someone non-technical — the segments, what they mean, and what to actually do about each one.

## The 5 segments it found

| Segment | % of customers | Avg age | Avg income | Avg spending score |
|---|---|---|---|---|
| Premium Big Spenders | 20% | 33 | $86.1k | 81.5 |
| Careful Affluent | 19.5% | 40 | $86.1k | 19.4 |
| Young Impulsive Spenders | 27% | 25 | $41.1k | 62.2 |
| Standard / Average | 23.5% | 56 | $54.4k | 48.9 |
| Budget Conscious | 10% | 46 | $26.8k | 18.4 |

The most interesting one honestly is "Careful Affluent" — same income as the Premium Big Spenders ($86k) but barely spending. That's not a low-value customer, that's a customer nobody's converting properly. If I were advising a real mall, that's the group I'd chase first.

## Running it yourself

```bash
git clone https://github.com/<your-username>/customer_segmentation_project.git
cd customer_segmentation_project
pip install -r requirements.txt
python src/customer_segmentation.py
```

Everything in `outputs/` gets regenerated when you run it. If you want to use your own data, just swap out `data/Mall_Customers.csv` for your own file with the same column names, or tweak the `cluster_features` list near the top of `src/customer_segmentation.py`. If you actually have real purchase history (not just a spending score), swapping in real Recency/Frequency/Monetary numbers would make this a lot more powerful.

## What I'd add next

- Real transaction-level RFM data instead of the synthetic spending score
- A comparison against DBSCAN or hierarchical clustering, just to sanity-check K-Means isn't missing something
- Turning this into a small Streamlit dashboard so segments can be explored interactively instead of static charts
- Actually A/B testing campaigns per segment and feeding results back in

## License

MIT — do whatever you want with it.
