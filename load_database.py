import os
import string
import time
import random
import datetime

import pandas as pd
import numpy as np

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

diagnoses_icd_path = "data/DIAGNOSES_ICD.csv"
d_icd_diagnoses_icd_path = "data/D_ICD_DIAGNOSES.csv"
patients_icd_path = "data/PATIENTS.csv"
chartevents_icd_path = "data/CHARTEVENTS.csv"
caregivers_icd_path = "data/CAREGIVERS.csv"
admissions_path = "data/ADMISSIONS.csv"
d_items_path = "data/D_ITEMS.csv"

diagnoses_icd_url = "https://physionet.org/files/mimiciii-demo/1.4/DIAGNOSES_ICD.csv"
d_icd_diagnoses_icd_url = (
    "https://physionet.org/files/mimiciii-demo/1.4/D_ICD_DIAGNOSES.csv"
)
patients_icd_url = "https://physionet.org/files/mimiciii-demo/1.4/PATIENTS.csv"
chartevents_icd_url = "https://physionet.org/files/mimiciii-demo/1.4/CHARTEVENTS.csv"
caregivers_icd_url = "https://physionet.org/files/mimiciii-demo/1.4/CAREGIVERS.csv"
admissions_url = "https://physionet.org/files/mimiciii-demo/1.4/ADMISSIONS.csv"
d_items_url = "https://physionet.org/files/mimiciii-demo/1.4/D_ITEMS.csv"

data_path_dict = {
    diagnoses_icd_path: diagnoses_icd_url,
    d_icd_diagnoses_icd_path: d_icd_diagnoses_icd_url,
    patients_icd_path: patients_icd_url,
    chartevents_icd_path: chartevents_icd_url,
    caregivers_icd_path: caregivers_icd_url,
    admissions_path: admissions_url,
    d_items_path: d_items_url,
}

data_path_dict = {
    "diagnoses_icd": [diagnoses_icd_path, diagnoses_icd_url],
    "d_icd_diagnoses": [d_icd_diagnoses_icd_path, d_icd_diagnoses_icd_url],
    "patients_icd": [patients_icd_path, patients_icd_url],
    "chartevents_icd": [chartevents_icd_path, chartevents_icd_url],
    "caregiver_icd": [caregivers_icd_path, caregivers_icd_url],
    "admissions": [admissions_path, admissions_url],
    "d_items": [d_items_path, d_items_url],
}


def load_date(paths):
    data_path, data_url = paths
    if os.path.exists(data_path):
        df = pd.read_csv(data_path, low_memory=False)
    else:
        df = pd.read_csv(data_url, low_memory=False)
        df.to_csv(data_path)

    return df


source_df_dict = {}
for key, item in data_path_dict.items():
    source_df_dict[key] = load_date(item)


# Utils
def random_name_generator():
    RANDS_CHARS = np.array(list(string.ascii_letters), dtype=(np.str_, 1))

    nchars = 8
    first_name = "".join(np.random.choice(RANDS_CHARS, nchars))
    last_name = "".join(np.random.choice(RANDS_CHARS, nchars))

    return first_name + " " + last_name


def random_word_generator():
    RANDS_CHARS = np.array(list(string.ascii_letters), dtype=(np.str_, 1))

    nchars = 8
    word = "".join(np.random.choice(RANDS_CHARS, nchars))

    return word


def random_number_generator(n=7):
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return random.randint(range_start, range_end)


def str_time_prop(start, end, time_format):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))

    ptime = stime + random.random() * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end):
    return str_time_prop(start, end, "%Y-%m-%d %I:%M:%S")


df_dict = {}


# Entities
def create_patient_df(source_df_dict):
    # Patient
    #  - ID - PATIENTS.subject_id
    #  - DOB - PATIENTS.dob
    #  - Name - generate
    #  - Ethinicity - ADMISSIONS.ethnicity
    #  - Gender - PATIENTS.gender

    patient_df = source_df_dict["patients_icd"][["subject_id", "dob", "gender"]]
    patient_df = pd.merge(
        patient_df,
        source_df_dict["admissions"][["subject_id", "ethnicity"]],
        on="subject_id",
        how="left",
    )

    patient_df = patient_df.rename(
        columns={
            "subject_id": "Patient ID",
            "dob": "DOB",
            "ethnicity": "Ethinicity",
            "gender": "Gender",
        }
    )

    patient_df["Name"] = [random_name_generator() for _ in range(len(patient_df))]

    patient_df = patient_df.drop_duplicates(subset=["Patient ID"])

    return patient_df


df_dict["patient_df"] = create_patient_df(source_df_dict)


def create_condition_df(source_df_dict):
    # Condition
    #  - ID - DIAGNOSES_ICD.icd9_code
    #  - Name - D_ICD_DIAGNOSES.short_title
    #  - Start Datetime - generate
    #  - End Datetime - generate
    #  - Stop Reason - generate

    condition_df = source_df_dict["diagnoses_icd"][
        ["subject_id", "icd9_code", "hadm_id"]
    ]
    condition_df = pd.merge(
        condition_df,
        source_df_dict["d_icd_diagnoses"][["icd9_code", "short_title"]],
        on="icd9_code",
        how="inner",
    )

    start = source_df_dict["admissions"]["admittime"].min()
    end = source_df_dict["admissions"]["admittime"].max()

    condition_df["Start Datetime"] = [
        random_date(start, end) for _ in range(len(condition_df))
    ]
    condition_df["Start Datetime"] = pd.to_datetime(condition_df["Start Datetime"])
    time_d = datetime.timedelta(days=2)
    condition_df["End Datetime"] = condition_df["Start Datetime"] + time_d

    condition_df["Stop Reason"] = [
        np.random.choice(["Treated", "Recovered"]) for _ in range(len(condition_df))
    ]

    condition_df = condition_df.rename(
        columns={
            "icd9_code": "Condition ID",
            "short_title": "Name",
            "Start Datetime": "Start Datetime",
            "End Datetime": "End Datetime",
            "Stop Reason": "Stop Reason",
            "hadm_id": "Visit ID",
        }
    )

    condition_df = condition_df.drop_duplicates(subset=["Condition ID"])

    return condition_df[
        [
            "Condition ID",
            "Name",
            "Start Datetime",
            "End Datetime",
            "Stop Reason",
            "Visit ID",
        ]
    ]


df_dict["condition_df"] = create_condition_df(source_df_dict)


def create_measurement_df(source_df_dict):
    # Measurement
    #  - ID - CHARTEVENTS.row_id
    #  - Name - CHARTEVENTS.itemid -> D_ITEMS.label
    #  - Measurment Datetime - CHARTEVENTS.charttime
    #  - Value as Number - CHARTEVENTS.valuenum
    #  - Unit - CHARTEVENTS.valueuom
    measurement_df = source_df_dict["chartevents_icd"][
        ["row_id", "itemid", "charttime", "valuenum", "valueuom", "hadm_id"]
    ]

    measurement_df = (
        pd.merge(
            measurement_df,
            source_df_dict["d_items"][["itemid", "label"]],
            on="itemid",
            how="inner",
        )
        .drop(columns=["itemid"])
        .rename(
            columns={
                "row_id": "Measurement ID",
                "label": "Name",
                "charttime": "Measurment Datetime",
                "valuenum": "Value as Number",
                "valueuom": "Unit",
                "hadm_id": "Visit ID",
            }
        )
    )

    return measurement_df[
        [
            "Measurement ID",
            "Measurment Datetime",
            "Value as Number",
            "Unit",
            "Name",
            "Visit ID",
        ]
    ]


df_dict["measurement_df"] = create_measurement_df(source_df_dict)


def create_doctor_df(source_df_dict, df_dict):
    # Doctor
    #  - Provider ID - CAREGIVERS.cgid
    #  - Name - generate
    #  - Gender - generate
    #  - Specialty - CAREGIVERS.label
    #  - DOB - generate

    doctor_df = source_df_dict["caregiver_icd"][["cgid", "label"]]
    doctor_df["DOB"] = [
        np.random.choice(df_dict["patient_df"]["DOB"]) for _ in range(len(doctor_df))
    ]
    doctor_df["Gender"] = [np.random.choice(["M", "F"]) for _ in range(len(doctor_df))]
    doctor_df["Name"] = [random_name_generator() for _ in range(len(doctor_df))]

    doctor_df = doctor_df.rename(
        columns={
            "cgid": "Provider ID",
            "label": "Specialty",
        }
    )

    return doctor_df[["Provider ID", "Name", "Gender", "Specialty", "DOB"]]


df_dict["doctor_df"] = create_doctor_df(source_df_dict, df_dict)


def create_hospital_df(source_df_dict, df_dict):
    # Hospital
    #  - Hospital ID - generate
    #  - Address - generate
    #  - Name - generate
    #  - ZIP - generate
    #  - County - generate
    #  - Hospital Capacity - generate
    #  - City - generate

    hospital_df = pd.DataFrame(
        [
            str(random_number_generator(4)) + " " + random_word_generator()
            for _ in range(len(df_dict["doctor_df"]) // 3)
        ],
        columns=["Address"],
    )

    hospital_df["Name"] = [random_name_generator() for _ in range(len(hospital_df))]
    hospital_df["ZIP"] = [random_number_generator(5) for _ in range(len(hospital_df))]
    hospital_df["County"] = [random_name_generator() for _ in range(len(hospital_df))]
    hospital_df["City"] = [random_name_generator() for _ in range(len(hospital_df))]
    hospital_df["Hospital Capacity"] = [
        random_number_generator(6) for _ in range(len(hospital_df))
    ]

    hospital_df["Hospital ID"] = [idx for idx in range(len(hospital_df))]

    return hospital_df[
        [
            "Hospital ID",
            "Address",
            "Name",
            "ZIP",
            "County",
            "City",
            "Hospital Capacity",
        ]
    ]


df_dict["hospital_df"] = create_hospital_df(source_df_dict, df_dict)


# Relations


def create_visit_df(source_df_dict, df_dict):
    # Visit
    #  - Visit ID - ADMISSIONS.hadm_id
    #  - Start Datetime - ADMISSIONS.admittime
    #  - End Datetime - ADMISSIONS.dischtime
    #  - Patient ID - ADMISSIONS.subject_id
    #  - Hospital ID - generate
    visit_df = source_df_dict["admissions"][
        ["hadm_id", "admittime", "dischtime", "subject_id"]
    ]

    visit_df["Hospital ID"] = [
        np.random.choice(df_dict["hospital_df"]["Hospital ID"])
        for _ in range(len(visit_df))
    ]

    visit_df = visit_df.rename(
        columns={
            "hadm_id": "Visit ID",
            "admittime": "Start Datetime",
            "dischtime": "End Datetime",
            "subject_id": "Patient ID",
        },
    )

    return visit_df[
        [
            "Visit ID",
            "Patient ID",
            "Hospital ID",
            "Start Datetime",
            "End Datetime",
        ]
    ]


df_dict["visit_df"] = create_visit_df(source_df_dict, df_dict)


def create_diagnosis_for_df(source_df_dict, df_dict):
    # Diagnosed For
    #  - Condition ID - DIAGNOSES_ICD.icd9_code
    #  - Patient ID - DIAGNOSES_ICD.subject_id
    diagnosed_for_df = (
        source_df_dict["diagnoses_icd"][["subject_id", "icd9_code"]]
        .rename(
            columns={
                "icd9_code": "Condition ID",
                "subject_id": "Patient ID",
            },
        )
        .drop_duplicates()
    )

    diagnosed_for_df = diagnosed_for_df.loc[
        diagnosed_for_df["Condition ID"].isin(df_dict["condition_df"]["Condition ID"])
    ].drop_duplicates(subset=["Condition ID"])

    return diagnosed_for_df[["Patient ID", "Condition ID"]]


df_dict["diagnosed_for_df"] = create_diagnosis_for_df(source_df_dict, df_dict)


def create_measured_on_df(source_df_dict, df_dict):
    # Measured On
    #  - Measurement ID - CHARTEVENTS.row_id
    #  - Patient ID - CHARTEVENTS.subject_id

    measured_on_df = source_df_dict["chartevents_icd"][["row_id", "subject_id"]].rename(
        columns={"row_id": "Measurement ID", "subject_id": "Patient ID"},
    )

    return measured_on_df[["Patient ID", "Measurement ID"]]


df_dict["measured_on_df"] = create_measured_on_df(source_df_dict, df_dict)


def create_performed_by_df(source_df_dict, df_dict):
    # Performed By
    #  - Measurement ID - CHARTEVENTS.row_id
    #  - Provider ID - CAREGIVERS.cgid
    """CREATE TABLE performed_by (
        provider_id INT REFERENCES doctor,
        measurement_id INT REFERENCES measurement,
        PRIMARY KEY (provider_id, measurement_id)
    );"""

    performed_by_df = source_df_dict["chartevents_icd"][["row_id", "cgid"]].rename(
        columns={"row_id": "Measurement ID", "cgid": "Provider ID"},
    )
    performed_by_df["Provider ID"] = performed_by_df["Provider ID"].astype(int)
    performed_by_df["Measurement ID"] = performed_by_df["Measurement ID"].astype(int)

    return performed_by_df[["Provider ID", "Measurement ID"]]


df_dict["performed_by_df"] = create_performed_by_df(source_df_dict, df_dict)


def create_diagnosis_by_df(source_df_dict, df_dict):
    # Diagnosed By
    #  - Condition ID - DIAGNOSES_ICD.icd9_code
    #  - Provider ID - CAREGIVERS.cgid

    diagnosed_by_df = source_df_dict["diagnoses_icd"][["icd9_code", "hadm_id"]].rename(
        columns={
            "icd9_code": "Condition ID",
        },
    )

    chartevents = source_df_dict["chartevents_icd"][["hadm_id", "cgid"]]

    diagnosed_by_df["Provider ID"] = [None for _ in range(len(diagnosed_by_df))]

    for i in range(len(diagnosed_by_df)):
        hadm = diagnosed_by_df.loc[i, "hadm_id"]
        cgids = chartevents.loc[chartevents["hadm_id"] == hadm, "cgid"]
        cgids = cgids if len(cgids) > 0 else [18999]
        diagnosed_by_df.loc[i, "Provider ID"] = int(np.random.choice(cgids))

    diagnosed_by_df = diagnosed_by_df.drop(columns=["hadm_id"])
    diagnosed_by_df = diagnosed_by_df.drop_duplicates()

    diagnosed_by_df = diagnosed_by_df.loc[
        diagnosed_by_df["Condition ID"].isin(df_dict["condition_df"]["Condition ID"])
    ].drop_duplicates(subset=["Condition ID"])

    diagnosed_by_df["Provider ID"] = diagnosed_by_df["Provider ID"].astype(int)

    return diagnosed_by_df[["Provider ID", "Condition ID"]]


df_dict["diagnosed_by_df"] = create_diagnosis_by_df(source_df_dict, df_dict)



conn = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432",
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# # Droping database MYDATABASE if already exists.
cursor.execute("DROP DATABASE IF EXISTS medicaldatabase")

# Preparing query to create a database
sql = "CREATE DATABASE medicaldatabase"
cursor.execute(sql)

cursor.close()
conn.commit()
conn.close()

conn = psycopg2.connect(
    dbname="medicaldatabase",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port="5432",
)

cursor = conn.cursor()


def create_tables(cursor):
    cursor.execute(
        """CREATE TABLE patient (
            patient_id INT PRIMARY KEY,
            dob CHAR(50),
            gender CHAR(1),
            ethnicity CHAR(100),
            name CHAR(50)
        );"""
    )

    cursor.execute(
        """CREATE TABLE doctor (
            provider_id INT PRIMARY KEY,
            name CHAR(50),
            gender CHAR(1),
            specialty CHAR(50),
            dob CHAR(50)
        );"""
    )

    cursor.execute(
        """CREATE TABLE hospital (
            hospital_id INT PRIMARY KEY,
            address CHAR(50),
            name CHAR(50),
            zip INT, 
            county CHAR(20),
            city CHAR(20),
            capacity INT
        );"""
    )

    cursor.execute(
        """CREATE TABLE visit (
            visit_id INT PRIMARY KEY,
            patient_id INT REFERENCES patient,
            hospital_id INT REFERENCES hospital,
            start_datetime CHAR(50),
            end_datetime CHAR(50)
        );"""
    )

    cursor.execute(
        """CREATE TABLE condition (
            condition_id CHAR(10) PRIMARY KEY,
            name CHAR(50),
            start_datetime CHAR(50),
            end_datetime CHAR(50),
            stop_reason CHAR(50),
            visit_id INT REFERENCES visit
        );"""
    )

    cursor.execute(
        """CREATE TABLE measurement (
            measurement_id INT PRIMARY KEY,
            measurement_datetime CHAR(50),
            value_as_number DECIMAL,
            unit CHAR(10),
            name CHAR(100),
            visit_id INT REFERENCES visit
        );"""
    )

    cursor.execute(
        """CREATE TABLE diagnosed_for (
            patient_id INT REFERENCES patient,
            condition_id CHAR(10) REFERENCES condition,
            PRIMARY KEY (patient_id, condition_id)
        );"""
    )

    cursor.execute(
        """CREATE TABLE measured_on (
            patient_id INT REFERENCES patient,
            measurement_id INT REFERENCES measurement,
            PRIMARY KEY (patient_id, measurement_id)
        );"""
    )

    cursor.execute(
        """CREATE TABLE performed_by (
            provider_id INT REFERENCES doctor,
            measurement_id INT REFERENCES measurement,
            PRIMARY KEY (provider_id, measurement_id)
        );"""
    )

    cursor.execute(
        """CREATE TABLE diagnosed_by (
            provider_id INT REFERENCES doctor,
            condition_id CHAR(10) REFERENCES condition,
            PRIMARY KEY (provider_id, condition_id)
        );"""
    )


def load_tables(cursor, df_dict):
    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["patient_df"].iterrows()
    )

    cursor.execute("INSERT INTO patient VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["doctor_df"].iterrows()
    )
    cursor.execute("INSERT INTO doctor VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["hospital_df"].iterrows()
    )
    cursor.execute("INSERT INTO hospital VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["visit_df"].iterrows()
    )
    cursor.execute("INSERT INTO visit VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["condition_df"].iterrows()
    )

    cursor.execute("INSERT INTO condition VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s,%s,%s,%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["measurement_df"].iterrows()
    )
    cursor.execute("INSERT INTO measurement VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["diagnosed_for_df"].iterrows()
    )
    cursor.execute("INSERT INTO diagnosed_for VALUES " + (values))

    values = ",".join(
        cursor.mogrify("(%s,%s)", row[1].values).decode("utf-8")
        for row in df_dict["diagnosed_by_df"].iterrows()
    )
    cursor.execute("INSERT INTO diagnosed_by VALUES " + (values))

    values = ",".join(
        cursor.mogrify(
            "(%s,%s)", [row[1].values[0].item(), row[1].values[1].item()]
        ).decode("utf-8")
        for row in df_dict["measured_on_df"].iterrows()
    )
    cursor.execute("INSERT INTO measured_on VALUES " + (values))

    values = ",".join(
        cursor.mogrify(
            "(%s,%s)", [row[1].values[0].item(), row[1].values[1].item()]
        ).decode("utf-8")
        for row in df_dict["performed_by_df"].iterrows()
    )
    cursor.execute("INSERT INTO performed_by VALUES " + (values))


create_tables(cursor)
load_tables(cursor, df_dict)

cursor.close()
conn.commit()
conn.close()
