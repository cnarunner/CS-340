from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps  # To convert pymongo Cursor object to


class CRUD(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, USER, PASS):
        # Initializing the MongoClient. This helps to
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!

        # Connection Variables
        #
        #USER = 'aacuser'
        #PASS = 'simplepass'
        HOST = 'localhost'
        PORT = 27017
        DB = 'AAC'
        COL = 'animals'
        #
        # Initialize Connection
        #
        self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER, PASS, HOST, PORT))
        self.database = self.client['%s' % (DB)]
        self.collection = self.database['%s' % (COL)]

        print("Connection Successful")

    def create(self, data):
        """Method to implement the C in CRUD."""

        if data is not None:
            inserted = self.database.animals.insert_one(data)  # data should be dictionary

            # Checks to make sure it was successful.
            if inserted != 0:
                return True
            return False
        else:
            raise Exception("Nothing to save, data parameter is empty")

    def read(self, dataS):  # dataS is data to search.
        """Method to implement the R in CRUD."""

        if dataS is not None:
            read = self.database.animals.find(dataS, {"_id": False})
        else:
            raise Exception("Nothing to read, dataS parameter is empty.")
        return read

    def update(self, dataS, dataU):  # dataS is data to search, dataU is data to update.
        """Method to implement the U in CRUD."""

        if dataS and dataU is not None:
            updated = self.database.animals.update_many(dataS, {"$set": dataU})
        else:
            raise Exception("Nothing to update, dataS or data U parameters are empty.")
        return updated.modified_count

    def delete(self, dataD):  # dataD is data to delete.
        """Method to implement the D in CRUD."""

        if dataD is not None:
            deleted = self.database.animals.delete_many(dataD)
        else:
            raise Exception("nothing to delete, dataD parameter is empty")
        return deleted.deleted_count
