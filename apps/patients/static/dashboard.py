import pandas as pd
import pymysql
from sqlalchemy import create_engine
import time
connect_info = 'mysql+pymysql://root@localhost:3306/diabetic_macular_edema'
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_sql_mes(startDate,endDate,id):       

    consulta = f"""
SELECT 
months.name as name,
months.id as num,
  COALESCE(count(d.id), 0) as total
FROM months
left join detections d  ON MONTH(d.datetime) = months.id 
  AND datetime between CAST('{startDate}' AS DATE) AND  CAST('{endDate}' AS DATE)  and d.patient_id = {id}
GROUP BY months.id 
ORDER BY months.id;
    """
    print(consulta)
    cnx = pymysql.connect(user='root', password='',
                              host='localhost', database='diabetic_macular_edema')
    cursor = cnx.cursor()
    ventas_por_dia = [0] * 12
    cursor.execute(consulta)
    for mes,num, total_ventas in cursor:
        ventas_por_dia[int(num)-1]= str(total_ventas)

    combinada = [list(pair) for pair in zip(months, ventas_por_dia)]
    return {"totalData": ventas_por_dia,"tableBody": combinada,"title":"Month"}

def get_sql_semana(startDate,endDate,id):
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

     and d.patient_id = {id} 
    
    GROUP BY days_of_week.day_of_week
    ORDER BY days_of_week.day_of_week;
    """
 
    df = pd.read_sql_query(sql=consulta, con=engine)
    
    return {"totalData":df["total"].to_list(),"tableBody": df.values,"title":"Week"}
def get_total_negative(startDate,endDate, id):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where patient_id = '{id}'  and prediction_result = 'false' and DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_positive(startDate,endDate, id):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where patient_id = '{id}' and prediction_result = 'true' and DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total(startDate,endDate, id):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where patient_id = '{id}' and DATE(datetime) between cast('{startDate}' as DATE) and cast('{endDate}' as DATE)"
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_today(id):
    engine = create_engine(connect_info)
    consulta = "SELECT count(id) as count FROM detections WHERE patient_id = '"+str(id)+"' AND DATE(datetime) = '"+str(time.strftime("%d-%m-%y"))+"'"
    print(consulta)
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def get_total_negative_all(id):
    engine = create_engine(connect_info)
    consulta = f"select count(id) as count from detections where patient_id = '{id}'  and prediction_result = 'true' "
    df = pd.read_sql_query(sql=consulta, con=engine)
    return df["count"][0]
def dashboard(id,startDate,endDate):

    return {
        "chartMonth":  get_sql_mes(startDate,endDate, id),
        "chartWeek":  get_sql_semana(startDate,endDate, id),
        "cardPositive":get_total_negative(startDate,endDate,id),
        "cardNegative":get_total_positive(startDate,endDate,id),
        "cardTotal":get_total(startDate,endDate,id),
        "cardNegativeAll":get_total_negative_all(id),
        "cardToday":get_total_today(id),
    }
