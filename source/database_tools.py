import MySQLdb
host = "nulinspiratie.mysql.pythonanywhere-services.com"
username = "nulinspiratie"
password = "mypassword"
database = "nulinspiratie$comments"


def get_entries():
    db = MySQLdb.connect(host, username, password, database)

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    results = {}
    for entry_type in ['authors', 'title_keywords', 'abstract_keywords']:
        try:
          # Execute the SQL command
          cursor.execute(f"SELECT * FROM {entry_type}")
          # Fetch all the rows in a list of lists.
          results[entry_type] = [result[1] for result in cursor.fetchall()]
        except Exception as e:
          print("Error: unable to fetch data", e)
    db.close()
    return results