import csv
import requests
import pandas as pd

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

BASE_HOURLY_TRAFFIC_PATTERN = [
                               ['0:00:00' ,200],
                               ['1:00:00' ,100],
                               ['2:00:00' ,50],
                               ['3:00:00' ,50],
                               ['4:00:00' ,500],
                               ['5:00:00' ,2000],
                               ['6:00:00' ,4000],
                               ['7:00:00' ,4000],
                               ['8:00:00' ,3500],
                               ['9:00:00', 3000],
                               ['10:00:00', 3000],
                               ['11:00:00', 3000],
                               ['12:00:00', 3200],
                               ['13:00:00', 3000],
                               ['14:00:00', 3800],
                               ['15:00:00', 4000],
                               ['16:00:00', 4200],
                               ['17:00:00', 4400],
                               ['18:00:00', 4000],
                               ['19:00:00', 3000],
                               ['20:00:00', 2000],
                               ['21:00:00', 1000],
                               ['22:00:00', 1000],
                               ['23:00:00', 500],
                              ]

def convert_vol_to_daily(value, start_time, end_time, distribution=BASE_HOURLY_TRAFFIC_PATTERN):
    """
    :start_time: is a string in HH:MM:SS
    :end_time: is a string in HH:MM:SS

    """

    start_time_dt = pd.to_datetime(start_time)
    end_time_dt   = pd.to_datetime(end_time)

    v_dist_df = pd.DataFrame(distribution,columns=['start_hour','volume'])
    v_dist_df['start_hour']= pd.to_datetime(v_dist_df['start_hour'], infer_datetime_format=True)
    v_dist_df = v_dist_df.set_index('start_hour')

    # convert from raw volumes to a distribution
    v_dist_df = v_dist_df['volume']/v_dist_df['volume'].sum()

    # convert from hourly to by the second and then interpolate
    dist_second_na = v_dist_df.resample('S').mean()/float(3600)
    dist_second = dist_second_na.interpolate(method='time')

    # return daily approximation based on distribution
    adt = value/dist_second[(dist_second.index>=start_time_dt) & (dist_second.index<end_time_dt)].sum()

    return round(adt,0)
