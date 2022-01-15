import urllib.parse, urllib.request, json, ssl

# Authentication and API Requests

# LEARNING LAB 2  Cisco Kinetic for Cities
# The Initial login steps are the same as Learning Lab 1.
# You can skip ahead to 'LEARNING LAB 2 CODE BEGINS HERE'

#Ignore invalid Certificates
ssl._create_default_https_context = ssl._create_unverified_context

#   1) Logging In
# The CKC URL needed for initial login
loginUrl = 'https://ckcsandbox.cisco.com/corev4/token'

#Define the required three Headers for the initial Login Post
headers = {
    'Cache-Control': "no-cache",
    'Content-Type': "application/x-www-form-urlencoded",
    'Postman-Token': "2915798c-f468-407c-a2dd-8897e441102b"
    }

# This dictionary contains the post body we will send to the /token API
# @Note: These are the sample sandbox client_id and client_secret values, so you will
#        need to replace them with yours as provided with your reservation
postData = {
    'client_secret':'nOZd6gw9_ORlJcZkgRifzMB6nzQa',
    'client_id':'Bpw8qejWXVQur3n6YAdqQAYtd94a',
    'grant_type':'password'
}

# get username and password from commandline
# For the first time user, the password will need to be set manually by logging into CKC dashboard, the link for which will be sent to the emailID
#   @Note: this will use the defaults from above if you just press 'enter'
username = input('Enter username (email address): ')

password = input('Enter password: ')


# Add username/password to post data
postData['username'] = username
postData['password'] = password


# urlencode the data
data = urllib.parse.urlencode(postData)

# use UTF-8 encoding for POST data and responses
encoding = 'UTF-8'

# POST needs binary data, so encode it
binary_data = data.encode(encoding)

print('\nLogging in:' + loginUrl + '\n')

# urlopen with data causes a post request
request = urllib.request.Request(loginUrl,  binary_data)
response = urllib.request.urlopen(request)

#   2) Parsing the login reponse to get the access_token needed for further API calls
# process the results and put into a JSON object/dictionary
results = response.read().decode(encoding)
responseDictionary = json.loads(results)
access_token = responseDictionary['access_token']
print('Response:', responseDictionary)


#   3) Using the token to make another API request
#Define the required Headers for a secondary GET request to obtain user details
#The url to obtain account details is GET to baseURL/cdp/v1/accounts/user/login

headers = {
    'authorization': "Bearer " + access_token,
    'Content-Type': "application/json"
    }

#The URL to request user details
requestUrl = 'https://ckcsandbox.cisco.com/t/devnet.com/cdp/v1/accounts/user/login'

print('\nGetting User Details: (' + requestUrl + ')\n')

# create the request
request = urllib.request.Request(requestUrl, headers = headers)

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDictionary = json.loads(results)

user_id = responseDictionary['id']

print('User Details:', results, '\n')

print('These items will be used in Lesson-2:')
print('Your Access Token:', access_token)
print('Your User ID:',user_id)

############################### LEARNING LAB 2 CODE BEGINS HERE ############################
#
# In this example, we will exercise the CKC API: {{Platform Instance URL}}/cdp/v1/locations/user/{userId}/info
# In the case of the Sandbox lab, this resolves to https://ckcsandbox.cisco.com/t/devnet.com/cdp/v1/locations/user/{userId}/info
# The access_token and user_id from Learning Lab 1 will be used to obtain the current Users Location Information

print('Learning Lab 2 Starts Here:')

#Define the required GET Headers needed by the CKC API
headers = {
    'authorization': "Bearer " + access_token,
    'Content-Type': "application/json"
    }

#The URL with queryParms to request user details
requestUrl = 'https://ckcsandbox.cisco.com/t/devnet.com/cdp/v1/locations/user/' + user_id + '/info'

print('\nGetting User Location Info: (' + requestUrl + ')\n')

# create the request
request = urllib.request.Request(requestUrl, headers = headers)

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDictionary = json.loads(results)

print('User Location Info:', results, '\n')

############################### LEARNING LAB 2  PART-2 ############################
#
# In this example, we will exercise the CKC API: {{Platform Instance URL}}/cdp/v1/capabilities/customer
# In the case of the Sandbox lab, this resolves to https://ckcsandbox.cisco.com/t/devnet.com/cdp/v1/capabilities/customer
# The access_token obtained as explained in Learning Lab 1 is used for authorization

#Define the required GET Headers needed by the CKC API
headers = {'authorization': "Bearer " + access_token }

#The URL with queryParms to request user details
requestUrl = 'https://ckcsandbox.cisco.com/t/devnet.com/cdp/v1/capabilities/customer'

print('\nGetting User capabilities: (' + requestUrl + ')\n')

# create the request
request = urllib.request.Request(requestUrl, headers = headers)

# perform the request
response = urllib.request.urlopen(request)

results = response.read().decode(encoding)
responseDictionary = json.loads(results)

print('User Capabilities:', results, '\n')
