
import requests
import pandas as pd
from goodtables import validate


default_repo_api = "https://api.github.com/repos/e-lo/forecast-cards/git/trees/f35185168b238429157adcbf5ba09d09ae7d0172?recursive=1"
default_subdirs  = ["examples"]

default_recode_na_vars   = ['forecast_system_type', 'area_type', 'forecaster_type', 'state', 'agency', 'functional_class','facility_type','project_type']
default_no_na_vars       = ['scenario_date','forecast_creation_date','forecast_value','obs_value']
default_required_vars    = default_recode_na_vars + default_no_na_vars
default_categorical_cols = ['project_size','creation_decade','scenario_decade','functional_class','forecast_system_type','project_type','agency','forecaster_type','area_type','facility_type','state']


def map_cards(repo_loc=default_repo_api,subdirs=default_subdirs):
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
    card_locs
      dictionary of card type: list of files
    schemas_loc
      dictionary of card type: schema locations
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


def fix_missing_values(all_df,recode_na_vars=default_recode_na_vars,no_na_vars=default_no_na_vars):
    '''
    Recode missing variables in ``recode_na_vars`` list as 'missing'.
    Delete records that have a missing ``no_na_vars``.
    Returns recoded/cleaned dataframe.
    '''
    all_df[recode_na_vars].fillna('missing')

    usable_df = all_df.dropna(subset=no_na_vars)

    print("Kept",len(usable_df),"of",len(all_df))

    return usable_df

def create_default_categorical_vars(df):
    ## categorical decades variable
    df['creation_decade'] = (df['forecast_creation_date'].apply(lambda x: x.year//10*10)).astype('category')
    df['scenario_decade'] = (df['scenario_date'].apply(lambda x: x.year//10*10)).astype('category')

    ## large projects dummy variable
    breakpoint = 30000
    bins = [df['forecast_value'].min(), breakpoint, breakpoint+usable_df['forecast_value'].max()]
    labels = ["small_project","large_project"]
    df['project_size'] = pd.cut(usable_df['forecast_value'], bins=bins, labels=labels)

    return df


def categorical_to_dummy(df, categorical_cols_list=default_categorical_cols,required_vars = default_required_vars):
    dummy_df = pd.get_dummies(df[categorical_cols])

    dummied_df = pd.concat([df[[v for v in required_vars if v not in categorical_cols]],dummy_df],axis=1)
    return dummied_df

def default_data_clean(df):
    df = fix_missing_values(df)
    df = create_default_categorical_vars(df)
    df = categorical_to_dummy(df)
    return df
