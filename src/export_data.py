
from mysql.connector import (connection)
from mysql.connector import Error
import pandas as pd
import os

database_host = os.environ['MYSQL_HOST']
database_name = os.environ['MYSQL_DATABASE']
database_user = os.environ['MYSQL_USER']
database_password = os.environ['MYSQL_PASSWORD']

try:
    cnx = connection.MySQLConnection(user=database_user, password=database_password, 
        host=database_host, database=database_name)
    print('Database connection sucessfully.')
except Error as e:
    print('Error on database connection: ', e)

# Service / Category

sql_query = pd.read_sql_query("SELECT id, name FROM service", cnx)

df = pd.DataFrame(sql_query)

df.to_json (r'/data/preprocess/service_categories.json', orient='records', force_ascii=False) # place 'r' before the path name to avoid any errors in the path

# Tickets Labeled

sql_query = pd.read_sql_query('''SELECT
    a.ticket_id as ticket_id,
	MIN(a.id) as article_id,
	a.a_subject as article_subject,
	a.a_body as article_body,
	t.title as tickect_title,
	t.tn as ticket_number,
	t.service_id as service_id,
	s.name as service_name
FROM
	article a
	JOIN ticket t ON a.ticket_id = t.id
	LEFT JOIN service s ON t.service_id = s.id
GROUP BY
	a.ticket_id''', cnx)

df = pd.DataFrame(sql_query)

df.to_json (r'/data/preprocess/tickets_labeled.json', orient='records', force_ascii=False) # place 'r' before the path name to avoid any errors in the path

