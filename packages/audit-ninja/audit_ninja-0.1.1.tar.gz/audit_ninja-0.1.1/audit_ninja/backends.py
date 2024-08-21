import os
import sys
from audit_ninja.settings import PROJECT_NAME, MONGO_DB_CREDS
from datetime import datetime
from pymongo import MongoClient

def get_mongo_db_handle(db_name, host, port, username, password):
    try:
        client = MongoClient(host=host,
                            port=int(port),
                            username=username,
                            password=password,
                            connect=False      
                            )    
        db_handle = client[db_name]
        return db_handle, client
    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, str(e))

def log_message(log_data,log_type):
    try:
        _, db_client = get_mongo_db_handle(
            MONGO_DB_CREDS["db_name"], 
            MONGO_DB_CREDS["host"], 
            MONGO_DB_CREDS["port"],
            MONGO_DB_CREDS["username"], 
            MONGO_DB_CREDS["password"]
            )
        
        # db_handle = db_client[PROJECT_NAME]
        # mycol = db_handle[collection_name]
        print('\n'*5)
        print('-'*50)
        print(log_data)
        print('-'*50)
        print('\n'*5)
        try:
            business_name = log_data.get('user_details',{}).get('business_name').replace(' ','')
        except:
            business_name = 'default'
        db_handle = db_client[business_name]
        mycol = db_handle[PROJECT_NAME]

        mycol.insert_one({"log_type":log_type, "log_data": log_data, "timestamp": datetime.now()})
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, str(e))



class ModelBackend:
    def request(self, request_info):
        log_message(request_info,"request_audit_logs")

    def crud(self, crud_info):
        log_message(crud_info, "crud_audit_logs")

    def login(self, login_info):
        log_message(login_info, "login_audit_logs")


# def push_record_to_mongo(collection_name, mydata):

#     print("db_handle----------", db_handle)
#     print("mongo_client--------->", mongo_client)

#     mycol = db_handle[collection_name]
#     if isinstance(mydata, list): 
#         """
#         Sample Data -->

#         mydata = [  {"data1" : "value"}, {"data2":"value"}  ]
        
#         """

#         x = mycol.insert_many(mydata)
#         print(x.inserted_ids)
#     else:
#         """
#         Sample Data -->

#         mydata = {"data" : "value"}
        
#         """

#         x = mycol.insert_one(mydata)
#         print(x.inserted_id)


# def list_mongo_data(collection_name, data=None):

#     print("db_handle----------", db_handle)
#     print("mongo_client--------->", mongo_client)

#     collection_handle = get_collection_handle(db_handle, collection_name)
        
#     if isinstance(data, dict):   
#         # Find One
#         x = collection_handle.find_one(data, sort=[('_id',pymongo.DESCENDING)])        # find_one() method returns the last occurrence in the selection.
#         pprint(x)
#         return x
              
#     else:
#         # Find All
#         response_list = []
#         for x in collection_handle.find({}):       # No parameters in the find() method gives you the same result as SELECT * in MySQL.
#             pprint(x)
#             response_list.append(x)
#         return response_list


