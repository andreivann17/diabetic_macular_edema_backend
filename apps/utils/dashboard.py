import pandas as pd
import pymysql
from sqlalchemy import create_engine
from ..ajustes import ajustes
import calendar
connect_info = 'mysql+pymysql://root@localhost:3306/recursos_humanos'
meses = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre']
semana = ['lunes','martes','miercoles','jueves','viernes','sabado','domingo']

def get_fecha_last(fecha):
    fechalast = ""
    if int(fecha[5:7]) ==1 :
        fechalast = str((int(fecha[0:4]) + 1)) + "-12"
    else:
        fechalast = fecha[0:4] + "-"+str(int(fecha[5:7])-1)
    return fechalast
def get_info_meses():
    fechas = pd.date_range(start='2023-01', end=pd.Timestamp.now().strftime('%Y-%m-%d'), freq='MS')

    meses_espanol = {
    'January': 'Enero',
    'February': 'Febrero',
    'March': 'Marzo',
    'April': 'Abril',
    'May': 'Mayo',
    'June': 'Junio',
    'July': 'Julio',
    'August': 'Agosto',
    'September': 'Septiembre',
    'October': 'Octubre',
    'November': 'Noviembre',
    'December': 'Diciembre'
}

    # Formatea las fechas en el formato deseado con el nombre completo del mes en español
    meses_anos = fechas.strftime('%Y-%B').tolist()
    meses_anos_espanol = [meses_anos[i].replace(meses_anos[i].split('-')[1], meses_espanol[meses_anos[i].split('-')[1]]) for i in range(len(meses_anos))]
    
    return {"meses":meses_anos_espanol,"fechas":fechas.strftime('%Y-%m').tolist()}
def set_info_card(data,datalast,signo):
    datasent = []
    total = 0
    totallast = 0
    for box,boxlast,boxsigno in zip(data,datalast,signo):
        value = "ERROR"
        total += float(box)
        totallast += float(boxlast)
        if float(boxlast) > 0:
            value = ((float(box) - float(boxlast)) / float(boxlast)) * 100
        datasent.append(["",str(box),boxsigno,"","-",str(value),boxlast])
    pvalue = "ERROR"
    if float(totallast) > 0:
            pvalue = ((float(total) - float(totallast)) / float(totallast)) * 100
    return [datasent,["",str(total),"$","","",pvalue,totallast]]
def get_dias(fecha):
    mes = int(fecha[5:7])
    anio = int(fecha[0:4])
    num_dias =calendar.monthrange(anio, mes)[1]
    # Ejecución de la consulta SQL para obtener los días y la suma de ventas
    dias = range(1, num_dias+1)
    return list(dias)

def get_sql_dias(fecha,clave,query):
    
    cnx = pymysql.connect(user='root', password='',
                              host='localhost', database='recursos_humanos')
    cursor = cnx.cursor()
    dias = get_dias(fecha)
    ventas_por_dia = [0 for _ in dias]
    
    if clave != "":
        cursor.execute(query, (int(fecha[5:7]), int(fecha[0:4]),clave))
    else:
        cursor.execute(query, (int(fecha[5:7]), int(fecha[0:4])))
    for dia, total_ventas in cursor:
        ventas_por_dia[int(dia)-1]= str(total_ventas)
     
    cursor.close()
    cnx.close()
    combinada = [list(pair) for pair in zip(dias, ventas_por_dia)]
    return { "totalData":ventas_por_dia,"tableHeader":dias,"tableBody":combinada,"title":"Dia"}
def get_sql_semana(dataconsulta):
    engine = create_engine(connect_info)
    consulta = """
    SELECT 
      CASE 
        WHEN dias_semana.dia_semana = 1 THEN 'Lunes' 
        WHEN dias_semana.dia_semana = 2 THEN 'Martes' 
        WHEN dias_semana.dia_semana = 3 THEN 'Miércoles'
        WHEN dias_semana.dia_semana = 4 THEN 'Jueves'
        WHEN dias_semana.dia_semana = 5 THEN 'Viernes'
        WHEN dias_semana.dia_semana = 6 THEN 'Sábado'
        WHEN dias_semana.dia_semana = 7 THEN 'Domingo'
      END AS dia_semana,
      """+dataconsulta["total"]+""" as total
    FROM (
      SELECT 1 as dia_semana UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7
    ) as dias_semana
    LEFT JOIN """+dataconsulta["tabla"]+"""  
      ON dias_semana.dia_semana = DAYOFWEEK("""+dataconsulta["prefijoFecha"]+""")
      AND """+dataconsulta["prefijoFecha"]+""" between CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) and  CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE)  
      """+dataconsulta["inner"]+"""
      """+dataconsulta["where"]+"""
    
    GROUP BY dias_semana.dia_semana
    ORDER BY dias_semana.dia_semana
    """
    
    df = pd.read_sql_query(sql=consulta, con=engine)
    
    return {"totalData":df["total"].to_list(),"tableHeader":["Lunes","Martes","Miercoles","Jueves","Viernes","Sabado","Domingo"],"tableBody": df.values,"title":"Semana"}

def get_sql_mes(dataconsulta):       

    consulta = """
 

SELECT 
meses.mes_nombre as nombre,
meses.mes_id as num,
  COALESCE("""+dataconsulta["total"]+""", 0) as total
FROM meses
 """+dataconsulta["inner"]+"""
  AND """+dataconsulta["prefijoFecha"]+""" between CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND  CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE)  """+dataconsulta["where"]+"""

GROUP BY meses.mes_id
ORDER BY meses.mes_id;


    """
   
    cnx = pymysql.connect(user='root', password='',
                              host='localhost', database='recursos_humanos')
    cursor = cnx.cursor()
    ventas_por_dia = [0] * 12
    cursor.execute(consulta)
    for mes,num, total_ventas in cursor:
        ventas_por_dia[int(num)-1]= str(total_ventas)

    combinada = [list(pair) for pair in zip(meses, ventas_por_dia)]
    return {"totalData": ventas_por_dia,"tableHeader":meses,"tableBody": combinada,"Title":"Mes"}
def get_sql_hora(dataconsulta):
    engine = create_engine(connect_info)
    consulta = """
 SELECT horas.rango_horas, 
  """+dataconsulta["total"]+""" as total
FROM (
  SELECT '0-1' AS rango_horas
  UNION ALL SELECT '1-2'
  UNION ALL SELECT '2-3'
  UNION ALL SELECT '3-4'
  UNION ALL SELECT '4-5'
  UNION ALL SELECT '5-6'
  UNION ALL SELECT '6-7'
  UNION ALL SELECT '7-8'
  UNION ALL SELECT '8-9'
  UNION ALL SELECT '9-10'
  UNION ALL SELECT '10-11'
  UNION ALL SELECT '11-12'
  UNION ALL SELECT '12-13'
  UNION ALL SELECT '13-14'
  UNION ALL SELECT '14-15'
  UNION ALL SELECT '15-16'
  UNION ALL SELECT '16-17'
  UNION ALL SELECT '17-18'
  UNION ALL SELECT '18-19'
  UNION ALL SELECT '19-20'
  UNION ALL SELECT '20-21'
  UNION ALL SELECT '21-22'
  UNION ALL SELECT '22-23'
    UNION ALL SELECT '23-24'
) AS horas

LEFT JOIN """+dataconsulta["tabla"]+"""  """+dataconsulta["inner"]+""" ON horas.rango_horas = 
  CONCAT(HOUR("""+dataconsulta["prefijoHora"]+"""), '-', LPAD(HOUR("""+dataconsulta['prefijoHora']+""")+1, if("""+dataconsulta["prefijoHora"]+""" >= 10,2,1), '0'))
  AND """+dataconsulta["prefijoFecha"]+""" BETWEEN CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE)
"""+dataconsulta['where']+"""

GROUP BY horas.rango_horas
ORDER BY CAST(SUBSTRING_INDEX(horas.rango_horas, '-', 1) AS UNSIGNED) ASC;
    """
   
    df = pd.read_sql_query(sql=consulta, con=engine)
    return {"totalData":df["total"].values,"tableHeader":df["rango_horas"].values,"tableBody":df.values[0:24],"title":"Hora"}

def get_info_comparacion(dataconsulta,title):
    engine = create_engine(connect_info)
    consulta =  """
    SELECT 
    """+dataconsulta["nombre"]+ """  as nombre,
    IF(COALESCE("""+dataconsulta["total"]+ """, 0) > (select """+dataconsulta["columna_total"]+ """ from """+str(dataconsulta["tabla_total"])+""" where """+dataconsulta["prefijoFecha"]+ """ BETWEEN CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE) ), 'danger', 'primary') as resultado,
     COALESCE("""+dataconsulta["total"]+ """, 0) as total,
     ifnull((IFNULL( COALESCE("""+str(dataconsulta["total"])+""", 0),0) * 100 ) /(select """+dataconsulta["columna_total"]+ """ from """+str(dataconsulta["tabla_total"])+""" where """+dataconsulta["prefijoFecha"]+ """ BETWEEN CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE)),0) as porcentaje,
 (select ifnull("""+dataconsulta["columna_total"]+ """,0) from """+str(dataconsulta["tabla_total"])+""" where """+dataconsulta["prefijoFecha"]+ """ BETWEEN CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE)) as alcance
FROM 
    (
        SELECT """+dataconsulta["campo"]+ """
        FROM """+dataconsulta["tabla"]+ """
        """+dataconsulta["inner"]+ """ where """+dataconsulta["prefijoFecha"]+ """ BETWEEN CAST('"""+dataconsulta["fecha"]+"""-01' AS DATE) AND CAST('"""+dataconsulta["fecha"]+"""-31' AS DATE) 
        """+dataconsulta["where"]+ """ 

   
GROUP BY 
    """+dataconsulta["group_by"]+ """;

        """

    df = pd.read_sql_query(sql=consulta, con=engine)
    
    alcance =0

    if len(df.values)>0:
        alcance = df["alcance"][0]
    
    
    return {"nombreData":df["nombre"].tolist(),"totalData":df["total"].tolist(),"resultadoData":df["resultado"].tolist(),"tableData":dataconsulta["data_table"],"porcentajeData":df["porcentaje"].tolist(),"title":title,"alcanceData":alcance,"currencyData":dataconsulta["currency"]}

