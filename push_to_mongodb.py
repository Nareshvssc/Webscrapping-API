import pymongo
import logger_courseinfo



def check_mongo_db_login(username,password,data_base_name,collection_name):
    try:
        client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@myfirstscarpper.5r2ps.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mydb = client.test
        logger_courseinfo.logging_info("connection  established successfully with MONGODB" )
    except Exception as err:
        logger_courseinfo.logging_error("connection doesnt' established with MONGODB "+str(err))
        return False
    if data_base_name in client.list_database_names():
        logger_courseinfo.logging_info("the data base  exists ")
        mydb = client[data_base_name]
        if collection_name in mydb.list_collection_names():
            logger_courseinfo.logging_info(f"the collection {collection_name} exists in your database")
        else:
            return False
    else:
        return False
    return True


def add_to_mongodb(data,username,password,data_base_name,collection_name):
    # username='Naresh'
    # password='Naresh123'
    # data_base_name = 'Ineuronwebscarpper_1'
    # collection_name = 'Full_website_data'
    try:
        client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@myfirstscarpper.5r2ps.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        mydb = client[data_base_name]
        logger_courseinfo.logging_info(f"the collection {collection_name} exists in your database")
        if check_in_mongodb(client,data_base_name,collection_name,data):
            coll_1 = mydb[collection_name]
            coll_1.insert_one(data)
            logger_courseinfo.logging_info(f"the data is pushed successfully to your mongodb {collection_name} ")
        else:
            logger_courseinfo.logging_info(f"similar data {data['Type']} with {data['course_name']} was found in mongodb in {data_base_name} in your collection {collection_name} hence not inserted sorry ")
    except Exception as err:
            logger_courseinfo.logging_error(err)


    # try:
    #     #pushing the data if same collection doesnt exists
    #     col_1 = mydb["Full_website_data"]
    #     if col_1 in client.list_collection_names():
    #         logger_courseinfo.logging_info("the collection already exists ")
    #     else:
    #         logger_courseinfo.logging_info(f"created new collection {col_1}")
    #         col_1.insert_many(data)

def check_in_mongodb(client,data_base_name,collection_name,data):
    mydb = client[data_base_name]
    coll_1 =mydb[collection_name]
    f=1
    cursor = coll_1.find({},{'Type':1,'course_name':1})
    for i in cursor:
        if i['Type']==data['Type'] and i['course_name']==data['course_name']:
            f=0
            break
    if f==1:
        return True
    else:
        return False



if __name__=="__main__":
    check_mongo_db_login(username, password, data_base_name, collection_name)