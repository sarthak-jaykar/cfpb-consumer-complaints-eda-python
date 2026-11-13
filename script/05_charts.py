"""
Step 5: Charts. Each chart shows its source and whether the period is partial.
Saves PNG files to screenshots/.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from common import RESULTS, SCREENSHOTS
from common import load_features

SOURCE = "Source: CFPB Consumer Complaints (submitted 1 May 2017 to 28 Aug 2023). Analysis in this project."

def save(fig, name):
    fig.tight_layout()
    fig.savefig(SCREENSHOTS / name, dpi=120)
    plt.close(fig)

def main():
    df = load_features()

    m = pd.read_csv(RESULTS / "q7_monthly.csv")
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(range(len(m)), m["complaints"], marker="o", markersize=3, color="#3b6ea8")
    ax.axhline(m["mean_all_months"].iloc[0], color="grey", linestyle="--", linewidth=1, label="Monthly average")
    step = 6
    ax.set_xticks(range(0, len(m), step))
    ax.set_xticklabels(m["year_month"].iloc[::step], rotation=45, fontsize=8)
    ax.set_title("Complaints per month, May 2017 to Aug 2023")
    ax.set_ylabel("Complaints")
    ax.legend(fontsize=8)
    fig.text(0.01, 0.01, SOURCE + " Aug 2023 covers 1 to 28 Aug (partial month).", fontsize=7)
    save(fig, "q7_monthly_volume.png")

    p = pd.read_csv(RESULTS / "q4_timeliness_by_product.csv").sort_values("timely_rate_pct")
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(p["product_short"], p["timely_rate_pct"], color="#3b6ea8")
    ax.set_xlim(85, 100)
    ax.set_title("Timely response rate by product (responded complaints only)")
    ax.set_xlabel("Timely response (%)")
    fig.text(0.01, 0.01, SOURCE + " Axis starts at 85%.", fontsize=7)
    save(fig, "q4_timely_rate_by_product.png")

    ch = pd.read_csv(RESULTS / "q3_channels.csv")
    ch = ch[ch["complaints"] >= 100]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(ch["submitted_via"], ch["complaints"], color="#3b6ea8")
    ax.set_title("Complaints by submission channel (channels with 100 or more)")
    ax.set_ylabel("Complaints")
    fig.text(0.01, 0.01, SOURCE, fontsize=7)
    save(fig, "q3_channels.png")

    o = pd.read_csv(RESULTS / "q5_outcomes_by_product.csv").sort_values("monetary_relief_pct")
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(o["product_short"], o["monetary_relief_pct"], color="#3b6ea8")
    ax.set_title("Share of closed complaints with monetary relief, by product")
    ax.set_xlabel("Monetary relief (%)")
    fig.text(0.01, 0.01, SOURCE + " Excludes complaints still in progress.", fontsize=7)
    save(fig, "q5_monetary_relief_by_product.png")

    py = pd.read_csv(RESULTS / "q1_product_by_year.csv", index_col=0)
    years = [c for c in py.columns if c != "total"]
    top = py.sort_values("total", ascending=False).head(5)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    for name, row in top[years].iterrows():
        ax.plot(years, row.values, marker="o", label=name)
    ax.set_title("Top five products: complaints per year")
    ax.set_ylabel("Complaints")
    ax.legend(fontsize=7)
    fig.text(0.01, 0.01, SOURCE + " 2023 is Jan to Aug only.", fontsize=7)
    save(fig, "q1_top_products_by_year.png")
    print("Charts saved to", SCREENSHOTS)

if __name__ == "__main__":
    main()
