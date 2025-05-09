#!/usr/bin/python
DOCUMENTATION = '''
---
module: github_repo
short_description: Manage your repos on Github
'''

EXAMPLES = '''
- name: Create a github Repo
  github_repo:
    github_auth_key: "..."
    name: "Hello-World"
    description: "This is your first repository"
    private: yes
    has_issues: no
    has_wiki: no
    has_downloads: no
  register: result

- name: Delete that repo
  github_repo:
    github_auth_key: "..."
    name: "Hello-World"
    state: absent
  register: result
'''
def main():

    fields = {
        "github_auth_key": {"required": True, "type": "str"},
        "username": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "description": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool"},
        "has_issues": {"default": True, "type": "bool"},
        "has_wiki": {"default": True, "type": "bool"},
        "has_downloads": {"default": True, "type": "bool"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
    }

    module = AnsibleModule(argument_spec=fields)
    module.exit_json(changed=False, meta=module.params)
    - name: Create a github Repo
      github_repo:
        github_auth_key: "..."
        username: "YOUR GITHUB USERNAME HERE"
        name: "Hello-World"
        description: "This is your first repository"
        private: yes
        has_issues: no
        has_wiki: no
        has_downloads: no
        state: present
      register: result
    
from ansible.module_utils.basic import *
import requests

api_url = "https://api.github.com"


def github_repo_present(data):

    api_key = data['github_auth_key']

    del data['state']
    del data['github_auth_key']

    headers = {
        "Authorization": "token {}" . format(api_key)
    }
    url = "{}{}" . format(api_url, '/user/repos')
    result = requests.post(url, json.dumps(data), headers=headers)

    if result.status_code == 201:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()

    # default: something went wrong
    meta = {"status": result.status_code, 'response': result.json()}
    return True, False, meta
def github_repo_absent(data=None):
    headers = {
        "Authorization": "token {}" . format(data['github_auth_key'])
    }
    url = "{}/repos/{}/{}" . format(api_url, data['username'], data['name'])
    result = requests.delete(url, headers=headers)

    if result.status_code == 204:
        return False, True, {"status": "SUCCESS"}
    if result.status_code == 404:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result