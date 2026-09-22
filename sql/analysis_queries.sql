-- ============================================================
-- Brewline Coffee Co. — SQL Analysis
-- Step 2 of the portfolio project: business-question queries
-- run against the cleaned `customers` and `orders` tables.
-- (SQLite syntax; portable to MySQL/PostgreSQL with minor tweaks)
-- ============================================================

-- 1. Monthly revenue trend
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(total_amount), 2)   AS revenue,
    COUNT(DISTINCT order_id)      AS orders
FROM orders
GROUP BY month
ORDER BY month;

-- 2. Top 10 items by revenue
SELECT
    item,
    category,
    COUNT(*)                      AS times_ordered,
    ROUND(SUM(total_amount), 2)   AS revenue
FROM orders
GROUP BY item, category
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue and average order value by store
SELECT
    store_location,
    COUNT(DISTINCT order_id)      AS orders,
    ROUND(SUM(total_amount), 2)   AS revenue,
    ROUND(AVG(total_amount), 2)   AS avg_order_value
FROM orders
GROUP BY store_location
ORDER BY revenue DESC;

-- 4. Customer segmentation: loyalty members vs. non-members
SELECT
    c.loyalty_member,
    COUNT(DISTINCT c.customer_id)     AS customers,
    ROUND(AVG(order_totals.total), 2) AS avg_spend_per_customer
FROM customers c
JOIN (
    SELECT customer_id, SUM(total_amount) AS total
    FROM orders
    GROUP BY customer_id
) order_totals ON order_totals.customer_id = c.customer_id
GROUP BY c.loyalty_member;

-- 5. Revenue by age group (join customers -> orders)
SELECT
    c.age_group,
    ROUND(SUM(o.total_amount), 2) AS revenue,
    COUNT(DISTINCT o.order_id)    AS orders
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY c.age_group
ORDER BY revenue DESC;

-- 6. Repeat customers: how many orders has each customer placed?
--    (classic "who are our most loyal customers" query)
SELECT
    customer_id,
    COUNT(DISTINCT order_id)      AS num_orders,
    ROUND(SUM(total_amount), 2)   AS lifetime_spend
FROM orders
GROUP BY customer_id
HAVING num_orders >= 15
ORDER BY lifetime_spend DESC
LIMIT 15;

-- 7. Day-of-week ordering pattern (staffing/inventory planning use case)
SELECT
    day_of_week,
    COUNT(DISTINCT order_id)      AS orders,
    ROUND(AVG(total_amount), 2)   AS avg_order_value
FROM orders
GROUP BY day_of_week
ORDER BY orders DESC;

-- 8. Payment method mix
SELECT
    payment_method,
    COUNT(DISTINCT order_id)          AS orders,
    ROUND(100.0 * COUNT(DISTINCT order_id) /
        (SELECT COUNT(DISTINCT order_id) FROM orders), 1) AS pct_of_orders
FROM orders
GROUP BY payment_method
ORDER BY orders DESC;

-- 9. Average satisfaction rating by category (only rated orders)
SELECT
    category,
    COUNT(satisfaction_rating)        AS rated_orders,
    ROUND(AVG(satisfaction_rating),2) AS avg_rating
FROM orders
WHERE satisfaction_rating IS NOT NULL
GROUP BY category
ORDER BY avg_rating DESC;

-- 10. Window function example: each store's rank by monthly revenue
SELECT
    month,
    store_location,
    revenue,
    RANK() OVER (PARTITION BY month ORDER BY revenue DESC) AS rank_in_month
FROM (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        store_location,
        ROUND(SUM(total_amount), 2)   AS revenue
    FROM orders
    GROUP BY month, store_location
)
ORDER BY month, rank_in_month;
