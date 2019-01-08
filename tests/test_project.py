import os
import pytest
import forecastcards

fc_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ex_project = os.path.join(os.path.join(fc_path,'forecastcards'),'examples','ecdot-lu123-munchkin_tod')

gh_project = {'username':'e-lo','repository':'forecastcards','branch':'master','subdir':'examples/ecdot-rx123-ybr_hov'}

schema_locs = { 'poi':'https://raw.github.com/e-lo/forecastcards/master/spec/en/poi-schema.json',
                "scenario": "https://raw.github.com/e-lo/forecastcards/master/spec/en/scenario-schema.json",
                "project": "https://raw.github.com/e-lo/forecastcards/master/spec/en/project-schema.json",
                "observations": "https://raw.github.com/e-lo/forecastcards/master/spec/en/observations-schema.json",
                "forecast": "https://raw.github.com/e-lo/forecastcards/master/spec/en/forecast-schema.json",
}

@pytest.mark.master
@pytest.mark.basic
def test_local_project():
    project            = forecastcards.Project(project_location= ex_project)
    assert(project.valid == True)

@pytest.mark.master
@pytest.mark.basic
def test_github_project():
    project            = forecastcards.Project(project_location = gh_project)
    assert(project.valid == True)

if __name__ == '__main__':

    print ("test local project")
    test_local_project()
    print ("test github project")
    test_github_project()
