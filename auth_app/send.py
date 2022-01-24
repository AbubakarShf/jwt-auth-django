import json
import requests
# def getStudentData(token):
#     headers={}
#     headers['Authorization']='Bearer '+token
#     Data=requests.get('http://127.0.0.1:8000/api/student',headers=headers)
#     # print(Data.text)
#     return Data
# def postStudentData(data,token):
#     headers={}
#     headers['Authorization']='Bearer '+token
#     Data=requests.post('http://127.0.0.1:8000/api/student',headers=headers,data=data)
#     return Data

# def verifyToken(token):
#     Data=requests.post('http://127.0.0.1:8000/verify',data={'token':str(token)})
#     data=json.loads(Data.text)
#     try:
#         if(data['code']=="token_not_valid"):
#             return False
#         else:
#             return True
#     except:
#         return True