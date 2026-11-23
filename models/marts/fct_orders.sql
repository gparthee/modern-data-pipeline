select o.order_id,o.customer_id,o.order_date,o.status,o.amount_cents,c.plan,c.region
from {{ ref('stg_orders') }} o join {{ ref('stg_customers') }} c on o.customer_id=c.customer_id
