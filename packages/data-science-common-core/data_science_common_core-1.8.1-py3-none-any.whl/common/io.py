"""Manage API calls and IO procedures."""
import binascii
import json
import logging
import os
import pickle
import sys
import time
from datetime import datetime

import google
import google.auth
from googleapiclient.discovery import build
import pandas as pd
import pgzip
from google.cloud import bigquery, storage
from slack_sdk import WebClient
from tqdm import tqdm

logging.Formatter.converter = time.gmtime

# Set standard output and standard error for the logs
logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
logger_format = "%(asctime)s [%(levelname)s] %(message)s"
formatter = logging.Formatter(logger_format)

h1 = logging.StreamHandler(sys.stdout)
h1.setLevel(logging.INFO)
h1.addFilter(lambda record: record.levelno <= logging.WARNING)
h1.setFormatter(formatter)

h2 = logging.StreamHandler()
h2.setLevel(logging.ERROR)
h2.setFormatter(formatter)
logger.addHandler(h1)
logger.addHandler(h2)


def get_slack_client(params):
    """Get slack client via bot authentication token."""
    return WebClient(token=params["slack_bot_oauth_secret"])


def auth_gsheets(params=None):
    """Authenticate to Google Spreadsheet."""
    # authenticate to Google Spreadsheet API
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()
    return sheet


def get_bq_client(params):
    """Get Google BigQuery client."""
    bq_client = bigquery.Client(project=params["google_project_id"])
    job_config = bigquery.QueryJobConfig(
        allow_large_results=True,
        flatten_results=True,
        labels={"project-name": params["project_name"]},
    )

    return bq_client, job_config


def get_storage_client(params):
    """Get Google Storage client."""
    return storage.Client(project=params["google_project_id"])


def get_data_bucket(params, storage_client):
    """Get Google Storage bucket."""
    return storage_client.bucket(params["gcs_bucket"])


def upload_to_bucket(params, file_path, suffix="", bucket_folder=None):
    """Upload file to Google blob storage.

    file_path: Pass the path of the file to upload from.

    suffix: Required file suffix

    bucket_folder: Name of the bucket folder.
        - model: To upload model pickle file.
        - ft: To upload feature transformer pickle file.
        - train_data: To upload the train and validation data during training mode.
        - test_data: To upload the test data during test mode.
    """
    # Select path on blob storage
    blob_path = (
        params[f"path_bucket_{bucket_folder}"]
        if bucket_folder != "model"
        else params[f"model_params_{params['model_type']}"]["path_bucket_model"]
    )

    # Append suffix if needed
    if suffix:
        blob_path += "-" + suffix

    msg = f"{params['session_id']} - {params['project_name']}: Uploading file to bucket"
    logger.info(msg)
    insert_logs(params, msg)

    # Fetch client
    client = get_storage_client(params)
    bucket = get_data_bucket(params, client)
    blob = bucket.blob(blob_path)

    # Upload file as blob
    blob.upload_from_filename(file_path, timeout=120)
    msg = f"{params['session_id']} - {params['project_name']}: File uploaded to bucket: {blob_path}"
    logger.info(msg)
    insert_logs(params, msg)

    return True


def download_from_bucket(params, blob_path):
    """Download file from Google blob storage.

    blob_path: Pass the path of the file to download from.

    returns: A file path of a downloaded file.
    """
    if os.path.exists(blob_path):
        msg = f"File exists {blob_path}"
        logger.warning(msg)
        insert_logs(params, msg)
        return ""

    else:
        # Fetch client
        client = get_storage_client(params)
        bucket = get_data_bucket(params, client)
        blob = bucket.blob(blob_path)

        # Download blob from bucket
        file_path = f"{params['folder_data']}/{blob_path.split('/')[-1]}"
        blob.download_to_filename(file_path)

        msg = f"File downloaded {file_path}"
        logger.info(msg)
        insert_logs(params, msg)
        return file_path


def insert_by_chunks(params, table_string, df):
    """Insert df to table with specified chunk size.

    table_string: Address of the table in DWH to insert the values.

    df: Table/DataFrame to insert the data from.

    """
    # Fetch client and output table
    client, _ = get_bq_client(params)
    table = client.get_table(table_string)

    n = df.shape[0]
    chunk_size = params["insertion_chunk_size"]
    chunk_num = n // chunk_size + 1

    msg = "Inserting to DWH"
    logger.info(msg)
    insert_logs(params, msg)

    for c in tqdm(range(chunk_num)):
        st = c * chunk_size
        ed = min(n, st + chunk_size)

        # Try insert data to output_table, then log status
        query_status = client.insert_rows(table, [*df.values[st:ed]])
        if len(query_status):
            msg = f"{params['session_id']} - {params['project_name']}: Insertion failed: {query_status}"
            logger.warning(msg)
            insert_logs(params, msg)

    return


def insert_logs(params: dict, message: str):
    """Create log entry to BigQuery."""
    if not params["dry_run"]:
        # Fetch client and output table
        client, _ = get_bq_client(params)
        log_table = client.get_table(
            f"{params['gbq_db_schema_log']}.{params['gbq_db_table_log']}"
        )

        row = [params["session_id"], datetime.utcnow(), params["project_name"], message]
        query_status = client.insert_rows(log_table, [row])
        if len(query_status):
            msg = f"{params['session_id']} - {params['project_name']}: Insertion failed: {query_status}"
            logger.warning(msg)
            insert_logs(params, msg)


def insert_to_bq(params, df):
    """Insert data to BigQuery table."""
    # Melt the data first to match structure
    df = pd.melt(df.reset_index(), id_vars=params["id_field"])

    # Define data to be inserted
    df["session_id"] = params["session_id"]
    df["version"] = params["version"]
    df["upload_date"] = datetime.utcnow()
    df["id_type"] = params["id_field"]

    # Rearrange rows to match schema
    df = df[
        [
            "session_id",
            "version",
            "upload_date",
            params["id_field"],
            "id_type",
            "variable",
            "value",
        ]
    ]
    df.columns = [
        ["session_id", "version", "upload_date", "id", "id_type", "pred_field", "pred"]
    ]

    out_table = f"{params['gbq_db_schema_out']}.{params['gbq_db_table_out']}"
    insert_by_chunks(params, out_table, df)

    return


def insert_metrics(params, results):
    """Insert training run's metrics to the DWH."""
    # Create a dataframe with 1 element as metrics
    out_dict = pd.DataFrame.from_records(
        [
            {
                "session_id": params["session_id"],
                "project_name": params["project_name"],
                "upload_date": datetime.utcnow(),
                "parameters": json.dumps(params),
                "metrics": json.dumps(results),
            }
        ]
    )

    client, _ = get_bq_client(params)
    out_table = client.get_table(
        f"{params['gbq_db_schema_metrics']}.{params['gbq_db_table_metrics']}"
    )

    # Insert row to the database
    client.insert_rows(out_table, list(out_dict.values))

    return


def read_from_sheet(params, mode="or"):
    """Insert data to Google Spreadsheet."""
    # Authenticate to Google Spreadsheet
    gsheet = auth_gsheets()

    # Call the Sheets API
    result = (
        gsheet.values()
        .get(
            spreadsheetId=params[f"gsheet_{mode}_file"],
            range=params[f"gsheet_{mode}_sheet"],
        )
        .execute()
    )
    # Get the values from the result
    return result.get("values", [])


def insert_to_sheet_new(
    params, data, mode="dest", replace=False, sheet_offset=None, include_col_header=True
):
    """Insert data to Google Spreadsheet."""
    msg = "Insert new predictions to Gsheet"
    insert_logs(params, msg)

    # Authenticate to Google Spreadsheet
    gsheet = auth_gsheets()

    # Convert any Timestamps to strings
    data = data.applymap(
        lambda x: x.isoformat() if isinstance(x, pd.Timestamp) else x
    ).reset_index(drop=not include_col_header)
    # Convert DataFrame to list of lists for Google Sheets, including column names
    data_list = [data.columns.tolist()] + data.reset_index(drop=True).values.tolist()

    # Clean the sheet if required
    if replace:
        gsheet.values().clear(
            spreadsheetId=params[f"gsheet_{mode}_file"],
            range=params[f"gsheet_{mode}_sheet"],
        ).execute()
        sheet = []

    else:
        # Fetch the current sheet data
        result = (
            gsheet.values()
            .get(
                spreadsheetId=params[f"gsheet_{mode}_file"],
                range=params[f"gsheet_{mode}_sheet"],
            )
            .execute()
        )
        sheet = result.get("values", [])

    # Check the current size of the sheet
    max_rows = len(sheet)
    max_cols = len(sheet[0]) if max_rows > 0 else 0

    # Calculate the target rows and columns after inserting the data
    num_rows, num_cols = len(data_list), len(data_list[0])
    start_row = sheet_offset[0] if sheet_offset else 0
    start_col = sheet_offset[1] if sheet_offset else 0

    # Calculate the end row and column
    end_row = start_row + num_rows
    end_col = start_col + num_cols

    # Expand the sheet with empty rows if necessary
    while len(sheet) < end_row:
        sheet.append([""] * max(num_cols, max_cols))

    # Expand each row with empty columns if necessary
    for row in sheet:
        while len(row) < end_col:
            row.append("")

    # Insert data into the sheet
    for i, row in enumerate(data_list):
        for j, value in enumerate(row):
            sheet[start_row + i][start_col + j] = value

    # Prepare the data for updating the sheet
    body = {"values": sheet}
    gsheet.values().update(
        spreadsheetId=params[f"gsheet_{mode}_file"],
        range=params[f"gsheet_{mode}_sheet"],
        valueInputOption="RAW",
        body=body,
    ).execute()

    return


def loader(params, target):
    """Load object from blob storage.

    - target: Name of the target file.
        - model: To download pre-trained model file.
        - ft: To download feature transformer file.
        - train_data: To download the train and validation data.
        - test_data: To download the test data.
    """
    # Select a target bucket path
    bucket_path = (
        params[f"model_params_{params['model_type']}"]["path_bucket_model"]
        if target == "model"
        else params[f"path_bucket_{target}"]
    )

    # Download the file path of a target
    logger.info(f"Downloading {bucket_path}...")
    file_path = download_from_bucket(params, bucket_path)

    # Use dill for ft
    logger.info(f"Loading in memory {file_path}...")
    with pgzip.open(file_path, "rb") as f:
        obj = pickle.load(f)

        return obj


def fetch_from_bucket(params, to_download=("train_data", "ft", "model", "test_data")):
    """Download object(s) from Google blob storage."""
    if isinstance(to_download, str):
        to_download = [to_download]

    # Store result objects
    return {target: loader(params, target) for target in to_download}


def ml_ft_upload(params):
    """Model-agnostic upload to bucket."""
    upload_to_bucket(params, params["path_ft_file"], bucket_folder="ft")
    upload_to_bucket(
        params,
        params[f"model_params_{params['model_type']}"]["path_model_file"],
        bucket_folder="model",
    )

    return


def cached_query(params, query):
    """Return query result via caching."""
    client, job_config = get_bq_client(params)
    today = datetime.utcnow()
    checksum = binascii.crc32(bytes(query, "ascii")) % (2**32)
    cache_path = f"data/query_{today.strftime(params['date_fmt'])}_{checksum:x}.pkl.gz"

    # Cache Hit, unpickle the file
    if os.path.exists(cache_path):
        logger.info("Using cached Query..")
        with pgzip.open(cache_path, "rb") as f:
            return pickle.load(f)
    else:
        logger.info("Cached query couldn't found, downloading..")
        df = client.query(query=query, job_config=job_config).to_dataframe(
            progress_bar_type="tqdm"
        )
        with pgzip.open(cache_path, "wb") as f:
            pickle.dump(df, f)
        return df


def read_bigquery_schema(params, schema_name, table_name):
    """Read schema from bigquery table."""
    # Fetch client
    client = bigquery.Client()

    # Fetch table info
    table = client.get_table(
        f"{params['google_project_id']}.{schema_name}.{table_name}"
    )

    return table.schema
