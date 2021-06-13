import mysql.connector
def executeSql(query):
    mydb = mysql.connector.connect(host="127.0.0.1",user="user",passwd="password",database="DBname")
    mycursor = mydb.cursor() #(buffered=True)
    mycursor.execute(query)
    if query.startswith('SELECT ') :
        records = mycursor.fetchall()
    else :
        records = mydb.commit()
    return records