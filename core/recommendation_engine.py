def generate_recommendations(profile):

    recs = []

    for _, row in profile.iterrows():

        if row["missing_pct"] > 20:
            recs.append(
                f"Consider imputing or removing column {row['column']}"
            )

        if row["unique"] > 1000:
            recs.append(
                f"Column {row['column']} may require indexing"
            )

    return recs
