import DBaccess as db
import pandas as pd
import re
from datetime import datetime

print ("Parsing excel..")
# Legge il file Excel
file_path = "HONOR Health-Data.xlsx"
sheet_name = "User's sleep information"

# Carica i dati dal foglio di lavoro specificato
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Funzione per estrarre valori con espressioni regolari
def extract_value(data_str, key):
    pattern = fr"{key}=(\d+)"
    match = re.search(pattern, data_str)
    return int(match.group(1)) if match else None

print("Inserting more or less ",len(data), "elements...")
bufferSize=2#0000
i=0
baseQuery="INSERT IGNORE INTO `health_Sleep` (`start`, `end`, `type`, `durationMinutes`) VALUES "
dataQuery=""
# Itera su ciascuna riga per elaborare i dati
for index, row in data.iterrows():
    # Recupera il valore della colonna startTime
    starttime = row.get("startTime", None)
    
    # Legge il contenuto della colonna preview
    preview_data = row.get("preview", "")

    # Estrae sleepTimestamp e wakeupTimestamp
    sleepTimestamp = extract_value(preview_data, "sleepTimestamp")
    startSleep=datetime.fromtimestamp(sleepTimestamp/1).strftime('%Y-%m-%d %H:%M:%S')
    wakeupTimestamp = extract_value(preview_data, "wakeupTimestamp")
    endSleep=datetime.fromtimestamp(wakeupTimestamp/1).strftime('%Y-%m-%d %H:%M:%S')
    sleep_time = datetime.fromtimestamp(sleepTimestamp)
    wakeup_time = datetime.fromtimestamp(wakeupTimestamp)
    duration_minutes = int((wakeup_time - sleep_time).total_seconds() / 60)

    # Stampa i risultati per verifica
    print(f"Row {index}: startTime={starttime}, sleepTimestamp={sleepTimestamp}, wakeupTimestamp={wakeupTimestamp}, startSleep={startSleep}, endSleep={endSleep}, duration={duration_minutes}")
    dataQuery+="('"+str(startSleep)+"', '"+str(endSleep)+"', 'SLEEP', '"+str(duration_minutes)+"'), "
    i += 1
    # facciamo l'insert ogni tot elementi
    if i%bufferSize==0:
        query=baseQuery+dataQuery[:-2]  
        #print(query);
        db.executeSql(query)
        dataQuery=""
# Perform the last insert
query=baseQuery+dataQuery[:-2]  
#print(query);
db.executeSql(query)

print("Inseriti ",i," elementi.")
