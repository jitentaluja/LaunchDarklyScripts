from utils.apiHandler import checkRateLimit as api_call
from utils.newApiHandler import checkRateLimit as new_api_call
import json
import os
import datetime


'''
Set your LaunchDarkly instance information here
'''
API_KEY = "api-791e23d8-7554-49bb-bccb-cda920330ffa"
project_list = []



'''
Define API call information
'''
project_list_url_iteration1 = f'/projects?limit=20'
project_list_url_iteration2 = f'/projects?limit=20&offset=20'
project_list_url_iteration3 = f'/projects?limit=20&offset=40'


def get_flag_list():
    flag_list = []
    get_projects_and_populateFlags(flag_list,project_list_url_iteration1)
    get_projects_and_populateFlags(flag_list,project_list_url_iteration2)
    get_projects_and_populateFlags(flag_list,project_list_url_iteration3)
    	
    return flag_list


def get_projects_and_populateFlags(flag_list,url):

    response = api_call("GET", url, API_KEY, {}).json()
    response_list = response['items']

    number_of_flags = len(response_list)
    for i in range(number_of_flags):
    	project_name = response['items'][i]['key']
    	# flag_list.append(project_name)   
    	print("Trying for " + project_name)
    	populate_flag_list(flag_list,project_name)

    return flag_list


def populate_flag_list(flag_list,project_name):
    url = f'/flags/{project_name}?archived=true'
    # flag_list.append("****** " + project_name + " ******")
    response = api_call("GET", url, API_KEY, {}).json()
    response_list = response['items']
    number_of_flags = len(response_list)

    if number_of_flags == 0:
    	flag_list.append(project_name + ": NA")

    for i in range(number_of_flags):
        flag_name = response['items'][i]['key']
        archived = response['items'][i]['archived']
        time_in_millis = response['items'][i]['archivedDate']
        converteddatetime = datetime.datetime.fromtimestamp(time_in_millis / 1000.0)
        archive_date = converteddatetime.strftime('%Y-%m-%d')

        createdate_in_millis = response['items'][i]['creationDate']
        converteddatetime = datetime.datetime.fromtimestamp(createdate_in_millis / 1000.0)
        creation_date = converteddatetime.strftime('%Y-%m-%d')
        
        z = response['items'][i]
        maintainer = ""
        if '_maintainer' in z:
        	maintainer = response['items'][i]['_maintainer']['email']
        else:
        	maintainer = 'none'

        clientMobileKey = response['items'][i]['clientSideAvailability']['usingMobileKey']
        clientEnvId = response['items'][i]['clientSideAvailability']['usingEnvironmentId']

        temporary = response['items'][i]['temporary']
        tags = response['items'][i]['tags']

        flag_list.append(project_name + ": " + str(flag_name) + ": " + str(tags) + ": " + str(maintainer) + ": " + ": " + ": " + str(clientMobileKey) + ": " + str(clientEnvId) + ": " + str(temporary) + ": " + str(creation_date) + ": " + str(archive_date) + ": " + str(archived) + ": " + ": "+ ": " + ": "+ ": " + ": " + ": ")

    return flag_list
    

# Main function
def get_flag_archived():

    # Get the list of flags, print it just because
    
    flag_list = get_flag_list()
    # print(flag_list)

    # Create a text file for output
    filename = "output-flagarchived-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file = open(filename, 'w')
    # file = open('output-flagarchived-200223.txt', 'w')

    flagDetails = ("LD Project Name" + ': ' + "Flag name" + ": " + "Tags" + ": " + "Maintainer email" + ": " + "Launched?" + ": " + "Client side?" + ": " + "Client side - using mobile key?" + ": " + "Client side - using environment id?" + ": " + "Temporary?" + ": " + "Creation Date" + ": " + "Archive Date" + ": " + "Flag Archived" + ": " + ": " + ": "+ ": " + ": "+ ": " + ": ")
    file.write(f'{flagDetails} \n')

    # Iterate through the list of flags
    for i in flag_list:
        # Write the flag key
        file.write(f'{i} \n')
    
    file.close()

if __name__ == "__main__":
    get_flag_archived()