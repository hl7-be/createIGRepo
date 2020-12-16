import requests
import json
import base64
from requests.auth import HTTPBasicAuth
import os
from pprint import pprint


baseUrl = 'https://api.github.com/'
headers1 = {'Accept': 'application/vnd.github.v3+json'}
headers2 = {'Accept': 'application/vnd.github.baptiste-preview+json'}
headers3 = {'Accept': 'application/vnd.github.inertia-preview+json'}

user = 'costateixeira'
token = ''  # Add your secret token here
auth = HTTPBasicAuth(user, token)
email = 'hl7belgium@gmail.com'
hook_active = False

owner = 'costateixeira'
repo = 'test4'
ownerType = 'org'
template_owner = 'hl7-be'
template_repo = 'empty-ig'

create_project   = False
create_repo      = False
create_readme    = False
create_gitignore = False
create_hook      = True
create_columns   = False


url = baseUrl+'users/'+owner
r = requests.get(url, headers=headers1)
if (r.status_code == 200):
    data = r.json()
    ownerType=data['type']
if (ownerType=='User'):
  print('USER')
else:
  if (ownerType=='Organization'):
    print('ORG')
  else:
    print('ERROR')


########### POST repo
create_repo_url=baseUrl+'repos/'+template_owner+'/'+template_repo+'/generate'
repo_create_body ={'owner': owner,'name': repo, 'description': repo + "Implementation Guide" }

if create_repo:
    r = requests.post(create_repo_url, data=json.dumps(repo_create_body), headers=headers2, auth=auth)
    if (r.status_code == 201):
        response=r.json()
        print('Repository Created')


create_file_url = baseUrl+'repos/'+owner+'/'+repo+'/contents/'

################################################################# CREATE README ####################################################################
########### GET README.md sha
r = requests.get(create_file_url+'README.md', headers=headers1, auth=auth)
readme_sha=''
if (r.status_code == 200):
    response=r.json()
    if ("sha" in response):
        readme_sha = response['sha']
        print("README.md exists")

########### POST README
if create_readme:
    readme = "Empty IG\n---\nThis is an empty IG\n<br> </br>\n###\n### Publication\nThis ImplementationGuide is published in the following locations:\n\nContinuous Build: __http://build.fhir.org/ig/"+owner+"/"+repo+"/branches/main/index.html__  \nCanonical / permanent URL: \n<br> </br>\n\n### Issues\nIssues and change requests are managed here:  \n\nIssues:  __https://github.com/"+owner+"/"+repo+"/issues__  \nKanban board:  __https://github.com/"""+owner+"/"+repo+"/projects/"+projectId+"__  \n\n"
    readme_enc = base64.b64encode(readme.encode('utf-8'))
    create_readme_body = {'message': "create readme", 'committer': {'name': owner,'email': email}, "sha": readme_sha, "content": readme_enc.decode('utf-8')}
    r = requests.put(create_file_url+"README.md", data=json.dumps(create_readme_body), headers=headers1, auth=auth)
    if (r.status_code == 200):
        response=r.json()
        print('README.md Created')


################################################################# CREATE .gitignore ####################################################################
r = requests.get(create_file_url+'.gitignore', headers=headers1, auth=auth)
gitignore_sha=''
if (r.status_code == 200):
    response=r.json()
    if ("sha" in response):
        gitignore_sha = response['sha']
        print("README.md exists")

########### POST .gitignore
if create_gitignore:
    gitignore = "Empty IG\n---\nThis is an empty IG\n<br> </br>\n###\n### Publication\nThis ImplementationGuide is published in the following locations:\n\nContinuous Build: __http://build.fhir.org/ig/"+owner+"/"+repo+"/branches/main/index.html__  \nCanonical / permanent URL: \n<br> </br>\n\n### Issues\nIssues and change requests are managed here:  \n\nIssues:  __https://github.com/"+owner+"/"+repo+"/issues__  \nKanban board:  __https://github.com/"""+owner+"/"+repo+"/projects/"+projectId+"__  \n\n"
    gitignore = base64.b64encode(gitignore.encode('utf-8'))
    create_gitignore_body = {'message': "create gitignore", 'committer': {'name': owner,'email': email}, "sha": gitignore_sha, "content": "IyBUZW1wb3JhcnkgZm9sZGVycyAjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIwp0ZW1wCnRlbXBsYXRlCm91dHB1dApmc2gtZ2VuZXJhdGVkLwoKIyBEb24ndCBjb21taXQgdGhpcyBiZWNhdXNlIGl0J3Mgc28gbGFyZ2UgIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjCi9pbnB1dC1jYWNoZS9vcmcuaGw3LmZoaXIucHVibGlzaGVyLmphcgovaW5wdXQtY2FjaGUvcHVibGlzaGVyLmphcgoKIyBXaW5kb3dzIGdlbmVyYXRlZCBmaWxlcyAjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwpUaHVtYnMuZGIKCiMgT1MgZ2VuZXJhdGVkIGZpbGVzICMKIyMjIyMjIyMjIyMjIyMjIyMjIyMjIwouRFNfU3RvcmUKLkRTX1N0b3JlPwoKIyBiYWNrdXAgZmlsZXMgIwojIyMjIyMjIyMjIyMjIyMjCiouYmFr"}
    r = requests.put(create_file_url+".gitignore", data=json.dumps(create_gitignore_body), headers=headers1, auth=auth)
    if (r.status_code == 200):
        response=r.json()
        print('.gitignore Created')



################################################################# CREATE Project ####################################################################
## see if project exists
projectId = ''
project_url = baseUrl+'repos/'+owner+'/'+repo+'/projects'
r = requests.request("GET", project_url, headers=headers3, auth=auth)
if (r.status_code == 200):
    print(r.text)
    response= json.loads(r.text)

    for r in response:
        if (r['name'] =='ImplementationGuide Issues'):
            projectId = r['id']
            print("Project exists")



if create_project:
    if (projectId == ''):
        create_project_url = baseUrl+'repos/'+owner+'/'+repo+'/projects'
        project_data = {"name": "ImplementationGuide Issues",  "body": "Project for managing the IG issues"}
        r = requests.post(create_project_url, data=json.dumps(project_data), headers=headers3, auth=auth)
        if (r.status_code == 201):
            response=r.json()
            projectId = response['id']
            print("Project created")


columns= {'inbox':{'name':'Inbox', 'id':''},'todo':{'name':'To Do', 'id':''},'wip':{'name':'In Progress', 'id':''},'done':{'name':'Done', 'id':''}}
columnList= ['inbox','todo','wip','done']

################################################################# CREATE Project columns ####################################################################
if create_columns:
    create_column_url = baseUrl+'projects/'+str(projectId)+'/columns'
    for columnName in columnList:
        column_title=columns[columnName]['name']
        column_data =  {'name':column_title}
        r = requests.post(create_column_url, data=json.dumps(column_data), headers=headers3, auth=auth)
        if (r.status_code == 201):
            response=r.json()
            columns[columnName]['id'] = response['id']
            print("column \""+column_title+ "\" created")
    print("You should manually set the column automation: \n - When issues are open - Inbox; \n - When issues are closed - Done")



################################################################# CREATE Webhook ####################################################################
### HOOK
if create_hook:
    post_hook_url = baseUrl+'repos/'+owner+'/'+repo+'/hooks'
    post_hook_payload = { 'name': 'web', 'active': hook_active,  'events': ['push'],'config': {'content_type': 'json','insecure_ssl': '0', 'url': 'https://us-central1-fhir-org-starter-project.cloudfunctions.net/ig-commit-trigger' }}
    r = requests.request("POST", post_hook_url, data=json.dumps(post_hook_payload), headers=headers3, auth=auth)
    if (r.status_code == 201):
        if hook_active:
            print("webhook created - active")
        else:
            print("webhook created - inactive")


## To Do:
# * Programmatically Setup automation
# * Also create feedback form  and data/features.xml
# * Add metadata for publication (when that is decided and working)

