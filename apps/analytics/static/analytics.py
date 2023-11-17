import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_sql_mes(startDate,endDate):       

    consulta = f"""
SELECT 
months.name as name,
months.id as num,
  COALESCE(count(d.id), 0) as total
FROM months
left join detections d  ON MONTH(d.datetime) = months.id 
  AND datetime between CAST('{startDate}' AS DATE) AND  CAST('{endDate}' AS DATE)  
GROUP BY months.id 
ORDER BY months.id;
    """
    cnx = pymysql.connect(user='root', password='',
                              host='localhost', database='diabetic_macular_edema')
    cursor = cnx.cursor()
    ventas_por_dia = [0] * 12
    cursor.execute(consulta)
    for mes,num, total_ventas in cursor:
        ventas_por_dia[int(num)-1]= str(total_ventas)

    combinada = [list(pair) for pair in zip(months, ventas_por_dia)]
    return {"totalData": ventas_por_dia,"tableBody": combinada,"title":"Month"}
def get_sql_days(startDate,endDate):
    engine = create_engine(connect_info)
    
    consulta = f"""
    WITH RECURSIVE DateSeries AS (
        SELECT CAST('{startDate}' AS DATE) AS date
        UNION ALL
        SELECT DATE_ADD(date, INTERVAL 1 DAY)
        FROM DateSeries 
        WHERE DATE_ADD(date, INTERVAL 1 DAY) <= CAST('{endDate}' AS DATE)
    )
    SELECT 
        ds.date,
        DAYNAME(ds.date) AS day_of_week,
        COUNT(d.id) AS total
    FROM DateSeries ds
    LEFT JOIN detections d ON DATE(d.datetime) = ds.date
    GROUP BY ds.date
    ORDER BY ds.date;
    """
 
    df = pd.read_sql_query(sql=consulta, con=engine)
    return {"data":df.values}
    
def get_sql_semana(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"""
SELECT 
      CASE 
        WHEN days_of_week.day_of_week = 1 THEN 'Sunday' 
        WHEN days_of_week.day_of_week = 2 THEN 'Monday' 
        WHEN days_of_week.day_of_week = 3 THEN 'Tuesday'
        WHEN days_of_week.day_of_week = 4 THEN 'Wednesday'
        WHEN days_of_week.day_of_week = 5 THEN 'Thursday'
        WHEN days_of_week.day_of_week = 6 THEN 'Friday'
        WHEN days_of_week.day_of_week = 7 THEN 'Saturday'
      END AS day_of_week,
    count(d.id) as total
    FROM (
      SELECT 1 as day_of_week UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7
    ) as days_of_week
           left join detections d 
      ON days_of_week.day_of_week = DAYOFWEEK(DATE(d.datetime))
      AND DATE(d.datetime) between CAST('{startDate}' AS DATE) and  CAST('{endDate}' AS DATE)  

     
    
    GROUP BY days_of_week.day_of_week
    ORDER BY days_of_week.day_of_week;
    """
 
    df = pd.read_sql_query(sql=consulta, con=engine)
    
    return {"totalData":df["total"].to_list(),"tableBody": df.values,"title":"Week"}
def get_total_negative(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where  prediction_result = 'false' and DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_positive(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where  prediction_result = 'true' and DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_today():
    engine = create_engine(connect_info)
    consulta = "SELECT count(id) as count FROM detections WHERE  DATE(datetime) = '"+str(time.strftime("%d-%m-%y"))+"'"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_negative_all():
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where prediction_result = 'true' "
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]

def get_total_gender(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"""SELECT g.id, g.name AS genero, COUNT(d.id) AS count
FROM gender g
LEFT JOIN patients p ON g.id = p.gender_id
LEFT JOIN detections d ON p.id = d.patient_id
 and DATE(d.datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)
GROUP BY g.id, g.name """    
    df = pd.read_sql_query(sql=consulta, con=engine)
    return {
       "totalData": df["count"].tolist(),
       "nameData": df["genero"].tolist(),
       "title":"Gender"
        }

def get_total_blood_type(startDate,endDate):
    engine = create_engine(connect_info)
    consulta = f"""SELECT b.id, b.type AS blood_type, COUNT(d.id) AS count
FROM blood_type b
LEFT JOIN patients p ON b.id = p.gender_id
LEFT JOIN detections d ON p.id = d.patient_id
 and DATE(d.datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)
GROUP BY b.id, b.type"""
    df = pd.read_sql_query(sql=consulta, con=engine)
    return {
       "totalData": df["count"].tolist(),
       "nameData": df["blood_type"].tolist(),
       "title":"BloodType"
        }
def get_info_patients(startDate,endDate):
    engine = create_engine(connect_info)
    consulta =  f"""
    SELECT 
    p.first_name  as name,
    IF(COALESCE(count(d.id), 0) > (select count(d.id) from detections where DATE(d.datetime) BETWEEN CAST('{startDate}' AS DATE) AND CAST('{endDate}' AS DATE) ), 'danger', 'primary') as resultado,
     COALESCE(count(d.id), 0) as total,
     ifnull((IFNULL( COALESCE(count(d.id), 0),0) * 100 ) /(select count(d.id) from detections where DATE(d.datetime) BETWEEN CAST('{startDate}-01' AS DATE) AND CAST('{endDate}' AS DATE)),0) as porcentaje,
 (select ifnull(count(d.id),0) from detections where DATE(d.datetime) BETWEEN CAST('{startDate}' AS DATE) AND CAST('{endDate}' AS DATE)) as alcance
FROM 
    (
        SELECT id,first_name
        FROM patients) p
        left join detections d on d.patient_id = p.id where DATE(d.datetime) BETWEEN CAST('{startDate}' AS DATE) AND CAST('{endDate}' AS DATE) 
       

   
GROUP BY 
    p.first_name;

        """

    df = pd.read_sql_query(sql=consulta, con=engine)
    
    alcance =0

    if len(df.values)>0:
        alcance = df["alcance"][0]
    
    
    return {"nombreData":df["name"].tolist(),"totalData":df["total"].tolist(),"resultadoData":df["resultado"].tolist(),"tableData":["Nombre", "Total", "Resultado"],"typeData": ["STR", "STR", "STR"],"porcentajeData":df["porcentaje"].tolist(),"title":"Patients performance","alcanceData":alcance,"currencyData":""}


def analytics(startDate,endDate):

    return {
        "chartMonth":  get_sql_mes(startDate,endDate),
        "chartWeek":  get_sql_semana(startDate,endDate),
        "cardPositive":get_total_negative(startDate,endDate),
        "cardNegative":get_total_positive(startDate,endDate),
        "cardTotal":get_total(startDate,endDate),
        "cardGender":get_total_gender(startDate,endDate),
        "cardBloodType":get_total_blood_type(startDate,endDate),
        "cardDays":get_sql_days(startDate,endDate),
       
    }
 