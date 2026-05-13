import logging
import pandas as pd

from sqlalchemy import create_engine


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------
# PostgreSQL Connection
# ---------------------------------------------------

DATABASE_URL = (
    "postgresql://clinical_user:"
    "clinical_password@localhost:5433/" # matches docker-compose.yml
    "clinical_trials"
)

engine = create_engine(DATABASE_URL)


# ---------------------------------------------------
# Load CSV Files
# ---------------------------------------------------

def load_csv_files():

    logging.info("Loading raw clinical datasets...")

    dm_df = pd.read_csv("data/raw/dm.csv")

    vs_df = pd.read_csv("data/raw/vs.csv")

    ae_df = pd.read_csv("data/raw/ae.csv")

    return dm_df, vs_df, ae_df


# ---------------------------------------------------
# Load to PostgreSQL
# ---------------------------------------------------

def load_to_postgres(dm_df, vs_df, ae_df):

    logging.info("Loading DM dataset into PostgreSQL...")

    dm_df.to_sql(
        "raw_dm",
        engine,
        if_exists="replace",
        index=False
    )

    logging.info("Loading VS dataset into PostgreSQL...")

    vs_df.to_sql(
        "raw_vs",
        engine,
        if_exists="replace",
        index=False
    )

    logging.info("Loading AE dataset into PostgreSQL...")

    ae_df.to_sql(
        "raw_ae",
        engine,
        if_exists="replace",
        index=False
    )

    logging.info("All datasets loaded successfully.")


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    dm_df, vs_df, ae_df = load_csv_files()

    load_to_postgres(dm_df, vs_df, ae_df)


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":
    main()