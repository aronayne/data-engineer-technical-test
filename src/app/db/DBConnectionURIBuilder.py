"""
Builds the connection string to MongoDB
"""
class DBConnectionURIBuilder:

    @staticmethod
    def build(username, password):
        return "mongodb+srv://"+username+":"+password+"@technical-test-cluster.zyqyw.mongodb.net/technicalTestDB?retryWrites=true&w=majority"
