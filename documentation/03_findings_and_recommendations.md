# Findings and Recommendations

## How to read this
Each finding follows: **finding → evidence → business implication → recommendation → measure**. Findings describe complaints. None shows that a company acted wrongly.

## Metric definitions

| Metric | Definition |
|---|---|
| Timely response rate | Complaints with timely = Yes ÷ complaints with timely = Yes or No |
| Monetary relief rate | Closed with monetary relief ÷ closed complaints (excludes in-progress) |
| Forwarded same day | Complaints with forwarding lag 0 ÷ all complaints |
| Excess over average | A spike month's count minus the average of other months |

## Findings

**F1. Complaint volume has grown, and 2023 is running higher.**
Complaints rose from 7,872 in 2018 to 12,953 in 2022. January to August 2023 has 9,131 complaints, about 1,141 a month, against about 1,079 a month in 2022.
*Implication:* the workload is growing, and 2023 has not slowed.
*Recommendation:* plan handling capacity against the 2022 to 2023 level, not the 2017 to 2019 level. *Owner:* complaint operations manager.
*Measure:* complaints per month, with monthly averages for partial years.

**F2. Checking and savings accounts dominate, and most of their complaints concern managing the account.**
Checking or savings is 39.7% of all complaints. "Managing an account" is 24.2% of all complaints and 61% of checking or savings complaints.
*Implication:* one product area and one issue drive much of the workload, so a fix there has wide reach.
*Recommendation:* review the account-management journey and what customers are told at each step. *Owner:* product owner, retail banking.
*Measure:* "Managing an account" complaints per month, before and after each change.

**F3. Timely responses are high overall, but lower for credit reporting and debt collection.**
96.1% of responded complaints are timely. Mortgage is 99.8%, while credit reporting is 93.7% and debt collection 93.6%. The difference across products is statistically clear (chi-square 414, p below 0.001).
*Implication:* about 1 in 16 responded complaints for credit reporting and debt collection is late.
*Recommendation:* review handling steps for those two products before the next reporting cycle. *Owner:* complaint operations manager.
*Measure:* timely rate by product, monthly, for responded complaints.

**F4. Monetary relief is concentrated in checking and credit card complaints.**
33.3% of closed checking or savings complaints, and 30.4% of credit card complaints, end with monetary relief. For credit reporting the rate is 3.6%, and for debt collection 4.1%.
*Implication:* the gap probably reflects the type of issue, since some problems are fixed with money and others by correcting records. The data cannot separate issue type from company practice.
*Recommendation:* compare relief rates within the same issue type before drawing any conclusion about fairness. *Owner:* policy analyst.
*Measure:* monetary relief rate by issue, not only by product.

**F5. The July 2023 spike is driven by account opening and account management.**
July 2023 had 1,749 complaints, about 113% above the monthly average. Checking or savings complaints were about 564 above an average month. "Opening an account" rose from about 34 a month to 183, moving from 4% to 10% of complaints. About a third of the month's complaints (618 of 1,749) came between 11 and 15 July.
*Implication:* a burst concentrated in one product and one step suggests a specific trigger, such as a product change, a fraud wave, or a system problem. The data cannot show which.
*Recommendation:* ask the product owner whether anything changed in account opening in early July 2023. Check the sub-issue "Account opened as a result of fraud" (160 complaints in July). *Owner:* consumer protection lead.
*Measure:* "Opening an account" complaints per week, with an alert threshold.

**F6. Most complaints are forwarded the same day, but 435 wait more than 30 days.**
79.4% of complaints are forwarded to the company on the day they are submitted, and 90% within 2 days. 435 took more than 30 days, and the longest took 275 days.
*Implication:* forwarding is fast for most complaints, but a long tail may be a data or process problem.
*Recommendation:* pull the 435 long-lag complaints and check whether the delay is in forwarding, recording or the data. *Owner:* complaint operations manager.
*Measure:* share forwarded within 2 days, monthly.

**F7. Recent timeliness cannot yet be judged.**
49% of July 2023 complaints and 82% of August 2023 complaints are still in progress, against 0% to 4% in earlier months.
*Implication:* a fall in timely rate in recent months would mislead until those complaints close.
*Recommendation:* report recent months with the in-progress share shown beside the timely rate. *Owner:* data team.
*Measure:* in-progress share by month.

## Caveats
- No company names, so findings are at product and issue level.
- Response time is not in the data; only the CFPB timely flag and forwarding time are used.
- Per-capita comparison by state (Q6) is not run, because no population data is included.
- Relief and timeliness differences are associations.

## Interview talking points
- Why in-progress complaints are excluded from timeliness rather than counted as late.
- Why a large sample makes the chi-square p-value less useful than the rates themselves.
- How the July 2023 spike was investigated, and why the company cannot be named.
