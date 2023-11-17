import requests
import pymysql
url = "https://www.universal-tutorial.com/api/countries/"

headers = {
  'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7InVzZXJfZW1haWwiOiJhbmRyZWl2YW5uMTdAZ21haWwuY29tIiwiYXBpX3Rva2VuIjoiRk8xODM1cTdLelU3dmhFcVlteEd5bWh0WHlNbEczejYtTm9SV1A1TXhxUXlvbndrUzhGOWlTUXB0U2w2SGtIRm5VayJ9LCJleHAiOjE2OTEyNTIwMzZ9.74InZQtbPnVrLfDfrhfcrKrVuvAfd-hydQ2UD91TPEU'
}

data_countries = requests.request("GET", "https://www.universal-tutorial.com/api/countries/", headers=headers)

for country in data_countries.json():
    conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
    with conexion.cursor() as cursor:  
        cursor.execute(f'insert into countries (name) VALUES ("{str(country["country_name"])}");')  
        conexion.commit() 
        country_id = cursor.lastrowid
    data_states = requests.request("GET", "https://www.universal-tutorial.com/api/states/"+str(str(country["country_name"])), headers=headers)
    for state in data_states.json():
        conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
        state_id = -1
        with conexion.cursor() as cursor:  
            cursor.execute(f'insert into states (name,country_id) VALUES ("{str(state["state_name"])}","{str(country_id)}");')  
            conexion.commit() 
            state_id = cursor.lastrowid
        data_cities = requests.request("GET", "https://www.universal-tutorial.com/api/cities/"+str(str(state["state_name"])), headers=headers)
        for city in data_cities.json():
            conexion = pymysql.connect(host='localhost',user='root',password='',db='diabetic_macular_edema')
            with conexion.cursor() as cursor:  
          
                cursor.execute(f'insert into cities (name,state_id) VALUES ("{str(city["city_name"])}","{str(state_id)}")')  
                conexion.commit() 
            
