# Data and Quality

## Source
| Field | Value |
|---|---|
| Dataset | Bank of America consumer complaints extract from CFPB records |
| Publisher | Consumer Financial Protection Bureau (US) |
| Dataset context | Secondary dataset obtained from publicly available online educational material; used for educational and portfolio analysis. |
| Period | Submitted 1 May 2017 to 28 August 2023 |
| Grain | one row per complaint (Complaint ID is unique) |

## Key fields

| Field | Meaning | Note |
|---|---|---|
| Date submitted | When CFPB received the complaint | Used for all time analysis |
| Date received | When CFPB sent it to the company | Forwarding lag = Date received − Date submitted |
| Submitted via | Channel: Web, Referral, Phone, Postal mail, Fax, Web Referral, Email | Email has 2 rows, too few to compare (still shown in the results) |
| Product and Sub-product | Product area | 9 products |
| Issue and Sub-issue | Problem reported | Sub-issue blank for 17.4% |
| Company response to consumer | Outcome | e.g. "Closed with monetary relief", "In progress" |
| Timely response? | Yes or No | Blank for 1,494, all of which are "In progress" |

## Quality decisions

| # | Issue | Decision |
|---|---|---|
| 1 | Timely blank (1,494) | Matches "In progress" exactly. Excluded from timeliness rates, not counted as late. |
| 2 | Sub-issue blank (17.4%) | Kept as "Not recorded". The source notes not every issue has sub-issues. |
| 3 | Forwarding lag up to 275 days; 435 complaints over 30 days | Kept and flagged for process review (see F6) |
| 4 | No company name | Company-level comparison not possible. Stated as a limit. |
| 5 | No company response date | Response time not measured. The timely flag is used as provided. |
| 6 | Recent months still open (July 2023: 49%, August 2023: 82% in progress) | Shown separately. Not compared with earlier months. |
| 7 | 2023 is partial | Marked partial. Monthly averages used for comparison. |

## Reconciliation

| Total | Expected | Result |
|---|---|---|
| Complaints | 62,516 | 62,516 |
| Product totals | 62,516 | 62,516 |
| Channel totals | 62,516 | 62,516 |
| Year totals | 62,516 | 62,516 |
| State totals | 62,516 | 62,516 |
| Duplicate Complaint IDs | 0 | 0 |
| Negative forwarding lag | 0 | 0 |

Cleaning and profile checks are printed to the console by `script/01_ingest.py` and `script/02_clean.py`.
