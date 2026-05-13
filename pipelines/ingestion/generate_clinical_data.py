import pandas as pd
import numpy as np
import random
import logging

from faker import Faker
from datetime import datetime, timedelta


# ---------------------------------------------------
# Logging Configuration
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

fake = Faker()


# ---------------------------------------------------
# Configuration
# ---------------------------------------------------

NUM_PATIENTS = 200

SITES = [
    "SITE001",
    "SITE002",
    "SITE003",
    "SITE004"
]

TREATMENT_ARMS = [
    "PLACEBO",
    "DRUG_A"
]

RACES = [
    "White",
    "Black or African American",
    "Asian",
    "American Indian or Alaska Native",
    "Native Hawaiian or Other Pacific Islander",
    "Other"
]

AE_TERMS = [
    "Headache",
    "Fatigue",
    "Nausea",
    "Rash",
    "Dizziness",
    "Vomiting",
    "Fever",
    "Injection Site Pain"
]


# ---------------------------------------------------
# Generate Demographics (DM)
# ---------------------------------------------------

def generate_demographics(num_patients=NUM_PATIENTS):

    logging.info("Generating demographics dataset...")

    records = []

    for i in range(num_patients):

        patient_id = f"SUBJ{1000 + i}"

        consent_date = fake.date_between(
            start_date="-1y",
            end_date="-30d"
        )

        age = random.randint(18, 85)

        # Intentionally inject bad data
        if random.random() < 0.02:
            age = -5

        record = {
            "patient_id": patient_id,
            "site_id": random.choice(SITES),
            "sex": random.choice(["M", "F"]),
            "age": age,
            "race": random.choice(RACES),
            "consent_date": consent_date,
            "treatment_arm": random.choice(TREATMENT_ARMS)
        }

        records.append(record)

    dm_df = pd.DataFrame(records)

    # Intentionally create duplicate patient
    duplicate_row = dm_df.iloc[0].copy()
    dm_df = pd.concat(
        [dm_df, pd.DataFrame([duplicate_row])],
        ignore_index=True
    )

    return dm_df


# ---------------------------------------------------
# Generate Vital Signs (VS)
# ---------------------------------------------------

def generate_vitals(dm_df):

    logging.info("Generating vital signs dataset...")

    records = []

    for _, patient in dm_df.iterrows():

        consent_date = pd.to_datetime(patient["consent_date"])

        for visit_num in range(1, 5):

            visit_date = consent_date + timedelta(days=visit_num * 7)

            systolic_bp = random.randint(90, 140)
            diastolic_bp = random.randint(60, 90)
            heart_rate = random.randint(55, 100)
            temperature = round(random.uniform(97.0, 99.5), 1)

            # Inject bad data intentionally
            if random.random() < 0.03:
                systolic_bp = 350

            if random.random() < 0.03:
                temperature = 109.0

            if random.random() < 0.03:
                visit_date = consent_date - timedelta(days=5)

            record = {
                "patient_id": patient["patient_id"],
                "visit_number": visit_num,
                "visit_date": visit_date,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "heart_rate": heart_rate,
                "temperature": temperature
            }

            records.append(record)

    vs_df = pd.DataFrame(records)

    return vs_df


# ---------------------------------------------------
# Generate Adverse Events (AE)
# ---------------------------------------------------

def generate_adverse_events(dm_df):

    logging.info("Generating adverse events dataset...")

    records = []

    for _, patient in dm_df.iterrows():

        has_ae = random.random() < 0.35

        if not has_ae:
            continue

        num_events = random.randint(1, 3)

        consent_date = pd.to_datetime(patient["consent_date"])

        for _ in range(num_events):

            start_date = consent_date + timedelta(
                days=random.randint(1, 120)
            )

            end_date = start_date + timedelta(
                days=random.randint(1, 10)
            )

            serious_flag = random.choice(["Y", "N"])

            record = {
                "patient_id": patient["patient_id"],
                "ae_term": random.choice(AE_TERMS),
                "severity": random.choice(
                    ["Mild", "Moderate", "Severe"]
                ),
                "start_date": start_date,
                "end_date": end_date,
                "serious_flag": serious_flag
            }

            records.append(record)

    ae_df = pd.DataFrame(records)

    return ae_df


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    logging.info("Starting synthetic clinical data generation...")

    dm_df = generate_demographics()

    vs_df = generate_vitals(dm_df)

    ae_df = generate_adverse_events(dm_df)

    logging.info("Saving datasets to data/raw/...")

    dm_df.to_csv("data/raw/dm.csv", index=False)

    vs_df.to_csv("data/raw/vs.csv", index=False)

    ae_df.to_csv("data/raw/ae.csv", index=False)

    logging.info("Clinical trial datasets generated successfully.")

    logging.info(f"DM Records: {len(dm_df)}")
    logging.info(f"VS Records: {len(vs_df)}")
    logging.info(f"AE Records: {len(ae_df)}")


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":
    main()