import csv
import random

SEED = 42
NUM_SHARDS = 8
ROWS_PER_SHARD = 100

def generate_valid_email(rng, user_id):
    names = [
        "alice", "bob", "charlie", "david", "emma",
        "frank", "grace", "henry", "isla", "jack",
        "rahul", "alex", "jerry", "tom", "betty",
        "julian", "tim", "charles", "robert", "ho"
    ]
    domains = ["example.com", "example.org", "example.net"]
    name = rng.choice(names)
    domain = rng.choice(domains)
    return f"{name}{user_id}@{domain}"

def generate_row(rng, user_id):
    record = {
        "user_id": user_id,
        "name": f"User{user_id}",
        "email": generate_valid_email(rng, user_id),
    }
    if rng.random() < 0.2:
        record[rng.choice(["user_id", "name", "email"])] = None

    return record

def generate_shard(shard_index, rng):
    rows = []
    for i in range(ROWS_PER_SHARD):
        user_id = shard_index * ROWS_PER_SHARD + i + 1
        rows.append(generate_row(rng, user_id))
    return rows

def main():
    rng = random.Random(SEED)
    for shard_index in range(NUM_SHARDS):
        rows = generate_shard(shard_index, rng)
        with open(f"shard-{shard_index}.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "name", "email"])
            writer.writeheader()
            writer.writerows(rows)

if __name__ == "__main__":
    main()
