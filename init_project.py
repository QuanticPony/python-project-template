# Copyright 2023 Unai Lería Fortea

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, re

SETUP_FILE = lambda project_name: f"""from setuptools import setup\n\nif __name__=='__main__':\n\tsetup(packages=["{project_name}"])"""
README_FILE = lambda project_name: f"""# {project_name}\n"""
LICENSE = lambda year, user_full_name: f"""Copyright {year} {user_full_name}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""


USER_FULL_NAME = ""
USER_NAME = ""
USER_MAIL = ""

PROJECT_NAME = ""
PROJECT_DIRECTORY = "."

YEAR = ""


def replace(content: str) -> str:
    content_new = re.sub(r'(\$\{USER_FULL_NAME\})', USER_FULL_NAME, content, flags=re.ASCII)
    content_new = re.sub(r'(\$\{USER_NAME\})', USER_NAME, content_new, flags=re.ASCII)
    content_new = re.sub(r'(\$\{USER_MAIL\})', USER_MAIL, content_new, flags=re.ASCII)
    content_new = re.sub(r'(\$\{PROJECT_NAME\})', PROJECT_NAME, content_new, flags=re.ASCII)
    content_new = re.sub(r'(\$\{PROJECT_DIRECTORY\})', PROJECT_DIRECTORY, content_new, flags=re.ASCII)
    content_new = re.sub(r'(\$\{YEAR\})', YEAR, content_new, flags=re.ASCII)
    return content_new

def replace_file(filename: str) -> None:
    new_content: str
    with open(filename, 'r') as fin:
        content = fin.read()
        new_content = replace(content)
    with open(filename, 'w') as fout:
        fout.write(new_content)



def replace_recursive(path: str) -> None:
    for file in os.listdir(path):
        filename = os.fsdecode(file)
        try:
            replace_file(f"{path}/{filename}")
        except IsADirectoryError:
            replace_recursive(f"{path}/{filename}")
        except Exception:
            pass


if __name__ == '__main__':

    if not PROJECT_NAME:
        raise Exception("Project name can not be null")
    

    replace_recursive(PROJECT_DIRECTORY)
            

    
    if not os.path.exists(f"{PROJECT_DIRECTORY}/{PROJECT_NAME}"):
        os.makedirs(f"{PROJECT_DIRECTORY}/{PROJECT_NAME}")
    if not os.path.exists(f"{PROJECT_DIRECTORY}/examples"):
        os.makedirs(f"{PROJECT_DIRECTORY}/examples")



    with open("setup.py", 'w') as setup_file:
        setup_file.write(SETUP_FILE(PROJECT_NAME))