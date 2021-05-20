import fnmatch
import requests
import yaml

from github import Github
from nested_lookup import nested_lookup

pat_key = ''

user_repo = input("Enter the repository link :\n")
key_to_find = input('Enter the key you want to find :\n')

key_found = False

split_chars = user_repo.split('/')

user = ''
repository = ''
branch = 'master'

if split_chars[-2] == 'tree':
  user = str(split_chars[-4])
  repository = str(split_chars[-3])
  branch = str(split_chars[-1])


g = Github(pat_key)
repo = g.get_repo(f"{user}/{repository}")
contents = repo.get_contents("", ref=f"{branch}")

file_list = []
while contents:
  file_content = contents.pop(0)
  if file_content.type == "dir":
    contents.extend(repo.get_contents(file_content.path))
  else:
    file_list.append(str(file_content))

files = []
for file_path in file_list:
  file_path.split('"')
  files.append(file_path.split('"')[1])

pattern = '*.yaml'
yml_files = fnmatch.filter(files, pattern)

for file in yml_files:
  file_url = f"https://raw.githubusercontent.com/{user}/{repository}/{branch}/{file}"
  r = requests.get(url = file_url)
  try:
    yaml_file = yaml.load(r.text, Loader=yaml.BaseLoader)
  except Exception:
    pass
  result = nested_lookup(f'{key_to_find}', yaml_file)
  if result:
    print(result, f"{file}")
    key_found = True

if key_found == False:
    print("No Key Found")
