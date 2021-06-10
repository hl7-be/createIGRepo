# Create IG Repository

This script creates a github repository for a FHIR ImplementationGuide. It takes care of all configurations, as long as the user selects (in the code or via a prompt) the options


## Authentication
This script requires you to apply your github password or, and much better - **a github token that you can generate**

## Options
this project takes the following options

```
create_repo      = True    # whether a repository needs to be created. Pretty much everything wlse will fail if this is not True 
create_project   = True    # whether a kanban project with issues is to be created.
repo_private     = True    # True will make the created repository private (note that the gh-pages will not be visible and the CI-build webhook will not work for private repos
create_readme    = True    # If True, a simple readme will be created with the relevant URLs filled in
create_gitignore = True    # if True, a standard .gitignore file will be created. Recommended value: True
create_columns   = True    # if True, the kanban columns will be created
create_hook      = True    # If True, the repository will create (but not activate) the Continuous IG build webhook which will deploy to build.fhir.org upon each commit to the main branch
hook_active      = False   # If True, the repository will activate the Continuous IG build webhook
create_workflow  = False   # If True, the repository will include a workflow to deploy the IG using github pipeline and github pages, indepentently of the build.fhir.org webhook
```

## Input parameters (will prompt if not predefined)
```
user = '' # This script needs github credentials. add your username here
token = ''  # This script needs github credentials. Add your secret token here
email = 'mail@hl7-be.org' # The email address that will be associated with the repository
owner = 'hl7-be' # this is the owner or organization where the repository is going to be created
repo = 'test_ig' # this is the repository that is going to be created



template_repo = 'empty-ig-custom' # this is the template repository that is going to be used - it will be cloned into the new IG
template_owner = 'hl7-be' # this is the owner of the template repository
```
