import os
import urllib.request
import pandas as pd
import zipfile
import sqlite3

# DWD historical data URL hardcoded into function.
def download_file(filename):
    url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/monthly/kl/historical/" + filename

    # Get the parent directory of the current script. We save files to a /data folder.
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    save_location = os.path.join(parent_dir, "data", filename)

    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(save_location), exist_ok=True)

    try:
        urllib.request.urlretrieve(url, save_location)
        print("File downloaded successfully!")
    except Exception as e:
        print("Error occurred while downloading the file:", str(e))

def load_txt_from_zip(zip_filename, txt_filename):
    zip_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", zip_filename)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(txt_filename) as file:
            df = pd.read_csv(file, delimiter=";")

    clean_df(df)

    return df

def clean_df(df):
    if "eor" in df.columns:
        df.drop(columns=["eor"], inplace=True) # DWD data contains eor (end of record) column that we don't need.

    # DWD replaces missing or invalid data with -999. We need something better since comparing
    # missing or invalid data to valid data points should not be possible.
    df.replace(-999, pd.NA, inplace=True)

    # The date format is originally in YYYYMMDD. We also don't want time.
    df["MESS_DATUM_BEGINN"] = pd.to_datetime(df["MESS_DATUM_BEGINN"], format='%Y%m%d').dt.date
    df["MESS_DATUM_ENDE"] = pd.to_datetime(df["MESS_DATUM_ENDE"], format='%Y%m%d').dt.date

    # New YYYY-MM column since the days are often unnecessary.
    df["DATE"] = pd.to_datetime(df["MESS_DATUM_BEGINN"].apply(lambda x: x.strftime('%Y-%m')))
    date_series = df.pop("DATE")
    df.insert(1, "DATE", date_series)

def save_to_sqlite(pandas_df, table_name):
    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{table_name}.sqlite")
    conn = sqlite3.connect(db_location)

    try:
        pandas_df.to_sql(table_name, conn, if_exists='replace', index=False)
        print("Data saved to SQLite database successfully!")
    except Exception as e:
        print("Error occurred while saving data to SQLite database:", str(e))

    conn.close()

def save_to_csv(pandas_df, filename):
    csv_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{filename}.csv")

    try:
        pandas_df.to_csv(csv_location, index=False)
        print("Data saved to CSV successfully!")
    except Exception as e:
        print("Error occurred while saving data to CSV:", str(e))

def load_from_sqlite(table_name):
    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{table_name}.sqlite")
    conn = sqlite3.connect(db_location)

    try:
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn, parse_dates=['DATE'])
        print("Data loaded from SQLite database successfully!")
    except Exception as e:
        print("Error occurred while loading data from SQLite database:", str(e))

    conn.close()

    return df

def main():
    bamberg = "monatswerte_KL_00282_18810101_20231231_hist.zip"
    wuerzburg = "monatswerte_KL_05705_18810101_20231231_hist.zip"

    download_file(bamberg)
    download_file(wuerzburg)

    bamberg_data_file = "produkt_klima_monat_18810101_20231231_00282.txt"
    wuerzburg_data_file = "produkt_klima_monat_18810101_20231231_05705.txt"

    bamberg_df = load_txt_from_zip(bamberg, bamberg_data_file)
    wuerzburg_df = load_txt_from_zip(wuerzburg, wuerzburg_data_file)

    combined_df = pd.concat([bamberg_df, wuerzburg_df])

    save_to_sqlite(combined_df, 'franconian-weather')
    save_to_csv(combined_df, 'franconian-weather')

if __name__ == "__main__":
    main()
