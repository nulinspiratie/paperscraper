

def get_entries(db):
    # prepare a cursor object using cursor() method
    # cursor = db.session.connection()

    results = {}
    for entry_type in ['authors', 'title_keywords', 'abstract_keywords']:
        try:
          # Execute the SQL command
          result = db.engine.execute(f"SELECT * FROM {entry_type}")
          # Fetch all the rows in a list of lists.
          results[entry_type] = [result[1] for result in result.fetchall()]
        except Exception as e:
          print("Error: unable to fetch data", e)
    return results