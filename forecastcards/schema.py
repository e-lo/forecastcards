import traceback
from urllib.parse import urljoin
from tableschema import Schema
from graphviz import Digraph
import forecastcards

class Card_schema:
    github_master_schema_loc = {'username':'e-lo','repository':'forecastcards','branch':'master','subdir':'spec/en/'}

    master_schema_parts = {
        "poi"          : "poi-schema.json",
        "scenario"     : "scenario-schema.json",
        "project"      : "project-schema.json",
        "observations" : "observations-schema.json",
        "forecast"     : "forecast-schema.json",
    }

    master_relationships = [
        ("poi:poi_id", "observations:poi_id"),
        ("observations:forecast_match_id","forecast:forecast_match_id"),
        ("scenario:run_id","forecast:run_id"),
        ("project:project_id","scenario:project_id"),
    ]

    def __init__(self, schema_dir = github_master_schema_loc, schema_parts = master_schema_parts, relationships = master_relationships, validate=True):

        self.schema_parts = schema_parts
        self.schema_dir   = schema_dir
        self.relationships = relationships
        self.valid        = False
        self.schema_locs = {}
        self.schema_dict = None

        if type(self.schema_dir) is dict:
            self.schema_locs = self.schema_locs_from_github()
        else:
            "Local schemas not implemented"
            ### TODO: implement local schemas_locs
            raise()

        if validate:
            self.schema_dict = self.validate_schemas(schema_locs = self.schema_locs, schema_parts=self.schema_parts)


    def schema_locs_from_github(self, schema_dir=None, schema_parts=None):

        if not schema_dir: schema_dir= self.schema_dir
        if not schema_parts: schema_parts = self.schema_parts

        url_loc = forecastcards.raw_github_url(
            schema_dir['username'],
            schema_dir['repository'],
            branch = schema_dir['branch'],
            subdir = schema_dir['subdir']
            )

        schema_locs = { k: urljoin(url_loc,v) for k, v in schema_parts.items() }
        return schema_locs

    def validate_schemas(self, schema_locs = None, schema_parts = None, verbose=False):
        '''
        :param schema_locs: dictionary of locations by schema schema_parts
        :type schema_locs: dict
        :param schema_parts: dicionary <schema part name>:<filename>
        :type schema_parts: dict
        :returns: dictionary schema instances

        Troubleshooting
            If schema doesn't validate, clean your JSON with https://jsonlint.com/
        '''

        if not schema_locs:  schema_locs = self.schema_locs
        if not schema_parts: schema_parts = self.schema_parts

        schema_dict = {}
        for k,v in schema_locs.items():
            if verbose: print ("Obtaining ", k,"schema from: ",v)
            try:
                schema_dict[k] = Schema(v)
                if verbose: print("Schema",k,"valid.")
            except Exception:
                traceback.print_exc()

        if len(schema_locs)==len(schema_dict):
            self.valid = True
            print ("Schema valid")
            return schema_dict
        else:
            return None

    def make_erd_graph(self):

        erd_graph = Digraph(name='Schemas', node_attr={'shape': 'plain'})

        for k,v in self.schemas_dict.items():
          node_label="<<table  border='0' cellborder='1' cellspacing='0'>"
          node_label+="<tr><td BGCOLOR='dodgerblue'><FONT point-size='16' FACE='lato'><b>"
          node_label+=str(k)
          node_label+="</b></FONT></td></tr>"
          for f in v.descriptor['fields']:
            node_label+="<tr ><td port='"
            node_label+=f['name']
            node_label+="'>"
            if 'constraints' in f.keys():
              if 'required' in f['constraints'].keys():
                if f['constraints']['required']==True:
                  node_label+="<b><FONT COLOR='firebrick' FACE='courier'>"+f['name']+"*</FONT></b>"
                else:
                  node_label+="<b><FONT COLOR='grey14' FACE='courier'>"+f['name']+"</FONT></b>"
              else:
                  node_label+="<b><FONT COLOR='grey14' FACE='courier'>"+f['name']+"</FONT></b>"
            else:
              node_label+="<b><FONT COLOR='grey14' FACE='courier'>"+f['name']+"</FONT></b>"

            if 'description' in f.keys():
              node_label+="<br/>"
              node_label+=f['description']
            if 'constraints' in f.keys():
              if 'enum' in f['constraints'].keys():
                node_label+="<br/>"
                node_label+="<FONT point-size = '8'>One of:</FONT><FONT point-size = '8' COLOR='dodgerblue3' FACE='courier'>"+", ".join(f['constraints']["enum"])+"</FONT>"
            node_label+="</td></tr>"
          node_label+="</table>>"
          erd_graph.node(k,label = node_label)

        if self.relationships:
            for i,j in relationships:
                    erd_graph.edge(i,j)


        return erd_graph

    def relationship_graph(self):
        g = Digraph('G')
        g.attr(bgcolor='cadetblue', label='Project P\nproject_roadabc.csv', fontcolor='white')

        with g.subgraph(name='cluster1') as c1:
            c1.attr(fillcolor='white', label='Opening Year Scenario', fontcolor='black',
                   style='filled')
            with c1.subgraph(name='cluster11') as c11:
                c11.attr(fillcolor='white', label='Forecast Run 2\nforecast-buildA1-1998-1988-f2.csv', fontcolor='black',
                       style='filled')
                c11.attr('node', shape='circle',style='filled')
                c11.node('a1node1',label="poi 1\n33,210", fillcolor='crimson')
                c11.node('a2node1',label="poi 2\n22,110", fillcolor='darkorange')

            with c1.subgraph(name='cluster12') as c12:
                c12.attr(fillcolor='white', label='Forecast Run 4\nforecast-buildA1-1998-1988-f4.csv', fontcolor='black',
                       style='filled')
                c12.attr('node', shape='circle',style='filled')
                c12.node('a1node2',label="poi 1\n33,220", fillcolor='crimson')
                c12.node('a2node2',label="poi 2\n22,210", fillcolor='darkorange')

        with g.subgraph(name='cluster2') as c2:
            c2.attr(fillcolor='white', label='Horizon Scenario A2\n', fontcolor='black',
                  style='filled')

            with c2.subgraph(name='cluster21') as c21:
                c21.attr(fillcolor='white', label='Forecast Run 12\nforecast-buildA2-2018-1988-f12.csv', fontcolor='black',
                       style='filled')
                c21.attr('node', shape='circle',style='filled')
                c21.node('b1node1',label="poi 1\n55,451",fillcolor='seagreen')
                c21.node('b2node1',label="poi 2\n47,250",fillcolor='cornflowerblue')

            with c2.subgraph(name='cluster22') as c22:
                c22.attr(fillcolor='white', label='Forecast Run 15\nforecast-buildA2-2018-1988-f15.csv', fontcolor='black',
                       style='filled')
                c22.attr('node', shape='circle',style='filled')
                c22.node('b1node2',label="poi 1\n55,433",fillcolor='seagreen')
                c22.node('b2node2',label="poi 2\n47,350",fillcolor='cornflowerblue')

        with g.subgraph(name='cluster3') as c3:
            c3.attr(fillcolor='white', label='Opening Year Observations\nobservations-1998-10-11.csv', fontcolor='black',
                   style='filled')
            c3.attr('node', shape='circle',style='filled')
            c3.node('c1node',label="poi 1\n22,450",fillcolor='crimson')
            c3.node('c2node',label="poi 2\n14,450",fillcolor='darkorange')

        with g.subgraph(name='cluster4') as c4:
            c4.attr(fillcolor='white', label='Horizon Year Observations\nobservations-2018-09-10.csv', fontcolor='black',
                   style='filled')
            c4.attr('node', shape='circle',style='filled')
            c4.node('d1node',label='poi 1\n44,555',fillcolor='seagreen')
            c4.node('d2node',label='poi 1\n49,555',fillcolor='cornflowerblue')
        return g
