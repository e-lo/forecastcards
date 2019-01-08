import csv
import glob
import os
import requests
from urllib.parse import urljoin
from goodtables import validate
import forecastcards

class Project:
    '''
    This class does some of the same things as the Cardset class, but
    is more efficient when you know the exact folder of the project.

    It is best used when you need to get the project ID of or
    validate a single project.
    '''

    github_example_data = {'username':'e-lo','repository':'forecastcards','branch':'master'}

    github_master_schema_loc = {
                'poi'         : "https://raw.github.com/e-lo/forecast-cards/master/spec/en/poi-schema.json",
                "scenario"    : "https://raw.github.com/e-lo/forecast-cards/master/spec/en/scenario-schema.json",
                "project"     : "https://raw.github.com/e-lo/forecast-cards/master/spec/en/project-schema.json",
                "observations": "https://raw.github.com/e-lo/forecast-cards/master/spec/en/observations-schema.json",
                "forecast"    : "https://raw.github.com/e-lo/forecast-cards/master/spec/en/forecast-schema.json",
                }

    fc_path = os.path.dirname(os.path.realpath(__file__))
    local_example_data_loc = os.path.join(fc_path,'examples')

    def __init__(self,
                 project_location = local_example_data_loc,
                 schemas = {},
                 schema_locs = github_master_schema_loc,
                 add_data    = True,
                 validate    = True,
                 compatable_cardsets = [], #cardset instances, locations
                ):

        self.project_location_valid(project_location)
        self.project_location    = project_location

        self.schema_locs         = schema_locs # dict by card type of urls to JSON files or schema instances
        self.compatable_cardsets = compatable_cardsets


        self.valid             = False
        self.validity_requires = ['project','poi','observations','scenario','forecast']
        self.fail_reports      = []

        self.card_locs_by_type = {'poi'         : [],
                                  'scenario'    : [],
                                  'observations': [],
                                  'forecast'    : [],
                                  'project'     : []}

        # get project id and check to make sure it doesn't conflict with other cardsets that should be compatible
        self.project_id = self.get_project_id(project_location)

        if compatable_cardsets:
            self.compatable = self.check_project_id(self.compatable_cardsets)

        if add_data: self.add_file_locations()

        if validate: self.validate_project()

    def project_location_valid(self,project_location):

        if not isinstance(project_location, dict) and not project_location.find('github')>=0:
            return os.path.exists(project_location)

        if not isinstance(project_location, dict):
            project_location = forecastcards.github_url_to_dict(project_location)

        repo_loc = forecastcards.api_github_url(project_location['username'],project_location['repository'],project_location['branch'])

        rj = requests.get(repo_loc).json()

        if len(rj['tree'])>1: return True
        return False

    def check_project_id(self, compatable_cardsets):
        '''
        check to see if project should be added
        :returns: True if project should be added; False if it shouldn't
        '''
        cs_with_project_id = []
        for cs in compatable_cardsets:
            if isinstance(cs, forecastcards.Cardset):
                if self.project_id in cs.projects:
                    cs_with_project_id.append(cs)
                    continue
            elif cs.find('github')>=0:
                cs = forecastcards.github_url_to_dict(cs)

            cs = forecastcards.Cardset(data_loc=cs_loc,validate=False)
            if self.project_id in cs.projects:
                cs_with_project_id.append(cs_loc_orig)

        if cs_with_project_id:
            print("Duplicate Project ID found in following cardsets:","\n".join(cs_with_project_id))
            return False
        else:
            return True

    def get_project_id(self, project_location):

        if isinstance(project_location, dict) or project_location.find('github')>=0:
            project_id = self.get_project_id_github(project_location)
        else:
            project_id = self.get_project_id_local(project_location)

        return project_id

    def get_project_id_local(self, project_location):
        for project_file in glob.iglob(os.path.join(project_location,'project*.csv')):
            with open(project_file, 'r') as f:
                proj_csv = list(csv.reader(f))

                assert(proj_csv[0][0] == 'project_id')
                project_id   = proj_csv[1][0].strip().lower()
                return project_id
        return None

    def get_project_id_github(self, project_location):
        if not isinstance(project_location, dict):
            project_location = forecastcards.github_url_to_dict(cs_loc)
        #print(project_location)
        repo_loc = forecastcards.api_github_url(project_location['username'],project_location['repository'],project_location['branch'])
        repo_raw = forecastcards.raw_github_url(project_location['username'],project_location['repository'],project_location['branch'])

        rj = requests.get(repo_loc).json()

        for file in rj['tree']:
            if project_location['subdir'] not in file['path']: continue
            if file['type']!='blob': continue

            path_list = file['path'].split("/")
            if path_list[-1][-4:].lower()==".csv" and path_list[-1][0:7].lower() == "project":
                proj_csv = list(forecastcards.get_csv_from_url(urljoin(repo_raw,file['path'])))
                #print(proj_csv)

                assert(proj_csv[0][0] == 'project_id')
                project_id   = proj_csv[1][0].strip().lower()
                return project_id
        return None

    def add_file_locations_github(self):
            if not isinstance(self.project_location, dict):
                project_location = forecastcards.github_url_to_dict(cs_loc)

            repo_loc = forecastcards.api_github_url(self.project_location['username'],self.project_location['repository'],self.project_location['branch'])
            repo_raw = forecastcards.raw_github_url(self.project_location['username'],self.project_location['repository'],self.project_location['branch'])

            rj = requests.get(repo_loc).json()
            for file in rj['tree']:
                if self.project_location['subdir'] not in file['path']: continue
                if file['type']!='blob': continue

                path_list = file['path'].split("/")

                if path_list[-1][-4:].lower()!=".csv": continue

                if path_list[-1][0:7].lower() == "project":
                    self.card_locs_by_type['project'].append(urljoin(repo_raw,file['path']))
                    #print("adding project:",file['path'])
                if path_list[-1][0:8].lower()=="scenario":
                    self.card_locs_by_type['scenario'].append(urljoin(repo_raw,file['path']))
                    #print("adding scenario:",file['path'])
                if path_list[-1][0:8].lower()=="forecast":
                    self.card_locs_by_type['forecast'].append(urljoin(repo_raw,file['path']))
                    #print("adding forecast:",file['path'])
                if path_list[-1][0:12].lower()=="observations":
                    self.card_locs_by_type['observations'].append(urljoin(repo_raw,file['path']))
                    #print("adding observation:",file['path'])
                if path_list[-1][0:3].lower()=="poi":
                    self.card_locs_by_type['poi'].append(urljoin(repo_raw,file['path']))
                    #print("adding poi:",file['path'])

    def add_file_locations_local(self):
        self.card_locs_by_type['poi']= glob.glob(os.path.join(self.project_location,'poi*.csv'),recursive=True)
        self.card_locs_by_type['scenario']= glob.glob(os.path.join(self.project_location,'scenario*.csv'),recursive=True)
        self.card_locs_by_type['observations']= glob.glob(os.path.join(self.project_location,'**/observations*.csv'),recursive=True)
        self.card_locs_by_type['forecast']= glob.glob(os.path.join(self.project_location,'**/forecast*.csv'),recursive=True)
        self.card_locs_by_type['project']= glob.glob(os.path.join(self.project_location,'project*.csv'),recursive=True)

    def add_file_locations(self):
        if isinstance(self.project_location, dict) or self.project_location.find('github')>=0:
            self.add_file_locations_github()
        else:
            self.add_file_locations_local()

    def validate_project(self, schema_locs=None, validity_requires=None):
        if not schema_locs:
            schema_locs = self.schema_locs

        if not validity_requires:
            validity_requires = self.validity_requires

        ## todo validate against local schemas
        valid        = True
        fail_reports = []

        for card_type, locs in self.card_locs_by_type.items():
            #print ("validating",card_type, locs)
            if not locs and card_type in validity_requires:
                valid = False
                fail_reports.append("MISSING REQUIRED CARD TYPE: "+card_type)
            ##todo add other validation checks here
            for card in locs:
                report = validate(card ,schema=requests.get(schema_locs[card_type]).json())
                if not report['valid']:
                    if card_type in validity_requires:
                        valid = False
                    print ("Validation Error:", card)
                    fail_reports.append(report)
                                # check that start time is before end time
                if card_type in ['forecast','observation']:
                    df=pd.read_csv(card,
                                   dtype={'obs_value':float},
                                   usecols=["start_time", "end_time"],
                                   parse_dates=["start_time", "end_time"])
                    df['invalid']=df['start_time']>=df['end_time']
                    if df['invalid'].sum()>0:
                        valid = False
                        report = card+ " - Start time isn't before end time."+str(df[df['invalid'] == True])
                        fail_reports.append(report)


        self.valid = valid
        self.fail_reports = fail_reports
