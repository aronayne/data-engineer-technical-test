from src.app.db.MongoDBConnection import MongoDBConnection

"""
Utility function that watches for changes on a collection
"""
with MongoDBConnection() as mongo_conn:
    change_stream = mongo_conn.db.technicalTestCollection.watch()
    for change in change_stream:
        print(change)
        print('')  # for readability only
