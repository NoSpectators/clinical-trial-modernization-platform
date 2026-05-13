import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    when,
    lit
)


# ---------------------------------------------------
# Logging
# ---------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------------------------------------------
# Spark Session
# ---------------------------------------------------

spark = (
    SparkSession.builder
    .appName("ClinicalTrialSilverLayer")
    .getOrCreate()
)


# ---------------------------------------------------
# Load Bronze CSV Files
# ---------------------------------------------------

def load_bronze_data():

    logging.info("Loading bronze datasets...")

    dm_df = (
        spark.read
        .option("header", True)
        .csv("data/raw/dm.csv")
    )

    vs_df = (
        spark.read
        .option("header", True)
        .csv("data/raw/vs.csv")
    )

    ae_df = (
        spark.read
        .option("header", True)
        .csv("data/raw/ae.csv")
    )

    return dm_df, vs_df, ae_df


# ---------------------------------------------------
# Clean Demographics
# ---------------------------------------------------

def clean_demographics(dm_df):

    logging.info("Cleaning demographics dataset...")

    dm_clean = (
        dm_df
        .dropDuplicates(["patient_id"])
        .withColumn(
            "age",
            when(
                (col("age") < 0) |
                (col("age") > 120),
                None
            ).otherwise(col("age"))
        )
    )

    return dm_clean


# ---------------------------------------------------
# Clean Vital Signs
# ---------------------------------------------------

def clean_vitals(vs_df):

    logging.info("Cleaning vital signs dataset...")

    vs_clean = (
        vs_df
        .withColumn(
            "systolic_bp",
            when(
                (col("systolic_bp") < 40) |
                (col("systolic_bp") > 250),
                None
            ).otherwise(col("systolic_bp"))
        )
        .withColumn(
            "temperature",
            when(
                (col("temperature") < 95) |
                (col("temperature") > 105),
                None
            ).otherwise(col("temperature"))
        )
    )

    return vs_clean


# ---------------------------------------------------
# Clean Adverse Events
# ---------------------------------------------------

def clean_adverse_events(ae_df):

    logging.info("Cleaning adverse events dataset...")

    ae_clean = (
        ae_df
        .withColumn(
            "serious_flag",
            when(
                col("serious_flag").isin("Y", "N"),
                col("serious_flag")
            ).otherwise(lit("N"))
        )
    )

    return ae_clean


# ---------------------------------------------------
# Save Silver Layer
# ---------------------------------------------------

def save_silver_layer(dm_df, vs_df, ae_df):

    logging.info("Saving silver datasets...")

    (
        dm_df.write
        .mode("overwrite")
        .option("header", True)
        .csv("data/silver/dm")
    )

    (
        vs_df.write
        .mode("overwrite")
        .option("header", True)
        .csv("data/silver/vs")
    )

    (
        ae_df.write
        .mode("overwrite")
        .option("header", True)
        .csv("data/silver/ae")
    )

    logging.info("Silver layer saved successfully.")


# ---------------------------------------------------
# Main
# ---------------------------------------------------

def main():

    logging.info("Starting bronze-to-silver transformation...")

    dm_df, vs_df, ae_df = load_bronze_data()

    dm_clean = clean_demographics(dm_df)

    vs_clean = clean_vitals(vs_df)

    ae_clean = clean_adverse_events(ae_df)

    save_silver_layer(
        dm_clean,
        vs_clean,
        ae_clean
    )

    logging.info("Transformation completed successfully.")


# ---------------------------------------------------
# Entry Point
# ---------------------------------------------------

if __name__ == "__main__":
    main()