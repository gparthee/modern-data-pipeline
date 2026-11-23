select order_date,region,count(*) as completed_orders,sum(amount_cents) as revenue_cents
from {{ ref('fct_orders') }} where status='completed' group by order_date,region
