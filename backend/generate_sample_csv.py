import csv
from datetime import date, timedelta
import random

# Generate sample CSV for consumption upload
with open("../data/sample_consumption.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["hostel", "date", "water_litres", "electricity_kwh", "gas_kg"])
    
    blocks = ["Block A", "Block B", "Block C", "Block D", "Block E", "Block F", "Block G", "Block H"]
    start_d = date.today() + timedelta(days=1)
    
    for i in range(14):
        curr_d = start_d + timedelta(days=i)
        for b in blocks:
            w = round(random.uniform(26000, 34000), 1)
            e = round(random.uniform(1150, 1600), 1)
            g = round(random.uniform(34, 48), 1)
            writer.writerow([b, str(curr_d), w, e, g])

print("Generated data/sample_consumption.csv with 112 rows.")
