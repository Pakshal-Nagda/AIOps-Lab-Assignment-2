import csv
import sys
import os

def validate_row(row):
    required_fields = ["user_id", "name", "email"]
    for field in required_fields:
        if not row.get(field):
            return False
    return True

def validate_csv(shard_number):
    filename = f"shard-{shard_number}.csv"
    invalid_rows = 0
    total_rows = 0
    with open(filename, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_rows += 1
            if not validate_row(row):
                invalid_rows += 1
    print(f"node={os.environ.get('NODE_NAME', 'unknown')} | "
          f"pod={os.environ.get('POD_NAME', 'unknown')} | "
          f"shard={shard_number} | "
          f"total_rows={total_rows} | "
          f"invalid_rows={invalid_rows}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate.py <shard-number>")
        sys.exit(1)
    validate_csv(sys.argv[1])
