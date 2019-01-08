import os
import sys
import forecastcards

USAGE = """
python forecastcards/scripts/validate_project.py  "/Users/elizabeth/Documents/urbanlabs/NCHRP 08-110/working/forecastcards/forecastcards/examples/ecdot-lu123-munchkin_tod"
"""

if __name__ == "__main__":
    project = forecastcards.Project(project_location = sys.argv[1])
    print("Card Locations:",project.card_locs_by_type)
    if project.valid:
        print("Project Valid:",project.project_id)
    else:
        print("Invalid Project: ",project.project_id)
        print(project.fail_reports)
