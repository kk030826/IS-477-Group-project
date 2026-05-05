import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the integrated master dataset
df = pd.read_csv('data/processed/integrated_nba_data.csv')

# 1. Correlation Analysis
# We want to see how PTS (Traditional) vs PIE (Advanced) correlate with Salary
correlation_matrix = df[['salary_2025_26', 'PTS', 'PIE', 'TS_PCT', 'AGE']].corr()
print("Correlation with Salary:")
print(correlation_matrix['salary_2025_26'])

# 2. Visualization: Productivity vs. Salary
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='PIE', y='salary_2025_26', hue='team_win_pct', size='PTS', palette='viridis')
plt.title('NBA Player Impact Estimate (PIE) vs. Salary 2025-26')
plt.xlabel('Player Impact Estimate (Advanced Metric)')
plt.ylabel('Salary ($)')
plt.grid(True, alpha=0.3)

# Identify Undervalued Outliers (High PIE, Low Salary)
# Drawing a quadrant for visualization
plt.axvline(x=df['PIE'].mean(), color='red', linestyle='--')
plt.axhline(y=df['salary_2025_26'].median(), color='red', linestyle='--')

plt.savefig('results/productivity_vs_salary.png')
plt.show()

# 3. Identify Top 10 'Undervalued' Players (High PIE/Salary Ratio)
df['value_ratio'] = df['PIE'] / (df['salary_2025_26'] / 1_000_000)
undervalued = df.sort_values(by='value_ratio', ascending=False).head(10)
undervalued[['player_name', 'PIE', 'salary_2025_26', 'value_ratio']].to_csv('results/undervalued_players.csv')
