import pandas as pd

def station_selector(df, station):
    return df[df["STATIONS_ID"] == station]

def compare_features(df, feature):
    df_feature_diff = df[["STATIONS_ID", "DATE", feature]]
    df_feature_diff =  df_feature_diff.pivot_table(index='DATE', columns='STATIONS_ID', values=feature)
    df_feature_diff = df_feature_diff.dropna()
    df_feature_diff['DIFFERENCE'] = df_feature_diff[282] - df_feature_diff[5705]
    df_feature_diff['DIFFERENCE'] = df_feature_diff['DIFFERENCE'].abs()

    # Other functions need to know which feature this was.
    df_feature_diff.rename(columns={'DIFFERENCE': feature}, inplace=True)

    # Pivot format is morphing the header into two layers. Unmporph.
    df_feature_diff.reset_index(inplace=True)
    df_feature_diff.columns = ['DATE', '282', '5705', feature]

    return df_feature_diff

def compare_multiple_features(df, features):
    df_result = pd.DataFrame()
    
    for feature in features:
        df_feature_diff = compare_features(df, feature)
        
        if df_result.empty:
            df_result = df_feature_diff
        else:
            # Merge on 'DATE', including only the new feature column to avoid duplicating 'STATIONS_ID' columns
            df_result = pd.merge(df_result, df_feature_diff[['DATE', feature]], on='DATE', how='inner')
    
    return df_result

def first_date_with_data(df, feature):
    first_valid_index = df[feature].first_valid_index()
    first_valid_date = df.loc[first_valid_index, 'DATE']

    return first_valid_date

def main():
    import os
    import sqlite3
    import pandas as pd

    table_name = "franconian-weather"
    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{table_name}.sqlite")

    conn = sqlite3.connect(db_location)
    df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
    conn.close()

    df_282 = station_selector(df, 282)

    #print(df_282)

    df_MO_TT_compared = compare_features(df, "MO_TT")

    print("printing from main:\n", df_MO_TT_compared)

    df_multiple = compare_multiple_features(df, ['MX_TX', 'MO_TX', 'MO_TT'])
    print(df_multiple)

if __name__ == "__main__":
    main()