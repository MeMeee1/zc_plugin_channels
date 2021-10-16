import asyncio
from os import stat
import aiohttp
from django.conf import settings
from aiohttp import ClientSession
import json
from django.urls import reverse
from channel_plugin.utils.customrequest import find_match_in_db
import requests
from apps.syncApp.utils import BadServerResponse
from channel_plugin.utils.customrequest import change_collection_name
# class TaskHandler:
#  __BASE_URL = "https://channels.zuri.chat/api"

#     def __init__(self):
#         __BASE_URL = "https://channels.zuri.chat/api"
#         self.__execute_operations()
    
#     @staticmethod
#     def run(data):
        
#         TaskHandler.member_id = data["message"]["member_id"]
#         TaskHandler.organization_id = data["message"]["organization_id"]
#         TaskHandler.event = data["event"]

#         assert isinstance(data, dict), f"Improper data type"
#         TaskHandler.__process_data(data)


    
#     @staticmethod
#     def __process_data(data):

#         TaskHandler.member_id = data["message"]["member_id"]
#         TaskHandler.organization_id = data["message"]["organization_id"]
#         TaskHandler.event = data["event"]

#         TaskHandler.instance = TaskHandler.__create_new_instance()
    
#     @staticmethod
#     def __create_new_instance():

#         return TaskHandler()    

#     def __execute_operations(self):


#         pass
#     @staticmethod
#     def get_schema():
#         return {"event": "enter_organization"}

data = {"plugin_id": settings.PLUGIN_ID}
read = settings.READ_URL
write = settings.WRITE_URL
delete = settings.DELETE_URL


# @change_collection_name
# async def find_match_in_db(org_id, collection_name, param, value, return_data=False):
#     data = {
#         "plugin_id": settings.PLUGIN_ID,
#         "organization_id": org_id,
#         "collection_name": collection_name,
#         "filter": {
#             "$and": [
#                 {param: {"$eq": value}},
#             ]
#         },
#     }
    
#     async with aiohttp.ClientSession() as session:
#         response = await session.post(read, data=json.dumps(data))
        
#         if response.status >= 200 or response.status < 300:
#             response_data = json.loads(await response.read()) or {}
#             assert isinstance(response_data, dict), "Invalid response returned"

#             try:
#                 if return_data:
#                     return response_data["data"]

#                 if response_data["data"] is not None:
#                     print("We made a match")
#                     return True

#             except:  # noqa
#                 print("No match")
#                 return None


# class JoinTaskHandler:
#     __BASE_URL = "https://channels.zuri.chat/api"

#     def __init__(self, data):
#         self.process_data(data)
#         self.__execute_operations()
    
#     @staticmethod
#     async def run(data):
#         assert isinstance(data, dict), f"Improper data type"
#         assert isinstance(data.get("message"), dict), "message must be of type dict"

#         await JoinTaskHandler.__create_new_instance(data)
#         return True    
    
#     @staticmethod
#     def __create_new_instance(data):
#         return JoinTaskHandler(data=data)    
    
#     @staticmethod
#     def get_schema():
#         return {"event": "enter_organization"}

#     async def __process_data(self, data):
#         self.member_id = data["message"]["member_id"]
#         self.organization_id = data["message"]["organization_id"]
#         self.event = data["event"]
    
#     async def __execute_operations(self):
#         print("Executing process")
#         default_channels = await self.__get_default_channels()
#         print(default_channels)
#         await self.__add_member_to_channel(self.member_id, self.organization_id, default_channels)
        
    
#     async def __get_default_channels(self):
        
#         data = await find_match_in_db(self.organization_id, "channel", "default", True, return_data=True)
#         assert  isinstance(data, list), "find_match_in_db returned an invalid type"
        
#         default_channel = [i["_id"] for i in data]
#         print(default_channel or "No default channels")
#         return default_channel or []

#     async def __add_member_to_channel(self, member_id, org_id, channels):
#         loop = asyncio.get_event_loop()        
#         task = []
#         for channel in channels:
#             async def add_member():
#                 try:
#                     endpoint_url = f"/v1/{org_id}/channels/{channel}/members/"
#                     data = {"_id": member_id,
#                             "role_id": "member",
#                             "is_admin": False,
#                             "notifications": {
#                             "web": "nothing",
#                             "mobile": "mentions",
#                             "same_for_mobile": True,
#                             "mute": False
#                             }
#                         }
                    
#                     url = (self.BASE_URL + endpoint_url)
#                     headers = {
#                         "Content-Type": "application/json"
#                     }
                    
#                     session = ClientSession()
#                     res = await session.post(url, data=json.dumps(data), headers=headers)
#                     print(res.status, "WHAT ")
#                 except:
#                     pass
#             task.append(add_member())
        
#         await asyncio.gather(*task)

class JoinTaskHandler:
    __BASE_URL = "https://channels.zuri.chat/api"

    def __init__(self, data):
        self.process_data(data)
        self.__execute_operations()
    
    @staticmethod
    def run(data):
        assert isinstance(data, dict), f"Improper data type"
        assert isinstance(data.get("message"), dict), "message must be of type dict"
        JoinTaskHandler.__create_new_instance(data)
        return True    
    
    @staticmethod
    def __create_new_instance(data):
        return JoinTaskHandler(data=data)    
    
    @staticmethod
    def get_schema():
        return {"event": "enter_organization"}

    def process_data(self, data):
        self.member_id = data["message"]["member_id"]
        self.organization_id = data["message"]["organization_id"]
        self.event = data["event"]
    
    def __execute_operations(self):
        print("Executing process")
        default_channels = self.__get_default_channels()
        print(default_channels)
        self.__add_member_to_channel(self.member_id, self.organization_id, default_channels)
        
    
    def __get_default_channels(self):
        
        data = find_match_in_db(self.organization_id, "channel", "default", True, return_data=True)
        data = data or [] # Screen for empty data
        print(data)
        assert  isinstance(data, list), "find_match_in_db returned an invalid type"
        
        default_channel = [i["_id"] for i in data]
        print(default_channel or "No default channels")
        return default_channel or []

    def __add_member_to_channel(self, member_id, org_id, channels):
        for channel in channels:
            def add_member():
                try:
                    endpoint_url = f"/v1/{org_id}/channels/{channel}/members/"
                    data = {"_id": member_id,
                            "role_id": "member",
                            "is_admin": False,
                            "notifications": {
                            "web": "nothing",
                            "mobile": "mentions",
                            "same_for_mobile": True,
                            "mute": False
                            }
                        }
                    
                    url = (self.BASE_URL + endpoint_url)
                    headers = {
                        "Content-Type": "application/json"
                    }
                    
                    res = requests.post(url, data=json.dumps(data), headers=headers)
                    print(res.status_code, "WHAT ")
                except:
                    pass

class RemoveTaskHandler:
    __BASE_URL = "https://channels.zuri.chat/api"
    
    def __init__(self, data):
        self.process_data(data)
        self.__execute_operations()
        
    @staticmethod
    def run(data):
        print(f"\nRUNNING Remove Task Handler with \n{data}")
        assert isinstance(data, dict), f"Improper data type"
        assert isinstance(data.get("message"), dict), "message must be of type dict"

        RemoveTaskHandler.__create_new_instance(data)

    @staticmethod
    def __create_new_instance(data):
        
        return RemoveTaskHandler(data = data)        
    
    def process_data(self, data):
        self.member_id = data["message"]["member_id"]
        self.organization_id = data["message"]["organization_id"]
        self.event = data["event"]
    
    @staticmethod
    def get_schema():
        return {"event":"leave_organization"}

    def __execute_operations(self):
        default_channels = self.__retrieve_user_channels(self.organization_id, self.member_id) 
        print(f"Default Chnnales {default_channels}")   
        self.__remove_from_channels(self.member_id, self.organization_id, default_channels)

    def __retrieve_user_channels(self, org_id, user_id):
        print("GETTING USER CHANNELS")
        endpoint_url = f"/v1/{org_id}/channels/users/{user_id}/"
        response = requests.get(RemoveTaskHandler.__BASE_URL + endpoint_url)
        if response.status_code < 500:
            try:
                data = response.json()
                print(data)
                channel_ids = [i["_id"] for i in data]
                print("GOTTEN CHANNELS")
                print(channel_ids or "Member does not belong to any channels")
                return channel_ids or []
            

            except Exception as e:
                print(e)
                return []
                # raise BadServerResponse
        else:
            raise BadServerResponse

    def __remove_from_channels(self, member_id, org_id, channels=[]):
        if len(channels) > 0:
            for channel_id in channels:
                try:
                    endpoint_url = f"/v1/{org_id}/channels/{channel_id}/members/{member_id}/"
                    response = requests.delete(RemoveTaskHandler.__BASE_URL + endpoint_url)
                except Exception as e:
                    raise BadServerResponse

    
    
    