import psycopg2
import random
import string
import time
import sys
import os

# Set up base set for pseudo-names and insertion counter
letters = string.ascii_letters
cnt, refreshFreq = 0, int(os.environ["REFRESH_FREQ"])

# Set up connection parameters
sys.stdout.write(
    f"Running with statistics refresh every {refreshFreq} requests\n"
    "Waiting for 5 sec. to connect to database...\n\n"
)
time.sleep(5)

conn = psycopg2.connect(
    host=os.environ["DATABASE_HOST"],
    port='5432',
    database="lab",
    user="user",
    password="password"
)
cur = conn.cursor()

cur.execute("TRUNCATE accounting;")
cur.execute("ALTER SEQUENCE public.accounting_id_seq  RESTART WITH 1;")
conn.commit()

while True:
    # Statistics output section
    if cnt % refreshFreq == 0 and cnt != 0:
        cur.execute("SELECT AVG(items_bought) FROM accounting;")
        conn.commit()
        meanItems = round(cur.fetchone()[0], 2)
        
        cur.execute("SELECT AVG(balance) FROM accounting;")
        conn.commit()
        meanBalance = round(cur.fetchone()[0], 2)

        sys.stdout.write(
              f"\n\n{cnt // refreshFreq} -- ✨ <<STATISTICS>> ✨ -- {cnt // 3}\n"
              f"AVG. ITEMS BOUGHT  --> {meanItems}\n"
              f"AVG. CUST. BALANCE --> {meanBalance}\n\n"
        )
    
    # Create insertion query and insert new data row-by-row section
    clientName = (''.join(random.choice(letters) for i in range(10)))
    query = (
        "INSERT INTO accounting (client_name, items_bought, balance)"
        f"VALUES ('{clientName}', {random.randint(1,10)}, {random.randint(10,80)})"
    )

    try:
        cur.execute(query)
        conn.commit()
        sys.stdout.write(f"✅ ({cnt}): INSERT -> accounting ✅\n")

    except psycopg2.Error as e:
        sys.stderr.write(f"Error performing transaction {e}. Terminating ...")
        exit(1)
    
    # Increase insertion counter and sleep for 1 sec.
    cnt += 1
    time.sleep(1)

# Terminate connection
cur.close()
conn.close()
