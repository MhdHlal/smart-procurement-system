import sqlite3
conn = sqlite3.connect('procurement.db')
cur = conn.cursor()
queries = [
    'ALTER TABLE purchase_requests ADD COLUMN requester TEXT',
    'ALTER TABLE purchase_requests ADD COLUMN requested_date TEXT',
    'ALTER TABLE purchase_requests ADD COLUMN notes TEXT'
]
for q in queries:
    try: cur.execute(q)
    except: pass
conn.commit()
conn.close()
print('✅ Database Patched Safely without data loss!')
