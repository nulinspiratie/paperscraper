

def retrieve_data(db):
    # prepare a cursor object using cursor() method
    # cursor = db.session.connection()

    results = {}
    for table in ['authors', 'keywords', 'journals']:
        try:
            # Get columns
            columns = [column[0] for column in
                       db.engine.execute(f"SHOW COLUMNS FROM {table}").fetchall()]

            # Get results
            data = db.engine.execute(f"SELECT * FROM {table}").fetchall()
            # Fetch all the rows in a list of lists.
            results[table] = [{column: result[k] for k, column in enumerate(columns)}
                              for result in data]
        except Exception as e:
            print("Error: unable to fetch data", e)
    return results