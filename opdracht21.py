import time
import board
import busio
import adafruit_tsl2561
import pymssql

# Instellen van de I2C-bus en de lichtsensor
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_tsl2561.TSL2561(i2c)

# Functie om verbinding te maken met de Azure SQL Database
def connect_to_database():
    try:
        conn = pymssql.connect(
            host='lucasdegeusserver.database.windows.net', 
            port=1433,
            database='Thema10', 
            user='lucas@lucasdegeusserver', 
            password='Ripping2'
        )
        return conn
    except Exception as e:
        print("Fout bij het verbinden met de database:", e)
        return None

connect_to_database()
# Functie om lichtsensorwaarden in de database in te voegen
def insert_sensor_value(sensor_value):
    conn = connect_to_database()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        query = "INSERT INTO Oefening21 (sensorDevice, sensorValue, createDateTime) VALUES (%s, %s, %s);"
        cursor.execute(query, ('LichtSensor', sensor_value, time.strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        print(f"Succesvol ingevoerd: {sensor_value}")
    except Exception as e:
        print("Fout bij het invoegen van data:", e)
    finally:
        conn.close()

# Hoofdlus om elke 30 seconden een sensorwaarde te verzenden
def main():
    while True:
        try:
            # Lees de lichtintensiteit van de sensor
            lux = sensor.lux
            if lux is not None:
                print(f"Lichtintensiteit: {lux} lux")
                insert_sensor_value(lux)
            else:
                print("Lichtsensorwaarde niet beschikbaar.")
        except Exception as e:
            print("Fout bij het lezen van de sensor:", e)
        
        # Wacht 30 seconden voordat de volgende meting wordt gedaan
        time.sleep(30)

if __name__ == "__main__":
    main()
