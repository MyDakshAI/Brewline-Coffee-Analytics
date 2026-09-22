# Brewline Coffee Co.: Sales & Customer Analytics

A data analytics portfolio project built the way the reference project was structured: Python for cleaning and EDA, SQL for business questions, a dashboard for visualization, and written findings at the end. The dataset is original and synthetic, so this one's actually mine to put on GitHub and LinkedIn.

## The scenario

Brewline Coffee Co. runs 3 stores (Downtown, Riverside, University Ave) and has a year of transaction data (2025) plus a customer table with loyalty status, age, and gender. Leadership wants to know which stores, products, and customer segments drive revenue, and where the opportunity is.

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
   Loads the raw CSVs, fixes the data quality issues (missing values, duplicate rows,
   inconsistent text casing, bad quantities), builds a few new fields (`age_group`,
   `total_amount`, `month`, `day_of_week`), and pokes around at revenue, customer, and
   product patterns. A later section adds RFM segmentation (Recency, Frequency,
   Monetary), scoring every customer and sorting them into groups like Champions,
   At Risk, and Lost.

2. **Data Analysis (SQL)**: `sql/analysis_queries.sql`
   Ten queries against a SQLite database built from the cleaned tables: monthly
   revenue trend, top items, revenue by store, loyalty segmentation, revenue by age
   group, repeat-customer identification, day-of-week patterns, payment method mix,
   satisfaction by category, and a window-function query ranking each store's monthly
   revenue.

3. **Visualization & Insights (Dashboard)**
   Live at:
   **https://claude.ai/artifact/VMQpvsugYihZDhDn9rwNNd**
   Filter by store to see how revenue, top items, and customer mix shift across
   locations. There's also a Power BI version that mirrors it, plus an extra
   Loyalty & Frequency page (more on that below).

4. **Report**: findings below.

5. **Publish**: push this folder to GitHub, pin it on your profile, write a LinkedIn
   post about one of the findings (see the suggested angle below).

6. **Iterate**: see "Ideas to extend this" if you want to keep going.

## Key findings

- Downtown is the top store by revenue (~$18.4K), about 33% ahead of University Ave, the weakest of the three.
- Espresso Drinks are the biggest category by far: 40% of all revenue, more than double Food, the next closest.
- Customers 55+ bring in the most revenue of any age group, even though they're not the biggest group by headcount. Worth digging into whether that's frequency or bigger orders.
- Loyalty membership barely changes anything on the surface. Average order value is basically the same for members and non-members ($7.34 vs. $7.44), and the frequency gap that might've explained the program turned out small too: members order 9.30 times a year on average vs. 9.16 for non-members, about 1.5% more. Neither basket size nor visit frequency shows a real lift from being a member.
- Monday is the busiest day, which matters for staffing.
- Card and Mobile Pay cover about 78% of transactions; cash is fading out.
- Running RFM on the customer base, 31.7% of customers (206 of 650) come back as At Risk or Lost/Hibernating: people who used to order a lot, or spent a lot, but haven't shown up in a while. That's a specific group a win-back campaign could actually target.
- The top 17.2% of customers, the Champions segment, account for almost a quarter of total revenue (24.8%). Useful number if you're trying to argue for protecting your best customers first.
- Loyalty membership does correlate with the healthier RFM segments, just not by a lot: 51% of Champions and 49% of Loyal Customers are members, compared to 42% of At Risk and 38% of Lost/Hibernating (the overall membership rate is 44.8%). So the plain average comparison above made the program look useless, but once you look at individual customers instead of group averages, there's a real, if modest, relationship hiding underneath.

## Suggested LinkedIn angle

A couple of ways to frame this, both built off pushing the loyalty question past the first answer:

1. Averages hid it, individuals didn't. Something like: *"I checked whether the loyalty program paid off through order size. It didn't. I checked visit frequency next, expecting that to be where it actually paid off, and it barely moved either. Comparing group averages, the program looked like it wasn't doing anything. Then I ran a full RFM segmentation on every customer and found a real pattern: loyalty members skew toward the healthy segments and away from At Risk or Lost. The signal was there, averaging just buried it."*
2. Lead with the business number. Something like: *"About a third of this coffee chain's customers, 206 out of 650, are At Risk or Lost by RFM standards, and the top 17% already generate a quarter of all revenue. That turns 'the loyalty program doesn't seem to be working' into an actual to-do list: here's who to win back, here's who to protect."*

Either works. The first shows you dig past the obvious metric; the second reads more like an action item for leadership.

## How to reproduce

```bash
python3 generate_data.py                          # (re)generate the raw synthetic data
python3 notebook/clean_and_analyze.py              # run the cleaning + EDA pipeline
# then open notebook/Brewline_Sales_Analysis.ipynb in Jupyter to see it cell-by-cell
```

`data/customers_clean.csv` and `data/orders_clean.csv` load straight into MySQL or
Postgres if you want real SQL software instead of SQLite. The queries in
`sql/analysis_queries.sql` are standard enough to work in either with small tweaks
(`strftime` becomes `DATE_TRUNC` in Postgres, for example).

For actual Power BI Desktop instead of the web dashboard, import `data/full_clean.csv`
directly. Every chart in the dashboard has a straightforward Power BI equivalent (line
chart for monthly revenue, donut for category mix, bar charts for the rest), with
`store_location` set up as a slicer. The Loyalty & Frequency page adds three measures,
`Distinct Customers`, `Orders per Customer`, and `Avg Order Value`, broken out by
`loyalty_member`, shown as a table plus a clustered column chart.

## Ideas to extend this

- ~~RFM segmentation to spot at-risk vs. VIP customers~~ (done, see `notebook/Brewline_Sales_Analysis.ipynb` Section 7 and `data/customer_segments.csv`).
- A cohort/retention analysis: do customers who signed up earlier order more over time?
- Basket analysis: which items tend to get bought together?
- Bring in weather or local event data to explain the monthly revenue dips and spikes.
- Fold the RFM segments into the dashboard or Power BI (revenue or customer count by segment).
