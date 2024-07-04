import analyzer
import FranconianWeather as fw
import pandas as pd
import seaborn as sns
sns.set_theme(style="darkgrid")
#import matplotlib
#matplotlib.use('Qt5Agg')  # Set the backend to Qt5Agg for hardware acceleration
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def feature_code_to_name(feature_code):
    feature_dict = {
        "STATIONS_ID": "Station ID",
        "DATE": "Date",
        "MESS_DATUM_BEGINN": "Start Date",
        "MESS_DATUM_ENDE": "End Date",
        "QN_4": "Quality Level",
        "MO_N": "Cloud Cover",
        "MO_TT": "Mean Temperature",
        "MO_TX": "Monthly Mean of Daily Max Temperature",
        "MO_TN": "Monthly Mean of Daily Min Temperature",
        "MO_FK": "Mean Wind Speed",
        "MX_TX": "Monthly Max Temperature",
        "MX_FX": "Max Wind Gust",
        "MX_TN": "Monthly Min Temperature",
        "MO_SD_S": "Sunshine Duration",
        "QN_6": "Quality Level",
        "MO_RR": "Total Rainfall",
        "MX_RS": "Max Rainfall"
    }

    return feature_dict[feature_code]

def feature_code_to_units(feature_code):
    feature_units_dict = {
        "STATIONS_ID": "",
        "DATE": "Year-Month",
        "MESS_DATUM_BEGINN": "",
        "MESS_DATUM_ENDE": "",
        "QN_4": "",
        "MO_N": "Okta",
        "MO_TT": "°C",
        "MO_TX": "°C",
        "MO_TN": "°C",
        "MO_FK": "Bft",
        "MX_TX": "°C",
        "MX_FX": "m/s",
        "MX_TN": "°C",
        "MO_SD_S": "Hours",
        "QN_6": "",
        "MO_RR": "mm",
        "MX_RS": "mm"
    }

    return feature_units_dict[feature_code]

def plot_feature_histogram(df, feature_code, ax=None, xlim=None, ylim=None):
    feature_name = feature_code_to_name(feature_code)
    feature_units = feature_code_to_units(feature_code)

    sns.histplot(df[feature_code], kde=True, ax=ax)
    ax.set_title(f"{feature_name} distribution")
    ax.set_xlabel(f"{feature_name} in {feature_units}")
    ax.set_ylabel("Frequency")

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

def plot_feature_line_graph(df, feature_code):
    feature_name = feature_code_to_name(feature_code)
    feature_units = feature_code_to_units(feature_code)

    sns.lineplot(x="DATE", y=feature_code, data=df)
    plt.title(f"{feature_name} over time")
    plt.xlabel("Date")
    plt.ylabel(f"{feature_name} in {feature_units}")

    # There's too many data points so we consolidate the x-axis
    # tickmarks to 5-year intervals.
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(base=5))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.margins(x=0.0)
    plt.show()

def plot_feature_scatter(df, feature_code_x, feature_code_y):
    feature_name_x = feature_code_to_name(feature_code_x)
    feature_units_x = feature_code_to_units(feature_code_x)

    feature_name_y = feature_code_to_name(feature_code_y)
    feature_units_y = feature_code_to_units(feature_code_y)

    sns.scatterplot(x=feature_code_x, y=feature_code_y, data=df)
    plt.title(f"{feature_name_x} vs {feature_name_y}")
    plt.xlabel(f"{feature_name_x} in {feature_units_x}")
    plt.ylabel(f"{feature_name_y} in {feature_units_y}")
    plt.tight_layout()
    plt.margins(x=0.0)
    plt.show()

def plot_feature_regression(df, feature_code_x, feature_code_y):
    feature_name_x = feature_code_to_name(feature_code_x)
    feature_units_x = feature_code_to_units(feature_code_x)

    feature_name_y = feature_code_to_name(feature_code_y)
    feature_units_y = feature_code_to_units(feature_code_y)

    if feature_code_x == 'DATE':
        # Instead of converting to timestamps, convert dates to days since a fixed date
        fixed_date = pd.to_datetime('1900-01-01')
        df_modified = df.copy(deep=True)
        df_modified['fDATE'] = pd.to_datetime(df_modified['DATE'])
        df_modified['fDATE'] = (df_modified['fDATE'] - fixed_date).dt.days
        feature_code_x = 'fDATE'
    else:
        df_modified = df

    sns.lmplot(x=feature_code_x, y=feature_code_y, data=df_modified,
               scatter_kws={'s': 10}, ci=95)
    
    plt.title(f"Absolute Difference in {feature_name_y}")
    plt.xlabel(f"{feature_name_x} in {feature_units_x}")
    plt.ylabel(f"{feature_name_y} in {feature_units_y}")

    if feature_code_x == 'fDATE':
        # Convert the numerical x-axis back to dates for labeling
        def format_date(days):
            return (fixed_date + pd.to_timedelta(days, unit='D')).strftime('%Y-%m-%d')
        plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: format_date(x)))
        plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.margins(x=0.0)
    plt.show()

def plot_temperature(df):

    colors = ["lightred", "lightblue"]
    station_ids = df['STATIONS_ID'].unique()

    sns.lineplot(data=df, x="DATE", y="MO_TT", hue="STATIONS_ID")

    for station_id, color in zip(station_ids, colors):
        df_station = df[df['STATIONS_ID'] == station_id]
        df_sorted = df_station.sort_values('DATE')
        x = df_sorted['DATE']
        y1 = df_sorted['MO_TN']  # Lower bound
        y2 = df_sorted['MO_TX']  # Upper bound

    plt.fill_between(x, y1, y2, color=color, alpha=0.5)
    plt.fill_between(x, y1, y2, color='gray', alpha=0.5)

    plt.tight_layout()
    plt.margins(x=0.0)
    plt.show()

def plot_boxplot(df, feature_codes):
    feature_units = feature_code_to_units(feature_codes[0])

    fig, ax = plt.subplots(figsize=(7, len(feature_codes) * 0.6))
    
    melted_df = pd.melt(df, value_vars=feature_codes, var_name='Feature', value_name='Value')
    melted_df['Feature Name'] = melted_df['Feature'].apply(feature_code_to_name)
    melted_df['Units'] = melted_df['Feature'].apply(feature_code_to_units)
    melted_df['Label'] = melted_df.apply(lambda x: f"{x['Feature Name']}", axis=1)
    
    sns.boxplot(data=melted_df, y='Label', x='Value', whis=[0, 100], width=.6, palette="vlag", ax=ax)
    sns.stripplot(data=melted_df, y='Label', x='Value', size=4, color=".3", ax=ax)
    
    plt.xlabel(f"{feature_units}")

    sns.set_theme(style="ticks")
 
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)
    
    plt.tight_layout()
    plt.show()

def main():
    import os
    import sqlite3
    import pandas as pd

    table_name = "franconian-weather"
    db_location = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data", f"{table_name}.sqlite")

    df = fw.load_from_sqlite(table_name)

    Bamberg_df = analyzer.station_selector(df, 282)
    Wuerzburg_df = analyzer.station_selector(df, 5705)
    
    print(Bamberg_df)

    #plot_feature_histogram(Bamberg_df, "MX_TX")

    Bamberg_yearly = Bamberg_df.copy(deep=True)
    Bamberg_yearly.set_index("DATE", inplace=True)
    Bamberg_yearly = Bamberg_yearly.resample("Y").max()

    #plot_feature_line_graph(Bamberg_yearly, "MX_TX")
    #plot_temperature(df)

    mean_temp_compared = analyzer.compare_features(df, "MO_TT")
    #multiple_temp_compared = analyzer.compare_multiple_features(df, ['MX_TX', 'MO_TX', 'MO_TT'])
    multiple_temp_compared = analyzer.compare_multiple_features(df, ['MX_TX', 'MO_TX', 'MO_TT', 'MO_TN', 'MX_TN'])
    
    
    #plot_feature_line_graph(mean_temp_compared, "MO_TT")
    print(mean_temp_compared)

    #plot_feature_regression(mean_temp_compared, 'DATE', 'MO_TT')
    #plot_boxplot(mean_temp_compared, 'MO_TT')
    plot_boxplot(multiple_temp_compared, ['MX_TX', 'MO_TX', 'MO_TT', 'MO_TN', 'MX_TN'])

if __name__ == "__main__":
    main()