import pandas as pd


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

def extracting_the_dataset(df):
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
    print(df)

if __name__ == "__main__":
    print(extracting_the_dataset(convert_file_data_to_dataframe("kharkov_street.txt")))