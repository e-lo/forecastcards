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

def github_url_to_dict(gh_url):
    '''
    :gh_url: is the url to a repository or a subfolder in a github repository
             example: https://github.com/e-lo/forecastcards/tree/master/forecastcards/examples
    :returns: dictionary of username repository, branch, and subdirectory
    '''
    g = gh_url[gh_url.find("github"):].strip().split("/")
    gh_dict = {}
    gh_dict['username'] = g[1]
    gh_dict['repository'] = g[2]
    gh_dict['branch'] = g[4]
    gh_dict['subdir'] = ''
    if len(g)>4:
        gh_dict['subdir']='/'.join(g[5:])
    return gh_dict
