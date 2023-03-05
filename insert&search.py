import datetime
import create_db
import create_df


def find_area(building_number, street_name):
    area = create_df.df.loc[
        (create_df.df['Street'] == street_name) & (create_df.df['Number of Building'] == building_number), 'Area']
    return area


def insert_data(name, last_name, building_number, street_name, new_column):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    area = find_area(building_number, street_name)
    unique_id = str(datetime.datetime.now().timestamp()).replace('.', '')[:8]
    create_db.c.execute("INSERT INTO users2 VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (unique_id, name, last_name, street_name, building_number, str(area), time, new_column))
    create_db.conn.commit()


def output_area(client_id, building_number, street_name):
    row = create_db.c.execute("SELECT * FROM users2 WHERE id=? AND building_number=? AND street_name=?",
                              (client_id, building_number, street_name)).fetchone()
    if row:
        area = row[5]
        print("Area:", area)
        return area
    else:
        print("User not found with specified building number and street name")
        return None


insert_data('D', 'mima', '2', 'Тараса Шевченка проспект', 'ABC12345')
