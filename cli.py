import toml
import inquirer

# Prompt the user for project details
project_questions = [
    inquirer.Text('region', message="Enter the region"),
    inquirer.Text('project_id', message="Enter the project ID"),
    inquirer.Text('repo', message="Enter the repository"),
    inquirer.Text('image', message="Enter the image")
]
project_answers = inquirer.prompt(project_questions)

# Prompt the user for service account details
service_account_questions = [
    inquirer.Text('name', message="Enter the service account name"),
    inquirer.Text('description', message="Enter the service account description", default="Docker repository for mycloudrun"),
    inquirer.Text('display_name', message="Enter the service account display name", default=project_answers['name'])
]
service_account_answers = inquirer.prompt(service_account_questions)

# Prompt the user for repository details
repository_questions = [
    inquirer.Text('name', message="Enter the repository name"),
    inquirer.Text('location', message="Enter the repository location"),
    inquirer.Text('description', message="Enter the repository description", default="GH Actions WID Pool")
]
repository_answers = inquirer.prompt(repository_questions)

# Prompt the user for workload identity pool details
workload_identity_pool_questions = [
    inquirer.Text('name', message="Enter the workload identity pool name"),
    inquirer.Text('display_name', message="Enter the workload identity pool display name", default="GH Actions WID Pool")
]
workload_identity_pool_answers = inquirer.prompt(workload_identity_pool_questions)

# Prompt the user for provider details
provider_questions = [
    inquirer.Text('name', message="Enter the provider name"),
    inquirer.Text('issuer_uri', message="Enter the issuer URI", default="https://token.actions.githubusercontent.com"),
    inquirer.Text('repository_owner', message="Enter the repository owner")
]
provider_answers = inquirer.prompt(provider_questions)

# Create a dictionary with the collected input
config_data = {
    'project': project_answers,
    'service_account': service_account_answers,
    'repository': repository_answers,
    'workload_identity_pool': workload_identity_pool_answers,
    'provider': provider_answers
}

# Write the dictionary to config.toml file
with open('config.toml', 'w') as config_file:
    toml.dump(config_data, config_file)

# Print a message indicating that the config.toml file has been created
print("The config.toml file has been created.")
