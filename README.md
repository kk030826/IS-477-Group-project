# NBA Productivity vs. Compensation Analysis

## Contributors
* Colin Cosillo (Lead Strategist)
* Daniel Kang (Lead Architect)

## Summary (500-600 words)
The modern National Basketball Association operates within a highly regulated and complex fiscal environment defined by a rigid salary cap, a luxury tax threshold, and a newly implemented "second apron" that significantly punishes inefficient spending. In this small margin era, where a single bad contract can derail a franchise for half a decade, the primary competitive advantage for a professional front office is the identification of surplus value. This is defined as the ability to secure high level on court production at a below market contractual cost. Our project was motivated by the difference in reliance of traditional scouting methodologies, which often prioritize high volume scoring and recognizable archetypes, and modern analytics which emphasize holistic impact, defensive efficiency, and shooting economy. Historically, the evaluation of professional basketball players was limited to basic box score statistics such as points, rebounds, and assists. However, the emergence of the player tracking era and advanced metrics has provided teams with a far more granular understanding of how individual actions contribute to the probability of winning a basketball game.
We hypothesized that while traditional box score statistics like Points Per Game have historically driven the vast majority of compensation decisions due to their visibility and public appeal, modern advanced metrics such as Player Impact Estimate and True Shooting Percentage should ideally show an increasingly stronger correlation with modern salary decisions as teams become more data driven. To test this hypothesis, we built a comprehensive data pipeline that integrated four distinct datasets encompassing traditional performance statistics, advanced efficiency metrics, financial records including multi year salary projections and contract lengths, and team standings. This multi dimensional approach allowed us to move beyond simple correlation and look at the intersection of individual performance, market value, and team success. By examining these four areas simultaneously, we aimed to uncover whether the market truly rewards the players who contribute most to winning, or if it continues to reward the players who simply accumulate the most volume.
By resolving entity discrepancies across these disparate sources, such as inconsistent naming conventions for international players or the presence of various suffixes that often break standard SQL join keys, we created a master dataset representing the 2024 through 2026 NBA landscape. Our research focused on two primary questions regarding the extent to which efficiency metrics predict salary compared to volume metrics and the identification of specific value outliers who exist in the gaps of the current market. Our findings suggest a lingering market gap where volume remains the primary currency for compensation, leaving significant opportunities for teams to exploit efficiency based value. This discrepancy highlights a fundamental inefficiency in the NBA labor market that savvy front offices can utilize to build championship rosters.
While the league has moved toward a more analytical framework in terms of on court strategy, spacing, and play calling, the financial market has not yet fully corrected for efficiency. There is a clear premium paid for the ability to generate individual points, often at the expense of defensive utility or shooting economy. By documenting these discrepancies, this project provides a baseline for understanding how roster construction might evolve as front offices begin to weigh advanced impact metrics more heavily in contract negotiations. Ultimately, our work highlights that the most successful franchises are likely those that can identify high impact players whose contributions are currently masked by a lack of traditional box score volume. Through this analysis, we provide a framework for future studies into the evolving relationship between professional sports compensation and modern data science, proving that in the NBA, as in any other market, information is the most valuable currency.


## Data Profile (Max 2000 words)
### NBA Player Statistics
* **Location:** `data/raw/player_stats_advanced.csv`
* **Structure:** 458 rows, 50+ columns.
* **Ethical/Legal:** Accessed via public API for educational use.

## Findings (~500 words)
[Insert your charts here. Discuss if Win Shares or PER had a higher correlation coefficient (R²) with Salary.]

## Challenges (~500 words)
[Reuse your Milestone 3 text about Entity Resolution (Luka Dončić) and Team Mapping.]

## Reproducing
1. Clone repository.
2. Run `pip install -r requirements.txt`.
3. Run `python main.py`.
