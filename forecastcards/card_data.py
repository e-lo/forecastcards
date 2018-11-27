
import requests
import pandas as pd
from goodtables import validate


default_repo_api = "https://api.github.com/repos/e-lo/forecast-cards/git/trees/f35185168b238429157adcbf5ba09d09ae7d0172?recursive=1"

default_subdirs = ["examples"]

def map_data(repo_loc=default_repo_api,subdirs=default_subdirs):
    '''Identify where data is, what schema it should conform to, and return a dictionary with locations.
    '''
    r = requests.get(repo_loc)
    rj = r.json()

    card_locs = {
           "poi": [],
           "scenario": [],
           "project": [],
           "observations": [],
           "forecast": [],
    }
    ## todo better regex matching by project
    for file in rj['tree']:
      path_list = file['path'].split("/")

      if len(path_list)>2 and path_list[1] in subdirs and file['type']=='blob':
          if path_list[-1][0:8].lower()=="forecast":
              full_url = urljoin(repo_raw,file['path'])
              print("adding",full_url,"to forecast")
              card_locs["forecast"].append(full_url)
          if path_list[-1][0:12].lower()=="observations":
              full_url = urljoin(repo_raw,file['path'])
              print("adding",full_url,"to observations")
              card_locs["observations"].append(full_url)
          if path_list[-1][0:3].lower()=="poi":
              full_url = urljoin(repo_raw,file['path'])
              print("adding",full_url,"to poi")
              card_locs["poi"].append(full_url)
          if path_list[-1][0:7].lower()=="project":
              full_url = urljoin(repo_raw,file['path'])
              print("adding",full_url,"to project")
              card_locs["project"].append(full_url)
          if path_list[-1][0:8].lower()=="scenario":
              full_url = urljoin(repo_raw,file['path'])
              print("adding",full_url,"to scenario")
              card_locs["scenario"].append(full_url)

    return card_locs

def validate_cards(card_locs,schemas_loc):
    '''
    If errors are found, try https://try.goodtables.io as a good GUI for identifying issues.
    '''
    reports={}
    for k,v in card_locs.items():
      #print ("validating",k,v)
      reports[k] = validate(card_locs[k][0],schema=requests.get(schemas_loc[k]).json())
      if not reports[k]['valid']:
        print ("--->INVALID TABLE", k)
        reports[k]
      else:
        print ("--->VALID",k)
    return reports


def combine_data(card_locs):
    '''
    Combine tables by card type and merge tables on keys.
    '''

    #Combine tables by type
    project_df = pd.concat(
        [pd.read_csv(
            f,
            parse_dates=['year_open_planned','year_horizon','date_open_actual'],
            infer_datetime_format=True,
            ) for f in card_locs["project"]
        ],
        ignore_index=True,
    )

    scenario_df = pd.concat(
        [pd.read_csv(
            f,
            parse_dates=['forecast_creation_date','scenario_date'],
            infer_datetime_format=True,
            ) for f in card_locs["scenario"]
        ],
        ignore_index=True,
    )

    poi_df = pd.concat(
        [pd.read_csv(f) for f in card_locs["poi"]],
        ignore_index=True,
    )

    observations_df = pd.concat(
        [pd.read_csv(
            f,
            dtype={'obs_value':float},
            ) for f in card_locs["observations"]
        ],
        ignore_index=True,
    )

    forecast_df = pd.concat(
        [pd.read_csv(
            f,
            dtype={'forecast_value':float},
            ) for f in card_locs["forecast"]
        ],
        ignore_index=True,
    )

    #Combine tables by type

    # scenario<---project
    scenario_proj_df    = scenario_df.merge(project_df, on='project_id', how='left')

    # observations <---poi
    observations_poi_df = observations_df.merge(poi_df, on='poi_id', how='left')

    # forecasts <---[observations+poi]<----[scenario+project]
    all_df = forecast_df.merge(
        observations_poi_df,
        on='forecast_match_id',
        how='left').merge(
            scenario_proj_df,
            on='run_id',
            how='left')

    return all_df
