#!/usr/bin/python3

'''
splunk-onboarding.py

Source: https://pynative.com/python-mysql-tutorial/

'''



from pathlib import Path # For mkdir
import mysql.connector
from mysql.connector import Error
import os
import sys  # For file operations



def CreateDirectoryNameForDeploymentApp(number):
    '''
    Create a deployment app directory name in format 'da-999999'

    number: number to use in the deployment app directory, number = 1 returns da-000001
    '''
    t = str(number)
    t = 'da-' + t.zfill(6) 
    return t



def UpdateCda(recordId):
    '''
    Update the table create_deployment_app_cda where cda_id = recordId

    recordId: Number of the record to update

    Example SQL: UPDATE `SPLUNK_ONBOARDING`.`create_deployment_app_cda` SET `cda_is_created` = '1' WHERE (`cda_id` = '4');
    '''
    query = 'UPDATE create_deployment_app_cda SET cda_is_created=1 WHERE cda_id=' + str(recordId) 
    print(query)
    cursor.execute(query)
    connection.commit()


def CreateDirectoryNameForTechnicalAddon(configName):
    '''
    Create a name for a directory that will be the TA name

    configName: Name of the config that will be part of the TA name.
    '''
    return 'ta-' + configName.lower()



def CreateDirectoryTree(directoryTree):
    '''
    Create the directoryTree 
    '''
    try:
        Path(directoryTree).mkdir(parents=True, exist_ok=True)
    except Error as e:
        print('CreateDirectoryTree() ERROR ' + e)
    else:
        print('CreateDirectoryTree() Succesful created directory tree ' + directoryTree)



def CreateOneTechnicalAddon(environmentCode, directoryTa, configItemCode):
    '''
    Create one technical addon on the 

    environmentCode: Code of the environment of 3 letters.
    directoryTa: Where will the TA be written
    configItemCode:
    '''
    print('CreateOneTechnicalAddon()')
    print(environmentCode)
    print(directoryTa)
    print(configItemCode)
    print(CreateDirectoryNameForTechnicalAddon(configItemCode))

    # Build the complete directory name
    CreateDirectoryTree(directoryTa + '/' + CreateDirectoryNameForTechnicalAddon(configItemCode) +'/local/')
    


def ProcessTechnicalAddon(environment):
    '''
    Select the records from the view that need to be created

    environment: Code of 3 letters to select the environment
    '''
    query = "SELECT * FROM view_create_technical_addon WHERE cta_env_code='" + environment + "' AND cta_is_created=0"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    
    print('ProcessTechnicalAddon(): Select records to create the technical add-ons')
    for row in records:
        # 0: cta_id
        # 1: cta_env_code
        # 2: env_directory_ma
        # 3: cta_cni_code
        # 4: cta_is_created
        CreateOneTechnicalAddon(row[1], row[2], row[3])
        print('=====')


def CreateOneDeploymentApp(recordId, logFileId, directoryCreate, pathToMonitor, sourceType, index):
    '''
    Create one new deployment app in the required directory

    recordId: Unique record ID. Every record has a unqiue ID
    logFileId: Unique log file ID. Every log file has a unique ID
    directoryCreate: Starting directory where to create the new inputs.conf
    pathToMonitor: Which log file to monitor in the inputs.conf
    sourceType: Use this source type in the inputs stanza
    index: Name of the index to write to
    '''
    print('CreateOneDeploymentApp()')

    directoryFull = directoryCreate + '/' + CreateDirectoryNameForDeploymentApp(logFileId) +'/local/'
    print(directoryFull)
    Path(directoryFull).mkdir(parents=True, exist_ok=True)

    #[monitor:///var/log]
    #whitelist = (\.log|log$|messages|secure|auth|mesg$|cron$|acpid$|\.out)
    #blacklist = (lastlog|anaconda\.syslog)
    #disabled = false
    #index = idxe_oslinux

    try:
        f = open(directoryFull + '/inputs.conf', 'w')
    except IOError as e:
        print('Error opening file:', e)
    else:
        f.write('[monitor://' + pathToMonitor + ']\n')
        f.write('disabled = false\n')
        f.write('sourcetype = ' + sourceType + '\n')
        f.write('index = ' + index + '\n')

        f.close()

        resultCode = os.system('/opt/splunk/bin/splunk status') # splunk restart to activate for real
        if resultCode == 0:
            print('Succesfully added new DA: {}'.format(logFileId))
            print('Update record to succesfully done!')
            UpdateCda(recordId)
        else:
            print('Error while adding a new DA {}'.format(logFileId))
    
    print('===')    



def ProcessDeploymentApps(environment):
    '''
    Select only the records from the view that needs to be created for the environment

    environment: Code of the Splunk environment thats needs to be created.
    '''
    query = "SELECT * FROM view_create_deployment_app WHERE cda_env_code='" + environment + "'"
    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    print('CreateDeploymentApp(): record found to process')
    for row in records:
        print(row[0], '\t', row[1], '\t', row[2], '\t', row[3], '\t', row[4], '\t', row[5], '\t', row[6], '\t', row[7],  '\t', row[8])
        CreateOneDeploymentApp(row[0], row[3], row[5], row[6], row[7], row[8]) # 0:recordId, 3:logFileId, 5:directoryCreate, 6:pathToMonitor, 7:sourceType, 8:index



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
            global cursor
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            ProcessTechnicalAddon('TST')

            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
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

    #ProcessDeploymentApps('VOY')
   
    #print(CreateDirectoryNameForDeploymentApp(43))


   



if __name__ == "__main__":
    main()
