from database.leaves_db import (
    load_leaves_db
)

# =========================================================
# LOAD DB
# =========================================================

df = load_leaves_db()

# =========================================================
# EXPORT
# =========================================================

output_file = "data/leaves.xlsx"

df.to_excel(

    output_file,

    index=False
)

print("================================")

print(f"EXPORTED: {len(df)} leaves")

print(f"FILE: {output_file}")

print("================================")