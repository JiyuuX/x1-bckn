import sqlite3
import csv

# Veritabanı dosyasının yolu
DATABASE_PATH = 'C:\\Users\\DEVRAN\\Downloads\\Yeni klasör (8)\\full-auth-api\\db.sqlite3'

# CSV dosyasının yolu
CSV_FILE_PATH = 'C:\\Users\\DEVRAN\\Downloads\\jpyt\\all_usernames.csv'

def insert_data_from_csv(db_path, csv_path):
    try:
        # SQLite veritabanına bağlan
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # CSV dosyasını oku
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Verileri eklemek için döngü
            for row in csv_reader:
                data_id = row['data_id']
                label = row['label']
                
                # Veriyi veritabanına ekle
                cursor.execute('''
                    INSERT INTO file_handler_alllabels (data_id, label)
                    VALUES (?, ?)
                ''', (data_id, label))

        # Değişiklikleri kaydet
        conn.commit()
        print("Data has been successfully inserted into AllLabels table.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Bağlantıyı kapat
        if conn:
            conn.close()

if __name__ == "__main__":
    insert_data_from_csv(DATABASE_PATH, CSV_FILE_PATH)
