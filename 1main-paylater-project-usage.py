from utils.apiHandler import checkRateLimit as api_call
from utils.newApiHandler import checkRateLimit as new_api_call
import json
import os
import datetime

'''
Set your LaunchDarkly instance information here
'''
API_KEY = "api-791e23d8-7554-49bb-bccb-cda920330ffa"
PROJECT_KEY = "paylater"
ENVIRONMENT_KEY_1 = "eu-production"
ENVIRONMENT_KEY_2 = "us-production"
ENVIRONMENT_KEY_3 = "production"



'''
Define API call information
'''
flag_list_url = f'/flags/{PROJECT_KEY}'

def total(arr):
    sum = 0

    for i in arr:
        sum = sum + i
 
    return(sum)


def get_flag_list():
    response = api_call("GET", flag_list_url, API_KEY, {}).json()
    response_list = response['items']
    number_of_flags = len(response_list)
    flag_list = []

    #file = open('output-flag-details.txt', 'w')

    for i in range(number_of_flags):
        #flag_list.append(response['items'][i]['key'])
        flag_name = response['items'][i]['key']
        z = response['items'][i]
        maintainer = ""
        a = response['items'][i]['creationDate']
        archived = response['items'][i]['archived']
        clientMobileKey = response['items'][i]['clientSideAvailability']['usingMobileKey']
        clientEnvId = response['items'][i]['clientSideAvailability']['usingEnvironmentId']

        if '_maintainer' in z:
        	maintainer = response['items'][i]['_maintainer']['email']
        else:
        	maintainer = 'none'
        
        converteddatetime = datetime.datetime.fromtimestamp(a / 1000.0)
        creation_date = converteddatetime.strftime('%Y-%m-%d')

        temporary = response['items'][i]['temporary']
        tags = response['items'][i]['tags']

        # Write the flag key
        flagDetails = (str(flag_name) + ': ' + str(tags) + ": " + str(maintainer) + ": " + ": " + ": " + str(clientMobileKey) + ": " + str(clientEnvId) + ": " + str(temporary) + ": " + str(creation_date) + ": " + ": " + str(archived))
        flag_list.append(flagDetails)
        # file.write(f'{flagDetails} \n')
    
    #file.close()
    return flag_list

# Main function
def get_flag_usage():

    # Get the list of flags, print it just because
    flag_list = get_flag_list()
    # print(flag_list)

    series_total_1 = 0
    series_total_2 = 0
    series_total_3 = 0

    count = 0

    # Create a text file for output
    # file = open('output-usage-200223.txt', 'w')
    filename = "output-usage-paylater-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file = open(filename, 'w')

    flagDetails = ("LD Project Name" + ': '+ "Flag name" + ': ' + "Tags" + ": " + "Maintainer email" + ": " + "Launched?" + ": " + "Client side?" + ": " + "Client side - using mobile key?" + ": " + "Client side - using environment id?" + ": " + "Temporary = TRUE Permanent = FALSE" + ": " + "Creation Date" + ": " + "Archive Date" + ": " + "Flag Archived" + ": " + "Prod-Env-1 (evaluations)" + ": " + "Prod-Env-1 (status)" + ": " + "Prod-Env-2 (evaluations)" + ": " + "Prod-Env-2 (status)" + ": " + "Prod-Env-3 (evaluations)" + ": " + "Prod-Env-3 (status)" + ": " + "Total Evaluations (millions)")
    file.write(f'{flagDetails} \n')

    # Iterate through the list of flags
    for i in flag_list:
        
        file.write(f'{PROJECT_KEY}: ')
        # Write the flag key
        file.write(f'{i}: ')
        x = i[:i.index(":")]
        # print(x)

        # Get a series of usage entries over a time period (default is for the past 30 days)
        flag_usage_url_1 = f'/usage/evaluations/{PROJECT_KEY}/{ENVIRONMENT_KEY_1}/{x}'
        flag_usage_url_2 = f'/usage/evaluations/{PROJECT_KEY}/{ENVIRONMENT_KEY_2}/{x}'
        flag_usage_url_3 = f'/usage/evaluations/{PROJECT_KEY}/{ENVIRONMENT_KEY_3}/{x}'

        flag_status_url_1 = f'/flag-statuses/{PROJECT_KEY}/{ENVIRONMENT_KEY_1}/{x}'
        flag_status_url_2 = f'/flag-statuses/{PROJECT_KEY}/{ENVIRONMENT_KEY_2}/{x}'
        flag_status_url_3 = f'/flag-statuses/{PROJECT_KEY}/{ENVIRONMENT_KEY_3}/{x}'

        count = count + 1
        print(	"Trying for flag " + str(count) + ": " + x)

        
        #Environment 1
        response = new_api_call("GET", flag_usage_url_1, API_KEY, {}).json()

        series_1 = response["series"]
        series_value_1 = []

        # Iterate through series entries, and add up the values
        for entry in series_1:
            for key, value in entry.items():
                if key != "time":
                    series_value_1.append(value)
            
        
        series_total_1 = total(series_value_1)
        # Write the total to the text file
        file.write(f'{series_total_1}: ')

        # Now check for STATUS
        response_status = new_api_call("GET", flag_status_url_1, API_KEY, {}).json()
        status_1 = response_status['name']

        # Write the status to the text file
        file.write(f'{status_1}: ')

        
        #Environment 2
        response = new_api_call("GET", flag_usage_url_2, API_KEY, {}).json()

        series_2 = response["series"]
        series_value_2 = []

        # Iterate through series entries, and add up the values
        for entry in series_2:
            for key, value in entry.items():
                if key != "time":
                    series_value_2.append(value)
            
        
        series_total_2 = total(series_value_2)
        # Write the total to the text file
        file.write(f'{series_total_2}: ')

        # Now check for STATUS
        response_status = new_api_call("GET", flag_status_url_2, API_KEY, {}).json()
        status_2 = response_status['name']

        # Write the status to the text file
        file.write(f'{status_2}: ')


        #Environment 3
        response = new_api_call("GET", flag_usage_url_3, API_KEY, {}).json()

        series_3 = response["series"]
        series_value_3 = []

        # Iterate through series entries, and add up the values
        for entry in series_3:
            for key, value in entry.items():
                if key != "time":
                    series_value_3.append(value)
            
        
        series_total_3 = total(series_value_3)
        # Write the total to the text file
        file.write(f'{series_total_3}: ')

        # Now check for STATUS
        response_status = new_api_call("GET", flag_status_url_3, API_KEY, {}).json()
        status_3 = response_status['name']

        # Write the status to the text file
        file.write(f'{status_3}: ')

        all_total = series_total_1 + series_total_2 + series_total_3
        file.write(f'{all_total} \n')
    
    file.close()

if __name__ == "__main__":
    get_flag_usage()