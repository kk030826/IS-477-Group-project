import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # 1. Load the data
    data_path = 'data/processed/integrated_nba_data.csv'
    if not os.path.exists(data_path):
        print(f"Error: Could not find {data_path}")
        return
        
    df = pd.read_csv(data_path)
    
    # 2. Setup results directory
    if not os.path.exists('results'):
        os.makedirs('results')

    # 3. Calculate Value Ratio and Clean Data
    # We define Value Ratio as PIE per Million Dollars of Salary
    df['value_ratio'] = df['PIE'] / (df['salary_2025_26'] / 1_000_000)

    # Sort and drop duplicates to ensure we only have 10 unique players
    # We keep the entry with the highest value ratio for each player
    df_unique = df.sort_values('value_ratio', ascending=False).drop_duplicates(subset=['player_name'])
    top_10 = df_unique.head(10)

    # 4. Generate the Charts
    # Chart A: PTS vs Salary
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x='PTS', y='salary_2025_26', scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    plt.title('Traditional Volume: Points Per Game vs. Salary')
    plt.savefig('results/pts_vs_salary.png')
    plt.close()

    # Chart B: Correlation Heatmap
    plt.figure(figsize=(8, 6))
    corr_cols = ['salary_2025_26', 'PTS', 'PIE', 'TS_PCT', 'AGE', 'team_win_pct']
    sns.heatmap(df[corr_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Performance vs. Compensation Correlation Heatmap')
    plt.tight_layout()
    plt.savefig('results/correlation_heatmap.png')
    plt.close()

    # Chart C: Top 10 Undervalued Bar Chart
    plt.figure(figsize=(12, 7))
    sns.barplot(data=top_10, x='value_ratio', y='player_name', palette='magma')
    plt.title('Top 10 Undervalued Players (Impact-to-Cost Efficiency)', fontsize=15)
    plt.xlabel('Value Ratio (PIE per Million $)')
    plt.ylabel('Player Name')
    plt.tight_layout()
    plt.savefig('results/undervalued_bar_chart.png')
    plt.close()

    # 5. Top 10 Undervalued Players CSV
    output_csv = 'results/undervalued_players.csv'
    top_10[['player_name', 'PIE', 'salary_2025_26', 'value_ratio']].to_csv(output_csv, index=False)
    
    print(f"Success! Generated 3 charts and the cleaned CSV in the 'results/' directory.")
    print(f"Verified: {len(top_10)} unique players exported to {output_csv}.")

if __name__ == "__main__":
    main()
