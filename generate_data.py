"""
Generates a synthetic 'Brewline Coffee Co.' sales dataset:
transactional coffee-shop data across 3 stores over one year,
with realistic messiness (missing values, dupes, inconsistent casing)
for the cleaning step of the project to have real work to do.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

N_CUSTOMERS = 650
N_ORDERS = 6000
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)

stores = ["Downtown", "Riverside", "University Ave"]
store_weights = [0.42, 0.31, 0.27]

categories = {
    "Espresso Drinks": ["Latte", "Cappuccino", "Americano", "Espresso Shot", "Flat White"],
    "Brewed Coffee": ["Drip Coffee", "Cold Brew", "Pour Over"],
    "Tea": ["Chai Latte", "Green Tea", "Herbal Tea"],
    "Pastries": ["Croissant", "Muffin", "Scone", "Cinnamon Roll"],
    "Food": ["Breakfast Sandwich", "Avocado Toast", "Bagel"],
}
cat_weights = [0.38, 0.20, 0.10, 0.20, 0.12]

payment_methods = ["Card", "Mobile Pay", "Cash", "Gift Card"]
payment_weights = [0.48, 0.30, 0.15, 0.07]

genders = ["Female", "Male", "Non-binary", None]  # None -> missing on purpose
gender_weights = [0.47, 0.45, 0.05, 0.03]

# --- Customers table ---
customer_ids = [f"C{1000+i}" for i in range(N_CUSTOMERS)]
ages = rng.integers(18, 70, size=N_CUSTOMERS)
signup_days_ago = rng.integers(0, 700, size=N_CUSTOMERS)
loyalty_member = rng.choice([True, False], size=N_CUSTOMERS, p=[0.42, 0.58])
customer_gender = rng.choice(genders, size=N_CUSTOMERS, p=gender_weights)

customers = pd.DataFrame({
    "customer_id": customer_ids,
    "age": ages,
    "gender": customer_gender,
    "loyalty_member": loyalty_member,
    "signup_date": [ (datetime(2025,12,31) - timedelta(days=int(d))).date() for d in signup_days_ago ],
})

# introduce some messiness: duplicate a few customers, blank ages
dupe_idx = rng.choice(customers.index, size=8, replace=False)
customers = pd.concat([customers, customers.loc[dupe_idx]], ignore_index=True)
blank_age_idx = rng.choice(customers.index, size=15, replace=False)
customers.loc[blank_age_idx, "age"] = np.nan

customers.to_csv("/home/claude/project/data/customers_raw.csv", index=False)

# --- Orders table ---
date_range_days = (END_DATE - START_DATE).days
# seasonal weighting: more orders in fall/winter months (back-to-school, holidays), fewer mid-summer
day_offsets = rng.integers(0, date_range_days, size=N_ORDERS)
order_dates = [START_DATE + timedelta(days=int(d)) for d in day_offsets]

rows = []
for i in range(N_ORDERS):
    cust = rng.choice(customer_ids)
    store = rng.choice(stores, p=store_weights)
    cat = rng.choice(list(categories.keys()), p=cat_weights)
    item = rng.choice(categories[cat])
    qty = rng.choice([1, 1, 1, 2, 2, 3], size=1)[0]
    base_price = {
        "Espresso Drinks": rng.uniform(3.75, 5.75),
        "Brewed Coffee": rng.uniform(2.75, 4.25),
        "Tea": rng.uniform(3.25, 4.75),
        "Pastries": rng.uniform(2.50, 4.50),
        "Food": rng.uniform(5.50, 8.50),
    }[cat]
    unit_price = round(base_price, 2)
    payment = rng.choice(payment_methods, p=payment_weights)
    rating = rng.choice([np.nan, 1, 2, 3, 4, 5], p=[0.55, 0.01, 0.03, 0.11, 0.18, 0.12])

    rows.append({
        "order_id": f"ORD{10000+i}",
        "customer_id": cust,
        "order_date": order_dates[i].strftime("%Y-%m-%d"),
        "store_location": store,
        "category": cat,
        "item": item,
        "quantity": int(qty),
        "unit_price": unit_price,
        "payment_method": payment,
        "satisfaction_rating": rating,
    })

orders = pd.DataFrame(rows)

# messiness: inconsistent casing/whitespace in store_location and category (real-world dirty data)
messy_idx = rng.choice(orders.index, size=250, replace=False)
orders.loc[messy_idx, "store_location"] = orders.loc[messy_idx, "store_location"].str.lower()
messy_idx2 = rng.choice(orders.index, size=150, replace=False)
orders.loc[messy_idx2, "store_location"] = " " + orders.loc[messy_idx2, "store_location"] + " "

# duplicate a handful of orders exactly (data entry error)
dupe_orders_idx = rng.choice(orders.index, size=20, replace=False)
orders = pd.concat([orders, orders.loc[dupe_orders_idx]], ignore_index=True)

# a few negative/zero quantity glitches (POS error)
glitch_idx = rng.choice(orders.index, size=6, replace=False)
orders.loc[glitch_idx, "quantity"] = 0

orders.to_csv("/home/claude/project/data/orders_raw.csv", index=False)

print("customers_raw.csv:", customers.shape)
print("orders_raw.csv:", orders.shape)
