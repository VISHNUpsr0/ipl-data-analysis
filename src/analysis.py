import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. LOAD
matches = pd.read_csv("../data/ipl_2024_matches.csv")
deliveries = pd.concat([
    pd.read_csv("../data/ipl_2022_deliveries.csv"),
    pd.read_csv("../data/ipl_2023_deliveries.csv"),
    pd.read_csv("../data/ipl_2024_deliveries.csv"),
    pd.read_csv("../data/ipl_2025_deliveries.csv"),
    pd.read_csv("../data/ipl_2026_deliveries.csv"),
], ignore_index=True)

# 2. CLEAN
matches.dropna(subset=["winning_team"], inplace=True)
deliveries.dropna(subset=["striker"], inplace=True)

# 3. ANALYZE
wins        = matches["winning_team"].value_counts().head(5)
top_batsmen = deliveries.groupby("striker")["runs_of_bat"].sum().sort_values(ascending=False).head(5)
avg_runs    = deliveries.groupby("match_id")["runs_of_bat"].sum().mean()
dismissals  = deliveries["wicket_type"].value_counts().head(5)
season_runs = deliveries.groupby("season")["runs_of_bat"].sum()

# 4. VISUALIZE — Dashboard (Matplotlib)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("IPL 2022–2026 Analysis", fontsize=16, fontweight='bold')

axes[0,0].bar(wins.index, wins.values, color='teal')
axes[0,0].set_title("Top 5 Teams by Wins")
axes[0,0].tick_params(axis='x', rotation=45)

axes[0,1].barh(top_batsmen.index, top_batsmen.values, color='orange')
axes[0,1].set_title("Top 5 Run Scorers")

axes[1,0].plot(season_runs.index.astype(str), season_runs.values, marker='o', color='purple')
axes[1,0].set_title("Season-wise Runs Trend")
axes[1,0].tick_params(axis='x', rotation=45)

axes[1,1].pie(dismissals.values, labels=dismissals.index, autopct='%1.1f%%')
axes[1,1].set_title("Dismissal Types")

plt.tight_layout()
plt.savefig("../images/dashboard.png")
plt.show()

# 5. SEABORN — Runs by Match Phase
plt.figure(figsize=(8, 5))
sns.boxplot(x="phase", y="runs_of_bat", data=deliveries)
plt.title("Runs Distribution by Match Phase")
plt.tight_layout()
plt.savefig("../images/boxplot.png")
plt.show()

# 6. SUMMARY
print("=" * 40)
print(f"  Top Team      : {wins.index[0]}")
print(f"  Top Batsman   : {top_batsmen.index[0]}")
print(f"  Avg Runs/Match: {avg_runs:.2f}")
print(f"  Top Dismissal : {dismissals.index[0]}")
print("=" * 40)
print("✅ Done! Charts saved to images/")