import pytest
import forecastcards

def test_schema_validate():
    forecastcards.validate_schemas()

def test_make_erd_graph():
    forecastcards.make_erd_graph(forecastcards.validate_schemas())

def test_relationship_graph():
    forecastcards.relationship_graph()

def test_map_cards():
    d = forecastcards.map_cards()
    for k,v in d.items():
        assert len(v)>0

card_locs = {
       "poi": ['https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/poi-rx123.csv'],
       "scenario": ['https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/scenarios-rx123.csv'],
       "project": ['https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/project-rx123.csv'],
       "observations": ['https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/observations/observations-1935.csv',
                        'https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/observations/observations-1960.csv',
       ],
       "forecast": ['https://raw.github.com/e-lo/forecast-cards/master/forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov/forecasts/forecast-A1-1960-1940-F1.csv'],
}

schema_locs = { 'poi':'https://raw.github.com/e-lo/forecast-cards/master/spec/en/poi-schema.json',
                "scenario": "https://raw.github.com/e-lo/forecast-cards/master/spec/en/scenario-schema.json",
                "project": "https://raw.github.com/e-lo/forecast-cards/master/spec/en/project-schema.json",
                "observations": "https://raw.github.com/e-lo/forecast-cards/master/spec/en/observations-schema.json",
                "forecast": "https://raw.github.com/e-lo/forecast-cards/master/spec/en/forecast-schema.json",
}

def test_validate_cards():
    forecastcards.validate_cards(card_locs,schema_locs)

def test_combine_data():
    forecastcards.combine_data(card_locs)

## TODO
#def test_fix_missing():
#    forecastcards.fix_missing_values(all_df)
