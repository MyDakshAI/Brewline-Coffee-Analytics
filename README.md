# Brewline Coffee Co.: Sales & Customer Analytics

**A complete data analytics portfolio project**: Python (cleaning + EDA) → SQL (business analysis) → interactive dashboard → written findings, built the same way as the reference project, but with an original synthetic dataset so it's genuinely yours to put on GitHub/LinkedIn.

## The scenario

Brewline Coffee Co. runs 3 stores (Downtown, Riverside, University Ave) and has a year of transaction data (2025) plus a customer table with loyalty status, age, and gender. Leadership wants to know: which stores/products/customer segments drive revenue, and where's the opportunity?

## Project structure

```
data/
  customers_raw.csv        <- synthetic, intentionally messy (missing ages, dupes)
  orders_raw.csv           <- synthetic, intentionally messy (bad casing, dupes, glitches)
  customers_clean.csv      <- output of Step 1
  orders_clean.csv         <- output of Step 1
  full_clean.csv           <- merged, analysis-ready table
  customer_segments.csv    <- per-customer RFM scores + segment labels (Step 1 extension)
  brewline.db              <- SQLite database used in Step 2
  summary.json             <- key stats, also feeds the dashboard
  dashboard_data.json      <- pre-aggregated data embedded in the dashboard

notebook/
  Brewline_Sales_Analysis.ipynb   <- Step 1: cleaning + EDA (Python)

sql/
  analysis_queries.sql     <- Step 2: 10 business-question SQL queries

outputs/
  dashboard.html            <- Step 3: interactive dashboard (published link below)
  *.pbix                    <- Step 3b: Power BI version, incl. a Loyalty & Frequency page
```

## The 6 steps

1. **Data Preparation, Modeling & EDA (Python)**: `notebook/Brewline_Sales_Analysis.ipynb`
   Load the raw CSVs, find and fix data quality issues (missing values, duplicate rows,
   inconsistent text casing, invalid quantities), engineer new fields (`age_group`,
   `total_amount`, `month`, `day_of_week`), and explore revenue patterns visually. A later
   section adds an **RFM segmentation** (Recency, Frequency, Monetary) that scores every
   customer individually and buckets them into segments like Champions, At Risk, and Lost.

2. **Data Analysis (SQL)**: `sql/analysis_queries.sql`
   10 queries against a SQLite database built from the cleaned tables: monthly revenue
   trend, top items, revenue by store, loyalty segmentation, revenue by age group,
   repeat-customer identification, day-of-week patterns, payment method mix, satisfaction
   by category, and a window-function query ranking each store's monthly revenue.

3. **Visualization & Insights (Dashboard)**
   An interactive dashboard, live at:
   **https://claude.ai/artifact/VMQpvsugYihZDhDn9rwNNd**
   Filter by store to see how revenue, top items, and customer mix shift across locations.
   A Power BI version mirrors it 1:1, plus an extra **Loyalty & Frequency** page (see below).

4. **Report**: key findings summarized below.

5. **Publish**: push this folder to GitHub, pin it on your profile, write a LinkedIn post
   walking through one interesting finding (see "Suggested LinkedIn angle" below).

6. **Iterate**: see "Ideas to extend this" at the bottom if you want to go further.

## Key findings

- **Downtown is the top store** by revenue (~$18.4K), roughly 33% ahead of University Ave, the lowest performer.
- **Espresso Drinks dominate**: 40% of all revenue, more than double the next category (Food).
- **Customers 55+ generate the most revenue** of any age group, despite not being the largest segment, worth a follow-up: is this driven by higher order frequency or bigger baskets?
- **Loyalty membership barely moves either metric that matters.** Average order value is essentially flat (members: $7.34 vs. non-members: $7.44), and the frequency gap that might have explained the program is small too: members average **9.30 orders/customer** over the year vs. **9.16** for non-members, about a 1.5% difference. Neither basket size nor visit frequency shows a meaningful lift from membership in this data.
- **Monday is the busiest day**: useful for staffing decisions.
- **Card and Mobile Pay make up ~78% of transactions**: cash is a shrinking share.
- **RFM segmentation shows 31.7% of customers (206 of 650) are At Risk or Lost/Hibernating**: customers who used to order regularly (or spent a lot) but haven't been back recently. That's a concrete, targetable group for a win-back campaign.
- **The top 17.2% of customers (Champions) generate 24.8% of total revenue**: a clear number for "protect your best customers first" if retention budget is limited.
- **Loyalty membership does skew toward the healthy RFM segments, just mildly:** 51% of Champions and 49% of Loyal Customers are loyalty members, vs. 42% of At Risk and only 38% of Lost/Hibernating customers (baseline membership rate is 44.8%). The aggregate AOV/frequency comparison above made it look like the program does nothing. Segmenting individual customers reveals a small but real association that group averages washed out.

## Suggested LinkedIn angle

Two options, both from following the loyalty question past the first plausible answer:

1. **The averages-vs-individuals story.** *"I checked whether the loyalty program paid off through order size. It didn't. So I checked visit frequency instead, expecting that to be the real payoff, and it barely moved the needle either (9.30 orders/customer vs. 9.16). Comparing group averages made it look like the program does nothing. Then I ran a full RFM segmentation on every customer individually, and a real (if modest) pattern showed up: loyalty members are meaningfully more likely to land in the 'healthy' segments and less likely to be At Risk or Lost. The averages hid a signal that only showed up once I stopped averaging."*
2. **The retention-targeting story.** *"Nearly a third of this coffee chain's customers (206 of 650) are At Risk or Lost by RFM standards, and the top 17% of customers already generate a quarter of all revenue. That's the kind of number that turns 'the loyalty program isn't working' into an actual to-do list: here's exactly who to win back, and here's exactly who to protect."*

Either works as the portfolio hook; the first is more "I dug deeper than the obvious metric," the second is more "here's a business action, not just a finding."

## How to reproduce

```bash
python3 generate_data.py                          # (re)generate the raw synthetic data
python3 notebook/clean_and_analyze.py              # run the cleaning + EDA pipeline
# then open notebook/Brewline_Sales_Analysis.ipynb in Jupyter to see it cell-by-cell
```

To load into real SQL software instead of SQLite, `data/customers_clean.csv` and
`data/orders_clean.csv` import directly into MySQL/PostgreSQL. The queries in
`sql/analysis_queries.sql` use standard syntax that works in both with minor tweaks
(e.g., `strftime` → `DATE_TRUNC` in Postgres).

To load into **actual Power BI Desktop** instead of the web dashboard: import
`data/full_clean.csv` directly, every chart in the dashboard maps to a straightforward
Power BI visual (line chart for monthly revenue, donut for category mix, bar charts for
the rest), with `store_location` as a slicer. The **Loyalty & Frequency** page adds three
measures (`Distinct Customers`, `Orders per Customer`, and `Avg Order Value`) broken out
by `loyalty_member`, as a table plus a clustered column chart.

## Ideas to extend this

- ~~Build an RFM segmentation to identify at-risk vs. VIP customers~~ (done, see `notebook/Brewline_Sales_Analysis.ipynb` Section 7 and `data/customer_segments.csv`).
- Add a **customer cohort/retention analysis**: do customers who signed up early order more over time?
- Add **basket analysis**: which items are commonly bought together?
- Bring in **weather or local event data** to explain the monthly revenue dips/spikes.
- Build an RFM segment breakdown into the dashboard/Power BI (revenue or customer count by segment).
