#!/usr/bin/env python

import os
import sys
import forecastcards

USAGE = """
python forecastcards/scripts/validate_cardset.py  "/Users/elizabeth/Documents/urbanlabs/NCHRP 08-110/working/forecastcards/forecastcards/examples"
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        data_loc = "."
    else:
        data_loc = sys.argv[1]
    cardset = forecastcards.Cardset(data_loc = data_loc)
    if not cardset.invalid_projects :
        print("Cardset Valid!")
    else:
        print("Invalid Project: ",cardset.invalid_projects)
        print(cardset.failed_reports)
