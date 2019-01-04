import os
import pytest
import forecastcards

fc_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ex_data = os.path.join(os.path.join(fc_path,'forecastcards'),'examples')

gh_data = {'username':'e-lo','repository':'forecastcards','branch':'master'}

schema_locs = { 'poi':'https://raw.github.com/e-lo/forecastcards/master/spec/en/poi-schema.json',
                "scenario": "https://raw.github.com/e-lo/forecastcards/master/spec/en/scenario-schema.json",
                "project": "https://raw.github.com/e-lo/forecastcards/master/spec/en/project-schema.json",
                "observations": "https://raw.github.com/e-lo/forecastcards/master/spec/en/observations-schema.json",
                "forecast": "https://raw.github.com/e-lo/forecastcards/master/spec/en/forecast-schema.json",
}

valid_project_control = set(['lu123','rx123'])

@pytest.mark.master
@pytest.mark.basic
def test_local_cardset():
    #forecastcards.Cardset(data_loc = ex_data)
    cardset = forecastcards.Cardset()
    assert(valid_project_control == set(cardset.validated_projects))

@pytest.mark.master
@pytest.mark.basic
def test_github_cardset():
    cardset = forecastcards.Cardset(data_loc = gh_data)
    assert(valid_project_control == set(cardset.validated_projects))

@pytest.mark.master
def test_github_add_local_cardset():
    cardset = forecastcards.Cardset(data_loc = gh_data, exclude_projects=['lu123'])
    cardset.add_projects(data_loc=ex_data, select_projects=['lu123'])
    assert(valid_project_control == set(cardset.validated_projects))

@pytest.mark.master
def test_local_add_github_cardset():
    cardset = forecastcards.Cardset(data_loc = ex_data, exclude_projects=['lu123'])
    cardset.add_projects(data_loc=gh_data, select_projects=['lu123'])
    assert(valid_project_control == set(cardset.validated_projects))

if __name__ == '__main__':

    print ("test default")
    test_local_cardset()
    print ("test github")
    test_github_cardset()
    print ("test github add local")
    test_github_add_local_cardset()
    print ("test local add github")
    test_local_add_github_cardset()
