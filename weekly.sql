CREATE TABLE IF NOT EXISTS public.mview_weekly_sales AS
SELECT 
    pos_site_id,
    sku_id,
    fsclwk_id,
    price_substate_id,
    type,
    SUM(sales_units) AS total_sales_units,
    SUM(sales_dollars) AS total_sales_dollars,
    SUM(discount_dollars) AS total_discount_dollars
FROM public.fact_transactions
GROUP BY pos_site_id, sku_id, fsclwk_id, price_substate_id, type;