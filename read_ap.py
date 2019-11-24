import openpyxl
import pandas as pd

# pd.set_option('max_columns', 10)
pd.set_option('max_rows', 30)

export_filename = 'aufwaende_zusammenfassung.xlsx'
filenames = ['1_1_Projekt_1.xlsx', '1_2_Projekt_2.xlsx', '1_3_Projekt_3.xlsx']
df = pd.DataFrame()


def get_last_row(ws):
    """
    2. Laenge des Dataframes bestimmen
        (abhaengig wie viele MA involviert sind)
    """
    for row in ws['D15:D50']:
        # print(type(row))
        # print(help(row[0]))
        print(row[0].value)
        if row[0].value == 'Summe':
            # print('Ziel erreicht')
            last_row = row[0].row - 1
            break
    return last_row


def read_new_data(filename, first_row, last_row):
    """
    3. Das Excel File (genauer den bestimmten Bereich des Excel Files) in einen
    Pandas Dataframe einlesen
    """
    df_new = pd.read_excel(filename,
                           usecols='D:J',
                           skiprows=first_row-1,
                           nrows=last_row-first_row)
    return df_new


for filename in filenames:
    """
    1. Excel File einlesen
        Startpunktposition ab der Daten eingelesen werden ist klar
    """
    wb = openpyxl.load_workbook(filename)
    ws = wb['Sheet1']

    first_row = 14
    last_row = get_last_row(ws)

    df_new = read_new_data(filename, first_row, last_row)

    df = df.append(df_new)

df_neu = df.groupby('Name').sum()
print(df.groupby('Name').sum())
"""
4. Stunden des jeweiligen MA im Quartal in ein dictionary
    schreiben.
    wenn MA oefter vorkommt, Stunden addieren
"""

"""
Rueckgabe: Dictionary mit Mitarbeiter, Kuerzel, Stunden, Abteilung
    Ausgabe der Daten im Dictionary in ein Excel Dokument
"""

# basierend auf 220 Arbeitstagen (pro Jahr, 250-30 Urlaub), 8h/Tag = 440h
avg_hours_quart = [440] * len(df_neu.index)
df_neu = df_neu.assign(Stunden_im_quartal=avg_hours_quart)
# print(df_neu['Summe [h]'])
# print(df_neu['avg_hours_quart'])
df_neu = df_neu.assign(Auslastung=df_neu['Summe [h]']/df_neu['Stunden_im_quartal'])
# print(df_neu[3])
df_neu.to_excel(export_filename)
