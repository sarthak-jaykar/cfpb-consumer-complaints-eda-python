# Bank of America Consumer Complaints Analysis (CFPB), 2017–2023

Which products and issues generate the most complaints, how often responses are timely, what outcomes consumers receive, and what drove the largest spike. Built in Python on 62,516 complaints submitted to the US Consumer Financial Protection Bureau (CFPB) from May 2017 to August 2023.

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C)
![Domain](https://img.shields.io/badge/Domain-Consumer%20Finance%20%26%20BA-success)

---

## Project Overview

A consumer finance team needs to know where complaint handling is under strain: which products and issues generate the most complaints, whether responses are on time, what consumers receive, and whether anything has changed recently.

The analysis answers these business questions:

1. Which products generate the most complaints, and how has volume changed?
2. What are the main issues within each product?
3. How do submission channels compare?
4. How often are responses timely, and where are they late?
5. What outcomes do consumers get?
6. How do states compare per capita? (Not run: population data is not in this dataset.)
7. Are there spikes, and what makes them up?

Scope covers complaint volume, product, issue, channel, timeliness, relief, state counts and monthly trend. Company identity, causes of complaints and outcomes beyond the recorded response are out of scope.

## Dataset

**Dataset:** Consumer complaint records concerning Bank of America, containing 62,516 records and 12 source fields (May 2017–August 2023).

**Dataset note:** Secondary dataset obtained from publicly available online educational material and used for learning and portfolio analysis. The original XLSX file is included in `data/`. This project analyses the supplied company-specific extract, not the entire CFPB complaint population.

## Key Metrics (May 2017 to August 2023)

| KPI | Result |
| --- | --- |
| Complaints | **62,516** |
| Timely response rate (responded complaints) | **96.1%** (58,619 of 61,022) |
| Complaints in 2022 / 2023 (January to August) | **12,953** / **9,131** |
| Checking or savings share of complaints | **39.7%** |
| Complaints forwarded to the company on the same day | **79.4%** |
| Peak month: July 2023 | **1,749** (113% above monthly average) |

## Key Findings

These findings describe complaints. None shows that a company acted wrongly, and none establishes why consumers complain.

1. **Complaint volume has grown, and 2023 is running higher.** Complaints rose from 7,872 in 2018 to 12,953 in 2022. January to August 2023 averages about 1,141 a month, against about 1,079 in 2022.
2. **Checking and savings accounts dominate, and most of their complaints concern the account itself.** "Managing an account" is 24.2% of all complaints and 61% of checking or savings complaints.
3. **Timely responses are high overall but lower for credit reporting and debt collection.** 96.1% of responded complaints are timely. Mortgage is 99.8%, while credit reporting is 93.7% and debt collection 93.6%. The difference is statistically clear.
4. **Monetary relief is concentrated in checking and credit card complaints.** 33.3% of closed checking or savings complaints and 30.4% of credit card complaints end with monetary relief, against 3.6% for credit reporting. The gap probably reflects issue type, which the data cannot separate from company practice.
5. **The July 2023 spike is driven by account opening and management.** It had 1,749 complaints, about 564 above an average month for checking or savings. "Opening an account" rose from about 34 a month to 183. About a third of the month's complaints came between 11 and 15 July.
6. **Most complaints are forwarded the same day, but 435 wait more than 30 days.** 90% are forwarded within 2 days. The longest took 275 days.
7. **Recent timeliness cannot yet be judged.** 49% of July 2023 complaints and 82% of August 2023 complaints are still in progress, against 0% to 4% in earlier months.

## Recommended Actions

These are proposed management targets, not proven results.

| Priority | Area | Action | Proposed target |
| --- | --- | --- | --- |
| **P1** | Account opening | Ask the product owner whether anything changed in account opening in early July 2023. Check the "Account opened as a result of fraud" sub-issue (160 complaints in July). | "Opening an account" complaints per week, with an alert threshold |
| **P1** | Long-lag complaints | Pull the 435 complaints forwarded more than 30 days after submission and check whether the delay is in forwarding, recording or the data. | Share forwarded within 2 days, monthly |
| **P2** | Timeliness | Review handling steps for credit reporting and debt collection before the next reporting cycle. | Timely rate by product, monthly, for responded complaints |
| **P2** | Capacity | Plan handling capacity against the 2022 to 2023 level, not the 2017 to 2019 level. | Complaints per month, with monthly averages for partial years |
| **P3** | Account management | Review the account-management journey and what customers are told at each step. | "Managing an account" complaints per month |
| **P3** | Reporting | Report recent months with the in-progress share next to the timely rate. | In-progress share by month |

## Tools and Methodology

- **Python:** pandas for cleaning and aggregation; SciPy for a chi-square test; Matplotlib and Seaborn for charts.
- **Pipeline:** five steps, run in order by `script/run_all.py`.

**Data model:** one row per complaint, keyed on Complaint ID. Derived fields include year, year-month, product label, timeliness and relief flags, and forwarding lag (date received minus date submitted).

**Definitions**
- Timely response rate: complaints marked timely, divided by complaints marked Yes or No. In-progress complaints are excluded.
- Monetary relief rate: complaints closed with monetary relief, divided by closed complaints.
- Forwarded same day: forwarding lag of zero days. This measures CFPB to company forwarding, not company response time.

**Cleaning rules**
- Blank timeliness (1,494) matches the "In progress" count exactly, so it is excluded from rates, not counted as late.
- Blank sub-issues and company responses are kept as "Not recorded".
- Nothing is dropped silently.

**Validation**
- Row count, Complaint ID uniqueness and forwarding-lag checks pass.
- Product, channel, year and state totals each sum to 62,516.
- A clean re-run reproduces all 19 result tables and all 5 charts exactly.

## Repository Structure

```text
cfpb-consumer-complaints-python/
├── README.md
├── data/                              Original consumer_complaints.xlsx dataset
├── documentation/
│   ├── 01_business_brief.md           Context, stakeholders, decisions, questions
│   ├── 02_data_and_quality.md         Source, fields, quality decisions, reconciliation
│   ├── 03_findings_and_recommendations.md  Metric definitions, findings, actions
│   ├── how_to_run.txt                 Setup and run guide (VS Code, Windows)
├── results/                           Analysis output tables
├── screenshots/                       Charts
├── script/
│   ├── common.py                      Paths, labels and shared helpers
│   ├── 01_ingest.py                   Profile the workbook (prints to console)
│   ├── 02_clean.py                    Clean and derive forwarding lag (prints checks to console)
│   ├── 03_features.py                 Year, product labels, timeliness and relief flags
│   ├── 04_analysis.py                 Answers to Q1 to Q7 (Q6 counts only)
│   ├── 05_charts.py                   Charts
│   └── run_all.py                     Runs steps 1 to 5
└── requirements.txt
```

## Analysis

| Business question | Code | Output |
| --- | --- | --- |
| Q1. Product volume and trend | `script/04_analysis.py` | `results/q1_volume_by_year.csv`, `q1_product_by_year.csv` |
| Q2. Main issues per product | `script/04_analysis.py` | `results/q2_top_issues_by_product.csv` |
| Q3. Submission channels | `script/04_analysis.py` | `results/q3_channels.csv` |
| Q4. Timeliness | `script/04_analysis.py` | `results/q4_timeliness_*.csv`, `q4_forwarding_lag.csv` |
| Q5. Outcomes | `script/04_analysis.py` | `results/q5_outcomes_by_product.csv` |
| Q6. States (counts only) | `script/04_analysis.py` | `results/q6_states_counts_only.csv` |
| Q7. Spikes | `script/04_analysis.py` | `results/q7_monthly.csv`, `q7_spike_breakdown_2023-07.csv` |

## Documentation

- [Business Brief](documentation/01_business_brief.md): stakeholders, decisions and questions
- [Data and Quality](documentation/02_data_and_quality.md): source, fields, quality decisions and reconciliation
- [Findings and Recommendations](documentation/03_findings_and_recommendations.md): metric definitions, findings and actions
- [How to Run](documentation/how_to_run.txt): setup and run guide

## How to Reproduce

```bash
pip install -r requirements.txt
```

1. The source workbook is already included at `data/consumer_complaints.xlsx`; no download or rename is needed.
2. Run the full pipeline:

```bash
python script/run_all.py
```

Results are written to `results/` and charts to `screenshots/`. Full steps are in [documentation/how_to_run.txt](documentation/how_to_run.txt).

## Limitations

- No company names and no company response dates.
- Recent months are still open, so their timeliness is not comparable.
- Per-capita comparison by state (Q6) is not run, because population data is not included.
- Findings describe association only.

## Author

[GitHub](https://github.com/sarthak-jaykar) · [LinkedIn](https://www.linkedin.com/in/sarthak-jaykar/)
