import os
import pandas as pd
import sqlite3
import zipfile
from FranconianWeather import download_file, load_txt_from_zip, clean_df, save_to_sqlite


# deletes files in the ../data subfolder
def delete_file_helper(filename):
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    file_location = os.path.join(parent_dir, "data", filename)
    os.remove(file_location)

def create_txt_file_helper(filename, content):
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    txt_file_path = os.path.join(parent_dir, "data", filename)

    with open(txt_file_path, 'w') as file:
        file.write(content)

def create_zip_file_helper(filename, file_to_zip):
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    zip_file_path = os.path.join(parent_dir, "data", filename)
    txt_file_path = os.path.join(parent_dir, "data", file_to_zip)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(txt_file_path, arcname=os.path.basename(txt_file_path))

def test_download_file():
    # Bamberg historical data is used for the download test
    filename = "monatswerte_KL_00282_18810101_20231231_hist.zip"

    download_file(filename)

    # Get the parent directory of the current script. We save files to a /data folder.
    parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    save_location = os.path.join(parent_dir, "data", filename)

    assert os.path.exists(save_location)

    delete_file_helper(filename)

def test_load_txt_from_zip():
    txt_filename = "test.txt"
    zip_filename = "test.zip"
    test_data = "The;quick;brown;fox;jumps;over;the;lazy;dog" # test data should be delimited with ";"

    test_data_in_array_form = [word for word in test_data.split(";")]

    create_txt_file_helper(txt_filename, test_data)
    create_zip_file_helper(zip_filename, txt_filename)

    df = load_txt_from_zip(zip_filename, txt_filename)
    expected_df = pd.DataFrame(columns=test_data_in_array_form)

    delete_file_helper(txt_filename)
    delete_file_helper(zip_filename)

    pd.testing.assert_frame_equal(df, expected_df)

def test_clean_df():
    test_data = [{"test": -999, "eor": "eor"}, {"test": 1.5, "eor": "eor"}]
    cleaned_test_data = [{"test": pd.NA}, {"test": 1.5}]

    df = pd.DataFrame(test_data)
    expected_df = pd.DataFrame(cleaned_test_data)

    clean_df(df) # operates in-place

    pd.testing.assert_frame_equal(df, expected_df)

def test_save_to_sqlite():
    df = pd.DataFrame([{"test": None}, {"test": 1.5}])
    test_table = "test_table"
    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{test_table}.sqlite")

    save_to_sqlite(df, test_table)

    conn = sqlite3.connect(db_location)
    loaded_df = pd.read_sql_query(f"SELECT * FROM {test_table}", conn)
    conn.close()

    delete_file_helper(f"{test_table}.sqlite")

    pd.testing.assert_frame_equal(df, loaded_df)

def test_pipeline():
    downloaded_zip_filename = "monatswerte_KL_00282_18810101_20231231_hist.zip"
    downloaded_data_filename = "produkt_klima_monat_18810101_20231231_00282.txt"
    expected_data_filename = "test.txt"
    test_table = "test_table"

    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{test_table}.sqlite")

    # Note: first row of (test) data is from 1881 and is note expected to change anytime soon.
    expected_data_headers = "STATIONS_ID;MESS_DATUM_BEGINN;MESS_DATUM_ENDE;QN_4;MO_N;MO_TT;MO_TX;MO_TN;MO_FK;MX_TX;MX_FX;MX_TN;MO_SD_S;QN_6;MO_RR;MX_RS;eor"
    expected_data_first_row = "        282;18810101;18810131;    5;  -999;   -999;   -2.70;    -999;-999;-999;-999;-999;-999;-999;-999;-999;eor"
    expected_data_content = expected_data_headers + "\n" + expected_data_first_row

    create_txt_file_helper(expected_data_filename, expected_data_content)

    expected_data_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", expected_data_filename)
    expected_df = pd.read_csv(expected_data_file_path, delimiter=";")

    clean_df(expected_df)
    expected_df.replace({pd.NA: None}, inplace=True) # clean creates pd.NA but loading makes them None. This is fine for now.

    # ETL pipeline
    download_file(downloaded_zip_filename) # Extract
    test_df = load_txt_from_zip(downloaded_zip_filename, downloaded_data_filename) # Transform
    save_to_sqlite(test_df.iloc[[0]], test_table) # Load

    conn = sqlite3.connect(db_location)
    loaded_df = pd.read_sql_query(f"SELECT * FROM {test_table}", conn)
    conn.close()

    # Cleanup
    delete_file_helper(downloaded_zip_filename)
    delete_file_helper(expected_data_filename)
    delete_file_helper(f"{test_table}.sqlite")

    pd.testing.assert_frame_equal(expected_df, loaded_df)
    

def main():
    test_download_file()
    test_load_txt_from_zip()
    test_clean_df()
    test_save_to_sqlite()

    test_pipeline()

if __name__ == "__main__":
    main()