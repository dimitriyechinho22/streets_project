import pandas as pd
import sqlite3
from datetime import datetime

conn = sqlite3.connect('identifier.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS streets
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             last_name TEXT,
             street TEXT,
             time DATETIME,
            )''')
conn.commit()


def convert_file_data_to_dataframe(filename):
    """
    Функція приймає аргументом шлях до файлу (або назву файлу), редагує дані та повертає pandas Dataframe.
    :param filename: Назва файлу
    :return: pandas DataFrame.
    """
    with open(filename, "r", encoding="utf-8") as file:
        data_as_list = file.readlines()
        data_as_list = [i.rstrip().lstrip().replace("\t", " ")
                        for i in data_as_list]
        for elem in range(len(data_as_list)):
            data_as_list[elem] = [' '.join(data_as_list[elem].split()[:-2]), ' '.join(data_as_list[elem].split()[-2:])]

        main_dataframe = pd.DataFrame(data_as_list, columns=("Street", "Area"))
        return main_dataframe


def extracting_the_dataset(df) -> object:
    """
    Оскільки назви деяких вулиць були змінені і колишні назви важливі, створює нову
    колонку Past Names де будуть зберігатись колишні назви вулиць.
    :param df: основна таблиця вулиць
    :return: оновлена таблиця
    """

    df["Ex Names"] = df["Street"].str.extract("\((.*)\)")
    df["Ex Names"] = df["Ex Names"].str.replace("бывш.", "")
    df["Ex Names"].fillna("-", inplace=True)
    df["Street"] = df["Street"].str.replace("\(бывш\..*\)", "")
    return df


def get_street_area(name, last_name, street, df):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    area = df.loc[(df['Street'] == street) | (df['Ex Names'] == street), 'Area']
    c.execute('''INSERT INTO streets (name, last_name, street, time) VALUES (?, ?, ?, ?)''',
              (name, last_name, street, current_time))
    conn.commit()
    return area


if __name__ == "__main__":
    name = 'Misha'
    last_name = 'Dik'
    street = '8 Марта улица'
    print(get_street_area(name, last_name, street,
                              extracting_the_dataset(convert_file_data_to_dataframe("kharkov_street.txt"))))
