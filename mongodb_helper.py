import datetime as dt
import pymongo

def getDbClient():
    srv_address = 'mongodb://brendathng:eusoffhall@cluster0-shard-00-00-dbct0.mongodb.net:27017,cluster0-shard-00-01-dbct0.mongodb.net:27017,cluster0-shard-00-02-dbct0.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true'
    client = pymongo.MongoClient(srv_address)
    return client

def returnToday(today): #return dataframe
  print('start')
  db_name='facilitiescalendar'
  collection_name = 'collection2'
  #second script for the bot

  client = getDbClient()
  db = client[db_name]
  collection = db[collection_name]
  today = today.strftime('%Y-%m-%d') 
  # today = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime('%Y-%m-%d') 
  print('today', today)
  print('collection', collection.find({'Date': today}))
  result = """ """
  all_results = collection.find({'Date': today})
  for event in all_results:
    print(event)
    t = event['Time']
    e = event['Event']
    print(t)
    print(e)
    result += """ \n {}: {}""".format(t, e)
  print(result)
  return result