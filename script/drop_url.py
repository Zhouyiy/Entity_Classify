import pymongo
MONGO_URI = 'mongodb://140.143.185.58:27017'
DATABASE = 'scrapy'
client = pymongo.MongoClient(MONGO_URI)
db = client[DATABASE]
db.authenticate("root", "Mrrz#123")
db.drop_collection("result")
