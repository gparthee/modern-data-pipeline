select customer_id, plan, region from {{ ref('raw_customers') }}
