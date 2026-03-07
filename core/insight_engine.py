def generate_insights(corr, profile):

    insights = []

    if corr is not None:
        for col in corr.columns:
            for idx in corr.index:
                if col != idx and abs(corr.loc[idx,col]) > 0.8:
                    insights.append(
                        f"Strong correlation between {idx} and {col}"
                    )

    for _, row in profile.iterrows():
        if row["missing_pct"] > 20:
            insights.append(
                f"Column {row['column']} has high missing values ({row['missing_pct']}%)"
            )

    return insights
