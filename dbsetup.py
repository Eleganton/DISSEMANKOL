from models.userTable import UserTable
import random

majors = ["DAT", "DATØK", "ML", "DATKOG", "FYS", "BIO", "GEO", "KEM"]

# Generate 1000 unique random beer_count values between 1 and 2000 (for example)
beer_counts = random.sample(range(1, 501), 500)

setuptable = []
for i in range(1, 100):
    username = f"user{i}"
    major = majors[(i - 1) % len(majors)]
    beer_count = beer_counts[i - 1]
    u = UserTable(username=username, major=major, beer_count=beer_count, money_spent = 15*beer_count)
    setuptable.append(u)
    u.set_password("123")


