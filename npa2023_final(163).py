#######################################################################################
# Yourname: Teerapop Petchnil
# Your student ID: 64070163
# Your GitHub Repo: 

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, and (restconf_final or netconf_final).

import netconf_final
import json
import requests
import time

#######################################################################################
# 2. Assign the Webex hard-coded access token to the variable accessToken.
# ของ user
accessToken = "Bearer Zjc2YmI2YjMtNTlhNC00ZTM2LTk1ZDItOGM5YWMzY2U2MTEyNzAxNjQ5YWMtZGRj_P0A1_7f327c1e-1188-4daa-9a20-2c6420320fe5"

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    "<!!!REPLACEME with roomID of the NPA2023 Webex Teams room!!!>"
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization":  }
# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "<!!!REPLACEME with URL of Webex Teams Messages API!!!>",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
    print("Received message: " + message)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message.find("/64070163") == 0:

        # extract the command
        command = message.split()[1]
        print(command)

# 5. Complete the logic for each command

        if command == "create":
            responseMessage = netconf_final.create()     
        elif command == "delete":
            responseMessage = netconf_final.delete()
        elif command == "enable":
            responseMessage = netconf_final.enable()
        elif command == "disable":
            responseMessage = netconf_final.disable()
        elif command == "status":
            responseMessage = netconf_final.status()
        else:
            responseMessage = "Error: No command or unknown command"
        
# 6. Complete the code to post the message to the Webex Teams room.
        
        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        postHTTPHeaders = HTTPHeaders = {"Authorization": <!!!REPLACEME!!!>, "Content-Type": <!!!REPLACEME!!!>}

        # The Webex Teams POST JSON data
        # - "roomId" is is ID of the selected room
        # - "text": is the responseMessage assembled above
        postData = {"roomId": <!!!REPLACEME!!!>, "text": <!!!REPLACEME!!!>}

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "<!!!REPLACEME with URL of Webex Teams Messages API!!!>",
            data=json.dumps(<!!!REPLACEME!!!>a),
            headers=<!!!REPLACEME!!!>,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
