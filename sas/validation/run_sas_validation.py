import logging
import pandas as pd
import saspy


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------
# Initialize SAS Session
# ---------------------------------------------------

logging.info("Starting SAS session...")

sas = saspy.SASsession()


# ---------------------------------------------------
# Load VS Dataset
# ---------------------------------------------------

logging.info("Loading VS silver dataset...")

vs_df = pd.read_csv(
    "data/raw/vs.csv"
)


# ---------------------------------------------------
# Send DataFrame to SAS
# ---------------------------------------------------

logging.info("Sending VS dataset to SAS...")

sas.df2sd(
    vs_df,
    table="vs",
    libref="work"
)


# ---------------------------------------------------
# Run SAS Edit Checks
# ---------------------------------------------------

logging.info("Executing SAS validation checks...")

with open(
    "sas/edit_checks/vital_signs_checks.sas",
    "r"
) as file:

    sas_code = file.read()

results = sas.submit(sas_code)


# ---------------------------------------------------
# Retrieve Validation Findings
# ---------------------------------------------------

logging.info("Retrieving validation findings...")

issues_df = sas.sd2df(
    table="validation_issues",
    libref="work"
)


# ---------------------------------------------------
# Save Validation Results
# ---------------------------------------------------

issues_df.to_csv(
    "data/gold/vs_validation_issues.csv",
    index=False
)

logging.info(
    "Validation findings saved successfully."
)

logging.info(
    f"Issues Found: {len(issues_df)}"
)