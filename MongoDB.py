from pymongo import MongoClient
url = "mongodb://USERNAME:PASSWORD@ds155651.mlab.com:55651/derpy"
client = MongoClient(url)
db = client.derpy
def insert():
    employeeId = '5'
    employeeName = 'Desmond'
    employeeAge = 21
    employeeCountry = 'Singapore'    
    db.employees.insert_one(
        {
        "id": employeeId,
        "name":employeeName,
        "age":employeeAge,
        "country":employeeCountry
        }
    )
    print('\nInserted data successfully\n')


insert()
