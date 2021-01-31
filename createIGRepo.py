import requests
import json
import base64
from requests.auth import HTTPBasicAuth
import os
from pprint import pprint


# Don't touch this
baseUrl = 'https://api.github.com/'
headers1 = {'Accept': 'application/vnd.github.v3+json'}
headers2 = {'Accept': 'application/vnd.github.baptiste-preview+json'}
headers3 = {'Accept': 'application/vnd.github.inertia-preview+json'}


#####################################################################################################################
################################   CHANGE THE VARIABLES BELOW, LEAVE THE REST  ######################################
#####################################################################################################################


# Set these variables to true or false, or comment them out for prompting
#create_project   = False
#create_repo      = False
#create_readme    = False
#create_gitignore = False
#create_columns   = False
#create_hook      = False
#hook_active      = False


## this is the repository that is going to be created
user = 'costateixeira'
token = ''  # Add your secret token here
email = 'mail@openhie.org'
owner = 'openhie'
repo = 'case-reporting'
#ownerType = ''

## this is the template repository that is going to be cloned
template_owner = 'openhie'
template_repo = 'empty-fhir-ig'

#####################################################################################################################
#####################################     Don't change beyond this point    #########################################
#####################################################################################################################


if (user==''):
  user = input("Username (to login): ")   
print("username: "+owner+"\n")

if (token==''):
  token = input("Token or password is empty. Add your password or token: ")   
auth = HTTPBasicAuth(user, token)

# TO DO: Try auth to see if OK. Exit if not

if (email==''):
  email = input("email of repository owner: ")   
print("Owner email: "+owner+"\n")

if (owner==''):
  owner = input("Repository owner (github handle to create repository): ")   
print("Repository owner: "+owner+"\n")
# TO DO: Check if handle exists?? exit if not


url = baseUrl+'users/'+owner
r = requests.get(url, headers=headers1)
if (r.status_code == 200):
    data = r.json()
    ownerType=data['type']
if (ownerType=='User'):
    print('Owner is an user')
else:
  if (ownerType=='Organization'):
    print('Owner is an organization')
  else:
    print('ERROR - owner not found or not accessible. Exiting...\n')
    exit(1)



if (repo==''):
  repo = input("Repository name: ")   

# Check if repo exists?? and set createRepo accordingly
r = requests.get(baseUrl+'repos/'+owner+'/'+repo, headers=headers2, auth=auth)
if (r.status_code == 200):
  print("Repository exits: "+owner+"/"+repo+"\n")
else:
  print("Repository will be created: "+owner+"/"+repo+"\n")



if (template_owner==''):
  template_owner = input("Template repository owner: ")   
print("Using template owner: "+template_owner+"\n")


if (template_repo==''):
  template_repo = input("Template repository name: ")   
print("Using template repository: "+template_repo+"\n")

r = requests.get(baseUrl+'repos/'+template_owner+'/'+template_repo, headers=headers2, auth=auth)
# TO DO: Check if template repo exists? abort if not
if (r.status_code == 200):
  print("Template exists: "+template_owner+"/"+template_repo+"\n")
else:
  print("Template does not exist: "+template_owner+"/"+template_repo+"\n. Exiting...\n")
  exit(1)

# exit(0) #for debugging, stop here before actually changing anything



try:
  print("Create project: "+str(create_project)+"\n")
except:
  create_project = (input("Create Project? (Y/N): ").upper() == 'Y')
  print("Create project: "+str(create_project)+"\n")

try:
  print("Create repository: "+str(create_repo)+"\n")
except:
  create_repo = (input("Create repository? (Y/N): ").upper() == 'Y')
  print("Create repository: "+str(create_repo)+"\n")

try:
  print("Create/Update README.md: "+str(create_readme)+"\n")
except:
  create_readme = (input("Create/Update README.md? (Y/N): ").upper() == 'Y')
  print("Create/Update README.md: "+str(create_readme)+"\n")

try:
  print("Create/update standard .gitignore: "+str(create_gitignore)+"\n")
except:
  create_gitignore = (input("Create standard .gitignore? (Y/N): ").upper() == 'Y')
  print("Create/update standard .gitignore: "+str(create_gitignore)+"\n")


try:
  print("Create kanban columns: "+str(create_columns)+"\n")
except:
  create_columns = (input("Create kanban columns? (Y/N): ").upper() == 'Y')
  print("Create kanban columns: "+str(create_columns)+"\n")


try:
  print("Create CI Build hook: "+str(create_hook)+"\n")
except:
  create_hook = (input("Create CI Build hook? (Y/N): ").upper() == 'Y')
  print("Create CI Build hook: "+str(create_hook)+"\n")

try:
  print("Activate CI Build hook: "+str(hook_active)+"\n")
except:
  hook_active = (input("Activate CI Build hook? (Y/N): ").upper() == 'Y')
  print("Activate CI Build hook: "+str(hook_active)+"\n")



########### POST repo
create_repo_url=baseUrl+'repos/'+template_owner+'/'+template_repo+'/generate'
repo_create_body ={'owner': owner,'name': repo, 'description': repo + "Implementation Guide" }

if create_repo:
    r = requests.post(create_repo_url, data=json.dumps(repo_create_body), headers=headers2, auth=auth)
    if (r.status_code == 201):
        response=r.json()
        print('Repository Created')


create_file_url = baseUrl+'repos/'+owner+'/'+repo+'/contents/'


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
    gitignore = "# Temporary folders #\n#####################\ntemp\ntemplate\noutput\nfsh-generated\n\n# Don't commit this because it's so large #\n###########################################\n/input-cache/publisher.jar\n\n# Windows generated files #\n###########################\nThumbs.db\n\n# OS generated files #\n######################\n.DS_Store\n.DS_Store?\n\n# backup files #\n################\n*.bak"
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

readme = ''
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
    readme = "Empty IG\n---\nThis is an empty IG\n<br> </br>\n###\n### Publication\nThis ImplementationGuide is published in the following locations:\n\nContinuous Build: __http://build.fhir.org/ig/"+owner+"/"+repo+"/branches/main/index.html__  \nCanonical / permanent URL: \n<br> </br>\n\n### Issues\nIssues and change requests are managed here:  \n\nIssues:  __https://github.com/"+owner+"/"+repo+"/issues__  \nKanban board:  __https://github.com/"""+owner+"/"+repo+"/projects/"+str(projectId)+"__  \n\n"
    readme_enc = base64.b64encode(readme.encode('utf-8'))
    create_readme_body = {'message': "create readme", 'committer': {'name': owner,'email': email}, "sha": readme_sha, "content": readme_enc.decode('utf-8')}
    r = requests.put(create_file_url+"README.md", data=json.dumps(create_readme_body), headers=headers1, auth=auth)
    if (r.status_code == 200):
        response=r.json()
        print('README.md Created')



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

