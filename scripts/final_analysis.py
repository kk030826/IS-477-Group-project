import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Load data
    df = pd.read_csv('data/processed/integrated_nba_data.csv')
    
    # Ensure results directory exists
    if not os.path.exists('results'):
        os.makedirs('results')

    # Calculate Value Ratio
    # We use (Salary / 1,000,000) to keep the ratio readable
    df['value_ratio'] = df['PIE'] / (df['salary_2025_26'] / 1_000_000)

    # --- FIX: Drop duplicates and filter for 10 unique players ---
    # We sort by value_ratio first, then drop duplicates keeping the highest value
    df_unique = df.sort_values('value_ratio', ascending=False).drop_duplicates(subset=['player_name'])
    top_10 = df_unique.head(10)

    # 1. CHART: PTS vs Salary
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='PTS', y='salary_2025_26', scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Traditional Volume: Points Per Game vs. Salary')
    plt.xlabel('Points Per Game (PTS)')
    plt.ylabel('Salary (USD)')
    plt.savefig('results/pts_vs_salary.png')
    plt.close()

    # 2. CHART: Correlation Heatmap
    plt.figure(figsize=(8, 6))
    corr_cols = ['salary_2025_26', 'PTS', 'PIE', 'TS_PCT', 'AGE', 'team_win_pct']
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap: Performance vs. Compensation')
    plt.tight_layout()
    plt.savefig('results/correlation_heatmap.png')
    plt.close()

    # 3. FIXED CHART: Top 10 Undervalued Bar Chart
    plt.figure(figsize=(12, 7))
    # Using 'player_name' on y-axis to ensure 10 distinct labels
    sns.barplot(data=top_10, x='value_ratio', y='player_name', palette='magma')
    
    plt.title('Top 10 Undervalued Players (Impact-to-Cost Efficiency)', fontsize=15)
    plt.xlabel('Value Ratio (PIE per Million $)', fontsize=12)
    plt.ylabel('Player Name', fontsize=12)
    plt.tight_layout() # Ensures labels don't get cut off
    
    plt.savefig('results/undervalued_bar_chart.png')
    plt.close()

    print(f"Success! Generated 3 charts in the results/ directory.")
    print(f"The top undervalued player is {top_10.iloc[0]['player_name']}.")

if __name__ == "__main__":
    main()
