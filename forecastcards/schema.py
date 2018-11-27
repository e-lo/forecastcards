from urllib.parse import urljoin
from tableschema import Schema
from graphviz import Digraph

default_schema_url = 'https://raw.github.com/e-lo/forecast-cards/master/spec/en'

default_schema_parts = {
    "poi": "poi-schema.json",
    "scenario": "scenario-schema.json",
    "project": "project-schema.json",
    "observations": "observations-schema.json",
    "forecast": "forecast-schema.json",
}

default_relationships = [
        ("poi:poi_id", "observations:poi_id"),
        ("observations:forecast_id","forecast:forecast_id"),
        ("scenario:run_id","forecast:run_id"),
        ("project:project_id","scenario:project_id"),
]

def validate_schemas(url_loc = default_schema_url, schema_parts = default_schema_parts):
    '''
    url_loc
      url location of collection of valid json files that define the schema
    schema_parts
      dictionary of <schema part name>:<filename>
      
    If schema doesn't validate, clean your JSON with https://jsonlint.com/ 
    '''
    schema_locs = { k: urljoin(url_loc,v) for k,v in schema_parts.items() }
    schemas_dict = {}
    for k,v in schemas_loc.items():
        print ("Obtaining ", k,"schema from: ",v)
        schemas_dict[k] = Schema(v)
    return schemas_dict
    
def schema_erd_graph(schemas_dict,relationships=default_relationships):
    erd_graph = Digraph(name='Schemas', node_attr={'shape': 'plain'})

    for k,v in schemas.items():
      node_label="<<table border='0' cellborder='1' cellspacing='0'>"
      node_label+="<tr><td><b>"
      node_label+=str(k)
      node_label+="</b></td></tr>"
      for f in v.descriptor['fields']:
        node_label+="<tr><td port='"
        node_label+=f['name']
        node_label+="'>"
        node_label+=f['name']
        node_label+="</td></tr>"
      node_label+="</table>>"
      erd_graph.node(k,label = node_label)
    
    if relationships:
        for i,j in relationships:
            erd_graph.edge(
        erd_graph.edge(i,j)

    return: erd_graph     
    
def relationship_graph():
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
