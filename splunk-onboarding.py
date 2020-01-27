#!/usr/bin/python3

'''
splunk-onboarding.py

Source: https://pynative.com/python-mysql-tutorial/

'''



from pathlib import Path
import mysql.connector
from mysql.connector import Error



def CreateDirectoryNameForDeploymentApp(number):
    '''
    Create a deployment app directory name in format 'da-999999'

    number: number to use in the deployment app directory, number = 1 returns da-000001
    '''
    t = str(number)
    t = 'da-' + t.zfill(6) 
    return t



def CreateOneDeploymentApp(logFileId, directoryCreate, pathToMonitor, sourceType):
    '''
    Create a new deployment app in the required directory

    logFileId: Unique log file ID. Every log file has a unqiue ID
    directoryCreate: Starting directory where to create the new inputs.conf
    pathToMonitor: Which log file to monitor in the inputs.conf
    sourceType: Use this source type in the inputs stanza
    '''
    print('CreateOneDeploymentApp()')

    directoryFull = directoryCreate + '/' + CreateDirectoryNameForDeploymentApp(logFileId) +'/local/'
    print(directoryFull)
    Path(directoryFull).mkdir(parents=True, exist_ok=True)



def ProcessDeploymentApps(environment):
    '''
    Select only the records from the view that needs to be created for the environment

    environment: Code of the Splunk environment thats needs to be created.
    '''
    query = "SELECT * FROM view_create_deployment_app WHERE cda_env_code='" + environment + "' AND cda_is_created=0"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print('CreateDeploymentApp(): record found to process')
    for row in records:
        print(row[0], '\t', row[1], '\t', row[2], '\t', row[3], '\t', row[4], '\t', row[5], '\t', row[6], '\t', row[7],  '\t', row[8])
        CreateOneDeploymentApp(row[3], row[5], row[6], row[7])

    



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
    
    ##sql_select_Query = "select * from environment_env"
    ##cursor = connection.cursor()
    ##cursor.execute(sql_select_Query)
    #3records = cursor.fetchall()
    ##print("Total number of rows in environment_env is: ", cursor.rowcount)

    ##print('Code==== Description==================== RCD==================== RLU================')
    ##for row in records:
    ##    print(row[0], '\t', row[1], '\t',  row[2], '\t', row[3])



    ProcessDeploymentApps('VOY')

    print(CreateDirectoryNameForDeploymentApp(43))


    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("MySQL connection is closed")



if __name__ == "__main__":
    main()
