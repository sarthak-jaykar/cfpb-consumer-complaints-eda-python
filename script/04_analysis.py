"""
Step 4: Analysis for questions Q1 to Q7 (see documentation/01_business_brief.md).
Q6 (complaints per capita) is NOT run: it needs an external population file that is not part of this dataset.
Rates use only complaints where the timeliness flag is known (Yes or No).
"""
import pandas as pd
from scipy import stats
from common import RESULTS
from common import load_features

def q1_volume(df):
    by_year = df.groupby(["year", "is_partial_year"]).size().rename("complaints").reset_index()
    by_year["note"] = by_year["is_partial_year"].map({True: "Jan to Aug only", False: "full year"})
    by_year.to_csv(RESULTS / "q1_volume_by_year.csv", index=False)
    prod = (df.groupby(["product_short", "year"]).size().unstack("year", fill_value=0))
    prod["total"] = prod.sum(axis=1)
    prod = prod.sort_values("total", ascending=False)
    prod.to_csv(RESULTS / "q1_product_by_year.csv")
    sub = (df.groupby(["product_short", "sub_product"]).size().rename("complaints").reset_index()
           .sort_values("complaints", ascending=False).head(12))
    sub.to_csv(RESULTS / "q1_top_sub_products.csv", index=False)
    return by_year, prod

def q2_issues(df):
    rows = []
    for product, grp in df.groupby("product_short"):
        vc = grp["issue"].value_counts().head(3)
        for rank, (issue, n) in enumerate(vc.items(), start=1):
            rows.append({"product_short": product, "rank": rank, "issue": issue, "complaints": int(n),
                         "share_of_product_pct": round(100 * n / len(grp), 2)})
    out = pd.DataFrame(rows).sort_values(["complaints"], ascending=False)
    out.to_csv(RESULTS / "q2_top_issues_by_product.csv", index=False)
    coverage = (df.assign(has_sub=df["sub_issue"] != "Not recorded")
                .groupby("product_short")["has_sub"].mean().mul(100).round(1).rename("sub_issue_coverage_pct"))
    coverage.to_csv(RESULTS / "q2_sub_issue_coverage.csv")
    return out

def q3_channels(df):
    r = df[df["responded"]]
    ch = df.groupby("submitted_via").agg(complaints=("complaint_id", "size"))
    ch["responded"] = r.groupby("submitted_via").size()
    ch["timely_yes"] = r.groupby("submitted_via")["timely_yes"].sum()
    ch["timely_rate_pct"] = (100 * ch["timely_yes"] / ch["responded"]).round(2)
    ch["same_day_forward_pct"] = (100 * df.groupby("submitted_via")["forwarded_same_day"].mean()).round(2)
    ch = ch.sort_values("complaints", ascending=False).reset_index()
    ch.to_csv(RESULTS / "q3_channels.csv", index=False)
    return ch

def q4_timeliness(df):
    r = df[df["responded"]]
    overall = pd.DataFrame([{"responded": len(r), "timely_yes": int(r["timely_yes"].sum()),
                             "timely_rate_pct": round(100 * r["timely_yes"].mean(), 2),
                             "in_progress_or_not_recorded": int((~df["responded"]).sum())}])
    overall.to_csv(RESULTS / "q4_timeliness_overall.csv", index=False)
    by_product = r.groupby("product_short").agg(responded=("complaint_id", "size"),
                                                timely_rate_pct=("timely_yes", lambda s: round(100 * s.mean(), 2))
                                                ).sort_values("responded", ascending=False).reset_index()
    by_product.to_csv(RESULTS / "q4_timeliness_by_product.csv", index=False)
    by_year = r.groupby("year").agg(responded=("complaint_id", "size"),
                                    timely_rate_pct=("timely_yes", lambda s: round(100 * s.mean(), 2))).reset_index()
    by_year.to_csv(RESULTS / "q4_timeliness_by_year.csv", index=False)
    table = pd.crosstab(r["product_short"], r["timely_response"])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    test = pd.DataFrame([{"test": "Chi-square: product vs timely response (responded complaints only)",
                          "chi2": round(chi2, 1), "dof": dof, "p_value": float(f"{p:.3g}"),
                          "caveat": "Large sample, so small differences can be significant; read the rates, not only p."}])
    test.to_csv(RESULTS / "q4_timeliness_test.csv", index=False)
    lag = df["forward_lag_days"]
    lagstats = pd.DataFrame([{"measure": "Forwarded to company on same day (%)", "value": round(100 * (lag == 0).mean(), 2)},
                             {"measure": "Median forwarding lag (days)", "value": float(lag.median())},
                             {"measure": "90th percentile forwarding lag (days)", "value": float(lag.quantile(0.9))},
                             {"measure": "Maximum forwarding lag (days)", "value": float(lag.max())},
                             {"measure": "Complaints forwarded more than 30 days later", "value": int((lag > 30).sum())}])
    lagstats.to_csv(RESULTS / "q4_forwarding_lag.csv", index=False)
    return overall, by_product

def q5_outcomes(df):
    closed = df[df["company_response_to_consumer"].ne("In progress")]
    out = closed.groupby("product_short").agg(closed=("complaint_id", "size"),
                                              monetary_relief_pct=("monetary_relief", lambda s: round(100 * s.mean(), 2)),
                                              explanation_pct=("company_response_to_consumer",
                                                               lambda s: round(100 * s.eq("Closed with explanation").mean(), 2))
                                              ).sort_values("closed", ascending=False).reset_index()
    out.to_csv(RESULTS / "q5_outcomes_by_product.csv", index=False)
    resp = closed.groupby("company_response_to_consumer").size().rename("complaints").reset_index()
    resp.to_csv(RESULTS / "q5_response_types.csv", index=False)
    return out

def q7_monthly(df):
    m = df.groupby("year_month").size().rename("complaints").reset_index()
    m["mean_all_months"] = round(m["complaints"].mean(), 1)
    m["deviation_pct_from_mean"] = (100 * (m["complaints"] - m["complaints"].mean()) / m["complaints"].mean()).round(1)
    m.to_csv(RESULTS / "q7_monthly.csv", index=False)
    top = m.nlargest(5, "complaints")
    top.to_csv(RESULTS / "q7_top_months.csv", index=False)
    return m, top

def q7_spike_breakdown(df, year_month):
    """Investigate one spike month: what it is made of, compared with the average of other months.
    The dataset has no company name, so this shows WHICH products and issues rose, not WHICH company."""
    spike = df[df["year_month"] == year_month]
    rest = df[df["year_month"] != year_month]
    months_rest = rest["year_month"].nunique()
    rows = []
    for col in ["product_short", "issue"]:
        s_share = spike[col].value_counts(normalize=True)
        r_share = rest[col].value_counts(normalize=True)
        comb = pd.DataFrame({"spike_count": spike[col].value_counts(), "spike_share_pct": (100 * s_share).round(2),
                             "other_months_share_pct": (100 * r_share).round(2)}).fillna(0)
        comb["other_months_avg_count_per_month"] = (rest[col].value_counts() / months_rest).round(1)
        comb["excess_count_vs_avg"] = (comb["spike_count"] - comb["other_months_avg_count_per_month"]).round(0)
        comb = comb.sort_values("excess_count_vs_avg", ascending=False).head(8).reset_index()
        comb.insert(0, "dimension", col)
        comb = comb.rename(columns={col: "value"})
        rows.append(comb)
    out = pd.concat(rows)
    out.to_csv(RESULTS / f"q7_spike_breakdown_{year_month}.csv", index=False)
    daily = spike.groupby(spike["date_submitted"].dt.day).size().rename("complaints").reset_index()
    daily.rename(columns={"date_submitted": "day_of_month"}).to_csv(RESULTS / f"q7_spike_daily_{year_month}.csv", index=False)
    recent = (df.groupby("year_month").agg(complaints=("complaint_id", "size"),
                                           in_progress=("responded", lambda s: int((~s).sum())))
              .tail(8).reset_index())
    recent["in_progress_pct"] = (100 * recent["in_progress"] / recent["complaints"]).round(1)
    recent.to_csv(RESULTS / "q7_recent_months_in_progress.csv", index=False)
    return out, recent

def q_states(df):
    s = df.groupby("state").size().rename("complaints").reset_index().sort_values("complaints", ascending=False)
    s["share_pct"] = (100 * s["complaints"] / len(df)).round(2)
    s.to_csv(RESULTS / "q6_states_counts_only.csv", index=False)
    return s

def main():
    df = load_features()
    by_year, prod = q1_volume(df)
    issues = q2_issues(df)
    channels = q3_channels(df)
    overall, tprod = q4_timeliness(df)
    outcomes = q5_outcomes(df)
    m, top = q7_monthly(df)
    states = q_states(df)
    spike, recent = q7_spike_breakdown(df, top.iloc[0]["year_month"])
    print("Q1 by year\n", by_year.to_string(index=False))
    print("\nQ2 top issues (first 6)\n", issues.head(6).to_string(index=False))
    print("\nQ3 channels\n", channels.to_string(index=False))
    print("\nQ4 overall\n", overall.to_string(index=False))
    print("\nQ4 by product\n", tprod.to_string(index=False))
    print("\nQ5 outcomes\n", outcomes.to_string(index=False))
    print("\nQ7 top months\n", top.to_string(index=False))
    print("\nStates (top 5)\n", states.head(5).to_string(index=False))
    print("\nSpike breakdown (top 5 excess)\n", spike.groupby("dimension").head(3).to_string(index=False))
    print("\nRecent months, in progress share\n", recent.to_string(index=False))

if __name__ == "__main__":
    main()
