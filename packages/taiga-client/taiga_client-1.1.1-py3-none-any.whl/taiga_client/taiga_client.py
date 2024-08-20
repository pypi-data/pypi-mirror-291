import requests
import json
from typing import List
from types import SimpleNamespace

class TaigaAPI:
    def __init__(self, serverIp: str, username: str, password: str, protocol: str = "https://") -> None:
        self.username = username
        self.password = password
        self.serverIp = protocol + serverIp

    def __getToken(self) -> str:
        """
        The function for obtaining an authorization token.
        """
        url = f"{self.serverIp}/api/v1/auth"
        headers = {"Content-Type": "application/json"}
        data = {
            "password": self.password,
            "type": "normal",
            "username": self.username
        }

        response = requests.post(url, headers=headers, json=data)

        auth = json.loads(response.text)
        return auth['auth_token']

    def getProjectBySlug(self, slug: str) -> SimpleNamespace:
        """
        The function for retrieving a project object by its slug.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/projects/by_slug?slug={slug}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createIssuse(self, projectID: int, subject: str, description: str, type: int, priority: int, status: int, tags: List[str] = []) -> SimpleNamespace:
        """
        The function for making issuse.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/issues"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "assigned_to": None,
            "description": description,
            "project": projectID,
            "subject": subject,
            "priority": priority,
            "watchers": [],
            "tags": tags,
            "status": status,
            "type": type
        }
        response = requests.post(url, headers=headers, json=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createEpic(self, projectID: int, subject: str, description: str, status: int, tags: List[str] = []) -> SimpleNamespace:
        """
        The function for making epic.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epics"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "assigned_to": None,
            "description": description,
            "project": projectID,
            "subject": subject,
            "watchers": [],
            "tags": tags,
            "status": status,
        }
        response = requests.post(url, headers=headers, json=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createUserstory(self, projectID: int, subject: str, description: str, status: int, swimlane: int = -1, tags: List[str] = []) -> SimpleNamespace:
        """
        The function for making epic.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/userstories"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        data = {
            "assigned_to": None,
            "description": description,
            "project": projectID,
            "subject": subject,
            "watchers": [],
            "tags": tags,
            "status": status,
            "swimlane": swimlane
        }
        response = requests.post(url, headers=headers, json=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data


    def createAttacementForIssue(self, projectID: int, issueID: int, attachmentPath: str, fromComment=False) -> SimpleNamespace:
        """
        The function for creating an attachment by the issue's ID.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/issues/attachments"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "attached_file": open(attachmentPath, "rb")
        }

        data = {
            "from_comment": fromComment,
            "object_id": issueID,
            "project": projectID
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createAttacementForEpic(self, projectID: int, objectID: int, attachmentPath: str, fromComment=False) -> SimpleNamespace:
        """
        The function for creating an attachment by the epic's ID.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epics/attachments"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "attached_file": open(attachmentPath, "rb")
        }

        data = {
            "from_comment": fromComment,
            "object_id": objectID,
            "project": projectID
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createAttacementForUserstory(self, projectID: int, objectID: int, attachmentPath: str, fromComment=False) -> SimpleNamespace:
        """
        The function for creating an attachment by the epic's ID.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/userstories/attachments"
        headers = {
            "Authorization": f"Bearer {token}"
        }

        files = {
            "attached_file": open(attachmentPath, "rb")
        }

        data = {
            "from_comment": fromComment,
            "object_id": objectID,
            "project": projectID
        }

        response = requests.post(url, headers=headers, files=files, data=data)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def getPriotityList(self, projectID: int):
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/priorities?project={projectID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def getStatusIssueList(self, projectID: int) -> SimpleNamespace:
        """
        This function returns a list of priority objects for issues.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/issue-statuses?project={projectID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def getTypeIssueList(self, projectID: int) -> SimpleNamespace:
        """
        This function returns a list of type objects for issues.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/issue-types?project={projectID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data


    def createIssueComment(self, issueID: int, text: str):
        """
        This function creates a comment for an issue.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/issues/{issueID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        data = {
        "comment": text,
        "version": 1
        }
        response = requests.patch(url, headers=headers, json=data)

        return response


    def getStatusUserstoryList(self, projectID: int) -> SimpleNamespace:
        """
        This function returns a list of possible statuses for a user story.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/userstory-statuses?project={projectID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createUserstoryComment(self, userstoryID: int, text: str):
        """
        This function creates a comment for an issue.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/userstories/{userstoryID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        data = {
        "comment": text,
        "version": 1
        }
        response = requests.patch(url, headers=headers, json=data)

        return response

    def getStatusEpicList(self, projectID: int)-> SimpleNamespace:
        """
        This function returns a list of possible statuses for a epic.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epic-statuses?project={projectID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createEpicComment(self, epicID: int, text: str):
        """
        This function creates a comment for an epic.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epics/{epicID}"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        data = {
        "comment": text,
        "version": 1
        }
        response = requests.patch(url, headers=headers, json=data)

        return response

    def getEpicList(self, projectID: int) -> SimpleNamespace:
        """
        This function returns a list of all epics.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epics?project={projectID}"
        headers = {
            "x-disable-pagination": "True",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def getUserstoryList(self, projectID: int) -> SimpleNamespace:
        """
        This function returns a list of all epics.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/userstories?project={projectID}"
        headers = {
            "x-disable-pagination": "True",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        response = requests.get(url, headers=headers)

        data = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))

        return data

    def createLinkForUserstoryToEpic(self, epicID: int, userstoryID: str):
        """
        This function links a user story to an epic.
        """
        token = self.__getToken()
        url = f"{self.serverIp}/api/v1/epics/{epicID}/related_userstories"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            
        }
        data = {
            "epic": epicID,
            "user_story": userstoryID
        }
        response = requests.post(url, headers=headers, json=data)

        return response
    
    def getStatusIdFromStr(self, projectID: int, statusStr: str) -> int:
        """
        Return status id form str.
        """
        userStoryStatusList = self.getStatusUserstoryList(projectID)
        for status in userStoryStatusList:
            if status.name.lower() == statusStr.lower():
                return status.id
        return -1