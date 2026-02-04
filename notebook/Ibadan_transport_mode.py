import random
import pandas as pd

random.seed(42)

n = 2000

# 10 areas total (7 within + 3 outskirts)
areas_within = ["Bodija", "Dugbe", "Mokola", "Challenge", "Agbowo", "Iwo Road", "Ring Road"]
areas_outskirts = ["Moniya", "Akinyele", "Apata"]

all_areas = areas_within + areas_outskirts

times = ["morning", "afternoon", "evening", "night"]
marital_statuses = ["single", "married"]
genders = ["male", "female"]

# 15 most popular jobs in Ibadan
job_income_map = {
    "student": (0, 30000),
    "civil servant": (30000, 200000),
    "market trader": (25000, 150000),
    "teacher": (35000, 100000),
    "artisan": (25000, 100000),
    "business owner": (40000, 500000),
    "driver": (30000, 100000),
    "shop attendant": (18000, 50000),
    "tailor": (20000, 80000),
    "hairdresser/barber": (20000, 80000),
    "trader": (30000, 150000),
    "mechanic": (30000, 100000),
    "security guard": (20000, 50000),
    "sales representative": (30000, 120000),
    "unemployed": (0, 0)
}

job_list = list(job_income_map.keys())


def get_realistic_job(age, gender, marital, income_bracket):
    """Assign jobs based on demographic factors"""

    # Age-based job filtering
    if age <= 22:
        likely_jobs = ["student", "shop attendant", "security guard", "unemployed"]
    elif age <= 25:
        likely_jobs = ["student", "sales representative", "shop attendant", "driver",
                       "unemployed", "artisan", "tailor"]
    elif age <= 35:
        likely_jobs = ["teacher", "civil servant", "market trader", "sales representative",
                       "artisan", "business owner", "driver", "mechanic", "trader"]
    elif age <= 50:
        likely_jobs = ["civil servant", "teacher", "business owner", "market trader",
                       "trader", "artisan", "mechanic"]
    else:
        likely_jobs = ["business owner", "market trader", "security guard", "civil servant",
                       "trader"]

    # Gender considerations (reflecting current realities)
    if gender == "female":
        female_common = ["teacher", "market trader", "hairdresser/barber", "tailor",
                         "shop attendant", "trader"]
        likely_jobs = [j for j in likely_jobs if j in female_common or
                       j in ["student", "unemployed", "civil servant", "business owner"]]

    # Marital status influence
    if marital == "married" and age > 30:
        stable_jobs = ["civil servant", "teacher", "artisan", "business owner", "mechanic"]
        likely_jobs = [j for j in likely_jobs if j in stable_jobs or random.random() < 0.3]

    if not likely_jobs:
        likely_jobs = job_list

    return random.choice(likely_jobs)


def get_commute_mode(area, job, income, time_of_day):
    """More realistic commute mode based on multiple factors"""

    is_outskirt = area in areas_outskirts

    # Base weights
    if is_outskirt:
        weights = {
            "commercial bus": 0.30,
            "okada": 0.28,
            "tricycle": 0.18,
            "private car": 0.12,
            "walking": 0.05,
            "micra": 0.07,
        }
    else:
        weights = {
            "commercial bus": 0.25,
            "okada": 0.20,
            "tricycle": 0.18,
            "private car": 0.18,
            "micra": 0.12,
            "walking": 0.07,
        }

    # Income adjustments
    if income > 150000:
        weights["private car"] = weights.get("private car", 0) * 3
        weights["okada"] = weights.get("okada", 0) * 0.3
    elif income < 30000:
        weights["walking"] = weights.get("walking", 0) * 2.5
        weights["commercial bus"] = weights.get("commercial bus", 0) * 1.5
        weights["private car"] = weights.get("private car", 0) * 0.1

    # Job-based adjustments
    high_status_jobs = ["civil servant", "teacher", "business owner"]
    if job in high_status_jobs and income > 80000:
        weights["private car"] = weights.get("private car", 0) * 2
        weights["okada"] = weights.get("okada", 0) * 0.5

    # Time-based adjustments
    if time_of_day == "night":
        weights["okada"] = weights.get("okada", 0) * 1.5
        weights["walking"] = weights.get("walking", 0) * 0.3

    # Normalize weights
    total = sum(weights.values())
    weights = {k: v / total for k, v in weights.items()}

    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]


def get_commute_distance(area, commute_mode):
    """Realistic distance based on area and mode"""

    if area in areas_outskirts:
        if commute_mode == "walking":
            return round(random.uniform(0.5, 3), 1)
        elif commute_mode in ["okada", "tricycle"]:
            return round(random.uniform(3, 18), 1)
        else:
            return round(random.uniform(10, 35), 1)
    else:
        if commute_mode == "walking":
            return round(random.uniform(0.3, 2.5), 1)
        elif commute_mode in ["okada", "tricycle"]:
            return round(random.uniform(1, 12), 1)
        else:
            return round(random.uniform(2, 18), 1)


rows = []

for _ in range(n):
    area = random.choice(all_areas)

    # More realistic time distribution
    time_of_day = random.choices(
        times, weights=[0.45, 0.30, 0.20, 0.05]
    )[0]

    # Age distribution closer to Nigerian demographics
    age = int(max(18, min(70, random.gauss(35, 12))))

    # Marital status based on age (only single and married)
    if age < 25:
        marital = random.choices(
            marital_statuses, weights=[0.80, 0.20]
        )[0]
    elif age < 35:
        marital = random.choices(
            marital_statuses, weights=[0.35, 0.65]
        )[0]
    else:
        marital = random.choices(
            marital_statuses, weights=[0.10, 0.90]
        )[0]

    gender = random.choice(genders)

    # Determine income bracket first
    if age < 25:
        income_bracket = "low"
    elif age < 40 and random.random() < 0.6:
        income_bracket = "medium"
    else:
        income_bracket = random.choice(["medium", "high"])

    job = get_realistic_job(age, gender, marital, income_bracket)

    inc_min, inc_max = job_income_map[job]
    if inc_min == inc_max == 0:
        income = 0
    else:
        income = random.randint(inc_min // 1000, inc_max // 1000) * 1000

    commuting = get_commute_mode(area, job, income, time_of_day)
    commute_distance = get_commute_distance(area, commuting)

    rows.append({
        "age": age,
        "time": time_of_day,
        "area": area,
        "marital_status": marital,
        "income": income,
        "job_description": job,
        "gender": gender,
        "commuting_means": commuting,
        "commute_distance_km": commute_distance
    })

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)

csv_filename = "ibadan_commute_2000.csv"
xlsx_filename = "ibadan_commute_2000.xlsx"

df.to_csv(csv_filename, index=False)
df.to_excel(xlsx_filename, index=False)

print(f"Saved {len(df)} rows to {csv_filename} and {xlsx_filename}")
print("\nSample statistics:")
print(f"Average age: {df['age'].mean():.1f}")
print(f"Average income: ₦{df['income'].mean():,.0f}")
print(f"\nGender distribution:")
print(df['gender'].value_counts())
print(f"\nMarital status distribution:")
print(df['marital_status'].value_counts())
print(f"\nTop 10 jobs:")
print(df['job_description'].value_counts().head(10))
print(f"\nTop 5 commute modes:")
print(df['commuting_means'].value_counts().head())
print(f"\nArea distribution:")
print(df['area'].value_counts())
