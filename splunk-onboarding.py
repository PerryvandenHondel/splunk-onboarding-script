#!/usr/bin/python3

'''
splunk-onboarding.py

Source: https://pynative.com/python-mysql-tutorial/

version 1

'''



import mysql.connector
from mysql.connector import Error



def SelectDeploymentAppsToBeCreated(environment):
    '''
    Select only the records form the view that needs to be created for the environment

    environment: Code of the Splunk environment thats needs to be created.
    '''
    query = "SELECT * FROM view_create_new_da WHERE lgf_env_code='" + environment + "' AND lgf_created=0"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print('SelectDeploymentAppsToBeCreated(): record found to process')
    for row in records:
        print(row[0], '\t', row[1], '\t', row[2], '\t', row[3], '\t', row[4], '\t', row[5], '\t', row[6])



def main():
    try:
        global connection
        connection = mysql.connector.connect(host='localhost', \
            database='SPLUNK_ONBOARDING', \
            user='root', \
            password='Password1!')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print("Error while connecting to MySQL", e)
    
    sql_select_Query = "select * from environment_env"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    print("Total number of rows in environment_env is: ", cursor.rowcount)

    print('Code==== Description==================== RCD==================== RLU================')
    for row in records:
        print(row[0], '\t', row[1], '\t',  row[2], '\t', row[3])


    SelectDeploymentAppsToBeCreated('VOY')


    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



if __name__ == "__main__":
    main()
