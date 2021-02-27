# "C:\Program Files\MongoDB\Server\4.4\bin\mongo.exe"
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone

class DataManager():
    def __init__(self):
        self.client = MongoClient(host='localhost',connect=True,port=27017)
        self.db = self.client['stock_screener']
        self.timestamp = datetime.now()

    def add_info(self,info,collection):
        for i in info: 
            i['datetime'] = self.timestamp
        self.db[collection].insert_many(info)
        self.client.close()
        return True

    def add_one(self,info,collection):
        info['datetime'] = self.timestamp
        self.db[collection].insert_one(info)
        self.client.close()
        return True

    def find_info(self,collection,query_dict_gte={},query_dict_lte={}):
        if len(query_dict_gte) > 0 or len(query_dict_lte) > 0:
            query = self.build_query(query_dict_gte,query_dict_lte)
        else:
            query = {}
        cursor = self.db[collection].find(query)#.limit(limit)
        self.client.close()
        return list(cursor)

    def build_query(self,query_dict_gte,query_dict_lte):
        """
        takes the input dicts and creates a greater then or less 
        then filter, if dt is in the dict then 
        it makes dt = key instead same for ticker and setup 
        """
        return_query = {}
        for i in query_dict_gte:
            if i in ['dt','ticker','setup']:
                return_query[i] = query_dict_gte[i]
            else:
                return_query[i] = {"$gte": query_dict_gte[i]}
        for i in query_dict_lte:
            if i in ['dt','ticker','setup']:
                return_query[i] = query_dict_lte[i]
            else:
                return_query[i] = {"$lte": query_dict_lte[i]}
        return return_query

    def test_connection(self):
        try:
            self.db.command('serverStatus')
        except Exception as e:
            print(e)
        else:
            print("connection succesful, you are a wizard")
        self.client.close()



# test = DataManager()
# test.add_info([{'dt':'2020/09/01',"ticker":'FB','price':20,'rvol':3,'avg_vol':5456},{'dt':'2020/09/01',"ticker":'ETV','price':25,'rvol':3,'avg_vol':5456}],'test')
# result = test.find_info('test',{'price':21,'dt':'2020/09/01'})
# print(test.timestamp)