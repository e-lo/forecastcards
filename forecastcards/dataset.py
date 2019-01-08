import requests
from urllib.parse import urljoin
import pandas as pd
from goodtables import validate
import forecastcards

class Dataset:
    default_recode_na_vars   = ['forecast_system_type', 'area_type', 'forecaster_type', 'state', 'agency', 'functional_class','facility_type','project_type']
    default_no_na_vars       = ['scenario_date','forecast_creation_date','forecast_value','obs_value']

    default_required_vars    = default_recode_na_vars + default_no_na_vars

    default_categorical_cols = ['project_size','creation_decade','scenario_decade','functional_class','forecast_system_type','project_type','agency','forecaster_type','area_type','facility_type','state']
    default_no_scale_cols    = ['scenario_date','forecast_creation_date','forecast_value','obs_value']

    def __init__(
                 self,
                 card_locs_by_type  = None,
                 file_to_project_id = None,
                 default_process  = True,
                 recode_na_vars   = default_recode_na_vars,
                 no_na_vars       = default_no_na_vars,
                 required_vars    = default_required_vars,
                 categorical_cols = default_categorical_cols,
                 no_scale_cols    = default_no_scale_cols
                 ):

        self.card_locs_by_type = card_locs_by_type
        self.all_df    = None

        if card_locs_by_type and file_to_project_id:
            self.all_df       = self.combine_data(card_locs_by_type, file_to_project_id)

        self.recode_na_vars   = recode_na_vars
        self.no_na_vars       = no_na_vars
        self.required_vars    = required_vars
        self.categorical_cols = categorical_cols
        self.no_scale_cols    = no_scale_cols

        self.df = None
        if default_process and card_locs_by_type and file_to_project_id:
            self.df = self.default_data_clean(self.all_df)

    def combine_data(self, card_locs_by_type, file_to_project_id):
        '''
        Combine tables by card type and merge tables on keys.
        '''
        print("Combining data")
        ## TODO need to add project_id to each table.
        #Combine tables by type

        project_df = pd.concat(
            [pd.read_csv(
                f,
                parse_dates=['year_open_planned','year_horizon','date_open_actual'],
                infer_datetime_format=True,
                ) for f in card_locs_by_type["project"]
            ],
            ignore_index=True,
        )

        scenario_df = pd.concat(
            [pd.read_csv(
                f,
                parse_dates=['forecast_creation_date','scenario_date'],
                infer_datetime_format=True,
                ) for f in card_locs_by_type["scenario"]
            ],
            ignore_index=True,
        )

        poi_df = pd.concat(
            [pd.read_csv(f).assign(project_id=file_to_project_id[f]) for f in card_locs_by_type["poi"]],
            ignore_index=True,
        )

        observations_df = pd.concat(
            [pd.read_csv(
                f,
                dtype={'obs_value':float},
                ).assign(project_id=file_to_project_id[f]) for f in card_locs_by_type["observations"]
            ],
            ignore_index=True,
        )

        forecast_df = pd.concat(
            [pd.read_csv(
                f,
                dtype={'forecast_value':float},
                ).assign(project_id=file_to_project_id[f]) for f in card_locs_by_type["forecast"]
            ],
            ignore_index=True,
        )

        #Combine tables by type

        # scenario<---project
        scenario_proj_df    = scenario_df.merge(project_df, on='project_id', how='left')
        #print("scenario_proj_df shape:",scenario_proj_df.shape )


        # observations <---poi
        observations_poi_df = observations_df.merge(poi_df, on=['project_id','poi_id'], how='left')
        #print("observations_poi_df shape:",observations_poi_df.shape )
        #print(observations_poi_df[['project_id','poi_id','obs_id','forecast_match_id']])
        # forecasts <---[observations+poi]<----[scenario+project]
        all_df = forecast_df.merge(
            observations_poi_df,
            on=['project_id','forecast_match_id'],
            how='left').merge(
                scenario_proj_df,
                on=['project_id','run_id'],
                how='left')
        #print(all_df[['project_id','run_id','forecast_match_id']])

        return all_df


    def fix_missing_values(self,all_df,recode_na_vars=[],no_na_vars=[]):
        '''
        Recode missing variables in ``recode_na_vars`` list as 'missing'.
        Delete records that have a missing ``no_na_vars``.
        Returns recoded/cleaned dataframe.
        '''
        if not recode_na_vars:
            recode_na_vars = self.recode_na_vars

        if not no_na_vars:
            no_na_vars = self.no_na_vars

        all_df[recode_na_vars].fillna('missing')

        usable_df = all_df.dropna(subset=no_na_vars)

        print("Kept",len(usable_df),"of",len(all_df))

        return usable_df

    def create_daily_volumes(self,row):

        ##TODO this is a simplification. Should be doing more robust checks.
        if (not row['start_time']) or (not row['end_time']):
            return row['forecast_value']

        adt = forecastcards.convert_vol_to_daily(row['forecast_value'], row['start_time'], row['end_time'])

        return adt

    def create_default_categorical_vars(self, df):
        ## categorical decades variable
        df['creation_decade'] = (df['forecast_creation_date'].apply(lambda x: x.year//10*10)).astype('category')
        df['scenario_decade'] = (df['scenario_date'].apply(lambda x: x.year//10*10)).astype('category')

        ## large projects dummy variable
        breakpoint = 30000
        df['daily_forecast_value']=df.apply(self.create_daily_volumes,axis=1)
        print(df[['start_time','end_time','forecast_value','daily_forecast_value']])
        bins = [df['daily_forecast_value'].min(), breakpoint, breakpoint+df['daily_forecast_value'].max()]
        labels = ["small_project","large_project"]
        df['project_size'] = pd.cut(df['forecast_value'], bins=bins, labels=labels)

        return df

    def categorical_to_dummy(self, df, categorical_cols=[],required_vars = []):

        if not required_vars: required_vars = self.required_vars
        if not categorical_cols: categorical_cols = self.categorical_cols

        dummy_df = pd.get_dummies(df[categorical_cols])

        dummied_df = pd.concat([df[[v for v in required_vars if v not in categorical_cols]],dummy_df],axis=1)
        return dummied_df

    def scale_dummies_by_forecast_value(self, df, no_scale_cols=[]):

        if not no_scale_cols: no_scale_cols = self.no_scale_cols

        scale_cols_df = df.drop(no_scale_cols, axis=1).mul(df['forecast_value'], axis=0)
        scaled_df     = pd.concat([scale_cols_df,df[no_scale_cols]],axis=1)
        return scaled_df

    def default_data_clean( self,
                            df,
                            recode_na_vars   = [],
                            no_na_vars       = [],
                            required_vars    = [],
                            categorical_cols = [],
                            no_scale_cols    = []):

        # add in defaults b/c can't reference 'self' in method args
        if not recode_na_vars: recode_na_vars = self.recode_na_vars
        if not no_na_vars: no_na_vars = self.no_na_vars
        if not required_vars: required_vars = self.required_vars
        if not categorical_cols: categorical_cols = self.categorical_cols
        if not no_scale_cols: no_scale_cols = self.no_scale_cols

        print("Fix Missing Values")
        df = self.fix_missing_values(df, recode_na_vars  = recode_na_vars, no_na_vars = no_na_vars)
        print("Creating default categorical variables")
        df = self.create_default_categorical_vars(df)
        df = self.categorical_to_dummy(df, categorical_cols = categorical_cols, required_vars = required_vars)
        print("Scaling dummy variables by forecast value")
        df = self.scale_dummies_by_forecast_value(df, no_scale_cols = no_scale_cols)
        return df
