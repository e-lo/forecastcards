import csv
import requests

def get_csv_from_url(url):
    with requests.Session() as s:
        download = s.get(url)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        return cr

def raw_github_url(username, repository, branch='master', subdir=''):
    gh = "https://raw.githubusercontent.com/"+str(username)+"/"+str(repository)+"/"+str(branch)+"/"+subdir
    return gh

def api_github_url(username, repository, branch='master'):
    gh = "https://api.github.com/repos/"+str(username)+"/"+str(repository)+"/git/trees/"+str(branch)+"?recursive=1"
    return gh
