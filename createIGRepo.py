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
create_repo      = True    # whether a repository needs to be created. Pretty much everything wlse will fail if this is not True 
create_project   = True    # whether a kanban project with issues is to be created.
repo_private     = False    # True will make the created repository private (note that the gh-pages will not be visible and the CI-build webhook will not work for private repos
create_readme    = True    # If True, a simple readme will be created with the relevant URLs filled in
create_gitignore = True    # if True, a standard .gitignore file will be created. Recommended value: True
create_columns   = True    # if True, the kanban columns will be created
create_hook      = True    # If True, the repository will create (but not activate) the Continuous IG build webhook which will deploy to build.fhir.org upon each commit to the main branch
hook_active      = False   # If True, the repository will activate the Continuous IG build webhook
create_workflow  = False   # If True, the repository will include a workflow to deploy the IG using github pipeline and github pages, independently of the build.fhir.org webhook


## this is the repository that is going to be created
user = 'costateixeira' # This script needs github credentials. add your username here
token = ''  # This script needs github credentials. Add your secret token here
# To Do: Add the token in an extenal file and .gitignore it

email = 'mail@hl7-be.org' # The email address that will be associated with the repository
owner = 'hl7-be' # this is the owner or organization where the repository is going to be created
repo = 'tutorial_ig' # this is the repository that is going to be created


ownerType = ''

template_repo = 'empty-ig' # this is the template repository that is going to be used - it will be cloned into the new IG
template_owner = 'hl7-be' # this is the owner of the template repository

###############################y######################################################################################
#####################################     Don't change beyond this point    #########################################
#####################################################################################################################


if (user==''):
  user = input("Username (to login): ")   
print("username: "+user+"\n")

if (token==''):
  token = input("Token or password is empty. Add your password or token: ")   
auth = HTTPBasicAuth(user, token)

# TO DO: Try auth to see if OK. Exit if not

if (email==''):
  email = input("email of repository owner: ")   
print("Owner email: "+email+"\n")

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
  print("Private repository: "+str(repo_private)+"\n")
except:
  repo_private = (input("Private repository? (Y/N): ").upper() == 'Y')
  print("Private repository: "+str(repo_private)+"\n")

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



try:
  print("Create CI workflow: "+str(create_workflow)+"\n")
except:
  create_workflow = (input("Create CI workflow? (Y/N): ").upper() == 'Y')
  print("Create CI workflow: "+str(create_workflow)+"\n")



########### POST repo
create_repo_url=baseUrl+'repos/'+template_owner+'/'+template_repo+'/generate'
repo_create_body ={'owner': owner,'name': repo, 'description': repo + "Implementation Guide", 'include_all_branches':True, 'private': repo_private }

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
    create_gitignore_body = {'message': "create gitignore", 'committer': {'name': owner,'email': email}, "sha": gitignore_sha, "content": "IyBUZW1wb3JhcnkgZm9sZGVycyAjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIwp0ZW1wCnRlbXBsYXRlCm91dHB1dAppbnB1dC1jYWNoZQpmc2gtZ2VuZXJhdGVkCgojIERvbid0IGNvbW1pdCB0aGlzIGJlY2F1c2UgaXQncyBzbyBsYXJnZSAjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKL2lucHV0LWNhY2hlL3B1Ymxpc2hlci5qYXIKCiMgV2luZG93cyBnZW5lcmF0ZWQgZmlsZXMgIwojIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKVGh1bWJzLmRiCgojIE9TIGdlbmVyYXRlZCBmaWxlcyAjCiMjIyMjIyMjIyMjIyMjIyMjIyMjIyMKLkRTX1N0b3JlCi5EU19TdG9yZT8KCiMgYmFja3VwIGZpbGVzICMKIyMjIyMjIyMjIyMjIyMjIwoqLmJhawo="}
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
    readme = "Empty IG\n---\nThis is an empty IG\n<br> </br>\n###\n### Publication\nThis ImplementationGuide is published in the following locations:\n\nContinuous Build: __http://build.fhir.org/ig/"+owner+"/"+repo+"/branches/main/index.html__  \nCanonical / permanent URL: \n<br> </br>\n\n### Issues\nIssues and change requests are managed here:  \n\nIssues:  __https://github.com/"+owner+"/"+repo+"/issues__  \nKanban board:  __https://github.com/"""+owner+"/"+repo+"/projects/1__  \n\n"
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


########### POST workflow
if create_workflow:
    
    create_gitactions_body = {'message': "create gitignore", 'committer': {'name': owner,'email': email}, "sha": gitignore_sha, "content": "IyBUaGlzIGlzIGEgc2ltcGxlIHdvcmtmbG93IHRoYXQgcnVucyB0aGUgcHVibGlzaGVyIGFuZCBjb3BpZXMgdGhlIG91dHB1dCB0byBodHRwczovLzxvd25lcj4uZ2l0aHViLmlvLzxyZXBvPi9pbmRleC5odG1sCiMgQmFzZWQgb24gdGhlIGluc3RydWN0aW9ucyBmcm9tIEVsbGlvdCBTaWx2ZXIsIGF2YWlsYWJsZSBmcm9tOiBodHRwczovL3d3dy5hcmdlbnRpeGluZm8uY29tL2FyY2hpdmVzLzE1NgojIE1ha2Ugc3VyZSB5b3VyIHJlcG8gaGFzIGEgYnJhbmNoIGNhbGxlZCBnaC1wYWdlcwoKCiMgVXBkYXRlIDE1LUphbi0yMDIxOiBUaGlzIG5vdyBhZGRzIGEgRlRQIHVwbG9hZCBmZWF0dXJlLiBUaGlzIHVzZXMgYSByZXBvc2l0b3J5IHNlY3JldC4KIyBBY3Rpb24gZG9jdW1lbnRhdGlvbgojIGh0dHBzOi8vZ2l0aHViLmNvbS9tYXJrZXRwbGFjZS9hY3Rpb25zL2Z0cC1kZXBsb3kKCm5hbWU6IENJCgojIENvbnRyb2xzIHdoZW4gdGhlIGFjdGlvbiB3aWxsIHJ1bi4gCm9uOgogICMgVHJpZ2dlcnMgdGhlIHdvcmtmbG93IG9uIHB1c2ggb3IgcHVsbCByZXF1ZXN0IGV2ZW50cyBidXQgb25seSBmb3IgdGhlIG1haW4gYnJhbmNoCiAgcHVzaDoKICAgIGJyYW5jaGVzOiAKICAgICAgLSBtYWluCiAgICAgIC0gbWFzdGVyCiAgcHVsbF9yZXF1ZXN0OgogICAgYnJhbmNoZXM6IAogICAgICAtIG1haW4KICAgICAgLSBtYXN0ZXIgCgogICMgQWxsb3dzIHlvdSB0byBydW4gdGhpcyB3b3JrZmxvdyBtYW51YWxseSBmcm9tIHRoZSBBY3Rpb25zIHRhYgogIHdvcmtmbG93X2Rpc3BhdGNoOgoKIyBBIHdvcmtmbG93IHJ1biBpcyBtYWRlIHVwIG9mIG9uZSBvciBtb3JlIGpvYnMgdGhhdCBjYW4gcnVuIHNlcXVlbnRpYWxseSBvciBpbiBwYXJhbGxlbApqb2JzOgogICMgVGhpcyB3b3JrZmxvdyBjb250YWlucyBhIHNpbmdsZSBqb2IgY2FsbGVkICJidWlsZCIKICBidWlsZDoKICAgICMgVGhlIHR5cGUgb2YgcnVubmVyIHRoYXQgdGhlIGpvYiB3aWxsIHJ1biBvbgogICAgcnVucy1vbjogdWJ1bnR1LWxhdGVzdAoKICAgICMgU3RlcHMgcmVwcmVzZW50IGEgc2VxdWVuY2Ugb2YgdGFza3MgdGhhdCB3aWxsIGJlIGV4ZWN1dGVkIGFzIHBhcnQgb2YgdGhlIGpvYgogICAgc3RlcHM6CiAgICAgICMgQ2hlY2tzLW91dCB5b3VyIHJlcG9zaXRvcnkgdW5kZXIgJEdJVEhVQl9XT1JLU1BBQ0UsIHNvIHlvdXIgam9iIGNhbiBhY2Nlc3MgaXQKICAgICAgLSB1c2VzOiBhY3Rpb25zL2NoZWNrb3V0QHYyCiAgICAgIC0gbmFtZTogVXBkYXRlIHRoZSBpbWFnZSB0byB0aGUgbGF0ZXN0IHB1Ymxpc2hlcgogICAgICAgIHVzZXM6IGRvY2tlcjovL2hsN2ZoaXIvaWctcHVibGlzaGVyLWJhc2U6bGF0ZXN0CiAgICAgICAgd2l0aDoKICAgICAgICAgICMgR2V0IHRoZSBsYXRlc3QgcHVibGlzaGVyIC0gZG9uJ3QgcnVuIHRoZSBiYXRjaCBzY3JpcHQgYnV0IHJ1biB0aGUgbGluZSBkaXJlY3RseQogICAgICAgICAgYXJnczogY3VybCAtTCBodHRwczovL2dpdGh1Yi5jb20vSEw3L2ZoaXItaWctcHVibGlzaGVyL3JlbGVhc2VzL2xhdGVzdC9kb3dubG9hZC9wdWJsaXNoZXIuamFyIC1vIC4vaW5wdXQtY2FjaGUvcHVibGlzaGVyLmphciAtLWNyZWF0ZS1kaXJzCgogICAgICAtIG5hbWU6IFJ1biB0aGUgSUcgcHVibGlzaGVyCiAgICAgICAgdXNlczogZG9ja2VyOi8vaGw3Zmhpci9pZy1wdWJsaXNoZXItYmFzZTpsYXRlc3QKICAgICAgICB3aXRoOgogICAgICAgICAgIyBSdW4gdGhlIHB1Ymxpc2hlciAtIGRvbid0IHJ1biB0aGUgYmF0Y2ggc2NyaXB0IGJ1dCBydW4gdGhlIGxpbmUgZGlyZWN0bHkKICAgICAgICAgIGFyZ3M6IGphdmEgLWphciAuL2lucHV0LWNhY2hlL3B1Ymxpc2hlci5qYXIgcHVibGlzaGVyIC1pZyAuCgogICAgICAtIG5hbWU6IERlcGxveQogICAgICAgIHVzZXM6IHBlYWNlaXJpcy9hY3Rpb25zLWdoLXBhZ2VzQHYzCiAgICAgICAgd2l0aDoKICAgICAgICAgIGdpdGh1Yl90b2tlbjogJHt7IHNlY3JldHMuR0lUSFVCX1RPS0VOIH19CiAgICAgICAgICBwdWJsaXNoX2RpcjogLi9vdXRwdXQKCiMgICAgICAtIG5hbWU6IFN5bmMgZmlsZXMKIyAgICAgICAgdXNlczogU2FtS2lya2xhbmQvRlRQLURlcGxveS1BY3Rpb25ANC4wLjAKIyAgICAgICAgd2l0aDoKIyAgICAgICAgICBzZXJ2ZXI6IGZ0cC5kbHB0ZXN0LmNvbQojICAgICAgICAgIHVzZXJuYW1lOiBkbHB1c2VyCiMgICAgICAgICAgcGFzc3dvcmQ6ICR7eyBzZWNyZXRzLmZ0cF9wYXNzd29yZCB9fSAgICAgICAgICAKIyAgICAgICAgICBsb2NhbC1kaXI6IG91dHB1dC8KIyAgICAgICAgICBzZXJ2ZXItZGlyOiBmaGlyL2hpdi8KCiMgICAgICAtIG5hbWU6IEdldCBsYXRlc3QgY29kZQojICAgICAgICB1c2VzOiBhY3Rpb25zL2NoZWNrb3V0QHYyLjMuMgogICAg"}
    r = requests.put(create_file_url+".github/workflows/main.yml", data=json.dumps(create_gitactions_body), headers=headers1, auth=auth)
    if (r.status_code == 200):
        response=r.json()
        print('.github workflow Created')



clone = (input("Create folder "+repo+" in current folder and clone repository? (Y/N): ").upper() == 'Y')
if clone:
  os.mkdir(repo)
  os.system("git clone https://github.com/"+owner+"/"+repo)

