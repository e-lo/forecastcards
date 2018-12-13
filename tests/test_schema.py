import os
import pytest
import forecastcards

@pytest.mark.master
@pytest.mark.basic
def test_github_schema():
    schema = forecastcards.Card_schema()
    assert(schema.valid == True)

if __name__ == '__main__':
    print ("test github schema")
    test_github_schema()
