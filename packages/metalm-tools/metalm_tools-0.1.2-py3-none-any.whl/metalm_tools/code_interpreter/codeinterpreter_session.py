import requests
import json
from typing import Optional, Dict, Any, Union, List
import ast
from pydantic import BaseModel
import base64
import os

def make_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Union[str, int, float]]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = 30
) -> requests.Response:
    """
    Make a generic HTTP request.
    
    :param method: HTTP method (e.g., GET, POST, PUT, DELETE)
    :param url: The URL for the request
    :param headers: Optional headers to include in the request
    :param params: Optional query parameters
    :param data: Data to send in the body of the request (for POST/PUT)
    :param json: JSON data to send in the body of the request (for POST/PUT)
    :param timeout: Request timeout in seconds
    :return: `requests.Response` object
    """

    supported_methods = {
        'GET': requests.get,
        'POST': requests.post,
        'PUT': requests.put,
        'DELETE': requests.delete
    }
    
    if method not in supported_methods:
        raise ValueError(f"Unsupported HTTP method: {method}")

    response = supported_methods[method](
        url,
        headers=headers,
        params=params,
        data=data,
        json=json,
        timeout=timeout
    )

    return response

class File(BaseModel):
    name: str
    content: bytes


class CodeboxOutput(BaseModel):
    output_type: str
    content: str
    files: Optional[List[File]] = None

class CodeinterpreterSession:
    
    def __init__(self,url,apikey):
        self.domain=url
        self.token= apikey
        self.uploaded_files = []
        self.session_id=self.start_session()

    def start_session(self):
        
        url = f"{self.domain}/api/v1/jupyter/start"
        response = make_request(
            method='POST', 
            url=url,
            headers={"accept":"application/json"},
            params={
                "token":"zhejianzhang",
                "language":"JUPYTER"
            }
            )
        session_id=response.text.strip('"')
        print(session_id)
        return session_id

    
    def install(self,packages):
        url = f"{self.domain}/api/v1/jupyter/install"
        data = {
                    "install_request": {
                    "packagenames":packages 
                    },
                    "session_key": {
                        "session_id":self.session_id,
                        "language": "JUPYTER"
                    }
                }
        response = make_request(
            method='POST', 
            url=url,
            headers={"accept":"application/json",'Content-Type': 'application/json'},
            json=data
            )

        print(response)
        print('Execute Result=',response.text)

    def download_files(self, filenames: List[str]):
        url = self.domain + '/api/v1/jupyter/download'
        session_key = {"session_id": self.session_id, "language": "JUPYTER"}
        print(f"file paths: {filenames}")
        headers = {'Content-Type': 'application/json','Accept': 'text/plain'}

        data = {
                "session_key": session_key,
                "filenames": filenames,
            }   
        response = requests.post(url, json=data, headers=headers)
        
        #print(response.status_code)
        # 检查请求是否成功
        if response.status_code == 200:
            for file_data in response.json():
                filename = file_data["name"] 
                content = file_data["content"]
                with open(filename, "w", encoding="utf-8") as f: 
                    f.write(content)
                print(f"Downloaded {filename}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
        return response.text
    
    def upload_files(self,filenames: List[str]):
        files = [(f"upload_files", (os.path.basename(filename), open(filename, 'rb'))) for i, filename in enumerate(filenames)]
        url = self.domain + '/api/v1/upload_batch_dev'
        session_key = json.dumps({"session_id":self.session_id,"language": "JUPYTER"})

        response = requests.post(
            url,  
            data={'session_key':session_key},
            files= files)
        #print(response.status_code)
        for file in files:
            self.uploaded_files.append(file[1][0])
            file[1][1].close()
            
        files_path = ["/codebox/"+ item for item in self.uploaded_files]
        return files_path
        
    def run_code(self,code):
        url = f"{self.domain}/api/v1/jupyter/execute_code"
        data = {
                    "code": {
                    "code": code
                    },
                    "session_key": {
                        "session_id":self.session_id,
                        "language": "JUPYTER"
                    }
                }
        response = make_request(
            method='POST', 
            url=url,
            headers={"accept":"application/json",'Content-Type': 'application/json'},
            json=data
            )
        
        rsp = CodeboxOutput.parse_raw(response.content)
        
        print('Code Execute Result=',rsp.content)
        if rsp.files:
            for item in rsp.files:
                with open(item.name, 'wb') as f:
                    f.write(base64.b64decode(item.content))
                    print(f'image saved at {item.name}')

        return response.text
      
    def close(self):
        url = f"{self.domain}/api/v1/codebox/stop"
        data = {
                        "session_id":self.session_id,
                        "language": "JUPYTER"
                    }
                
        response = make_request(
            method='POST', 
            url=url,
            headers={"accept":"application/json",'Content-Type': 'application/json'},
            json=data
            )

        if response.status_code ==200:
            print('remote container stopped')
        else:
            print('close error')
    
    def __del__(self):
        self.close()
