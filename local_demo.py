import csv, sqlite3
from pathlib import Path
root = Path(__file__).parent
conn = sqlite3.connect(":memory:")
conn.executescript("""CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, plan TEXT, region TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount_cents INTEGER);""")
for table, filename in [("customers","raw_customers.csv"),("orders","raw_orders.csv")]:
    with (root/"seeds"/filename).open() as f:
        reader = csv.reader(f)
        n = len(next(reader))
        conn.executemany(f"INSERT INTO {table} VALUES ({','.join('?'*n)})", reader)
assert conn.execute("SELECT count(*) FROM orders o LEFT JOIN customers c USING(customer_id) WHERE c.customer_id IS NULL").fetchone()[0] == 0
assert conn.execute("SELECT count(*) FROM orders WHERE status NOT IN ('completed','cancelled','refunded') OR amount_cents<0").fetchone()[0] == 0
rows = conn.execute("""SELECT region,count(*),sum(amount_cents) FROM orders JOIN customers USING(customer_id)
WHERE status='completed' GROUP BY region ORDER BY region""").fetchall()
for region,count,cents in rows:
    print(f"{region}: {count} completed orders | ${cents/100:,.2f}")
print(f"Total: {sum(r[1] for r in rows)} completed orders | ${sum(r[2] for r in rows)/100:,.2f}")
print("Local integrity checks passed.")
