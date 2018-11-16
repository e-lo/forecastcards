# What are forecast cards?

Forecast cards are a simple data specification for storing key information about your travel forecast in order to:  
 - evaluate performance of a forecast over time,    
 - analyze the collective performance of forecasting systems and institutions over time, and 
 - identify contributing factors to high performing forecasts.  


## Overview of forecast cards

There four are types of Forecast Cards:
 - Points of Interest, such as a roadway segment or transit line,
 - Projects, such as a roadway expansion, an HOV designation,
 - Scenarios or runs, including information about the forecasting system
 - Forecasts, which are predictions at the points of interest about what the project will do,
 - Observations, which are points of data used to evaluate the the forecasts
 
Each "card" is a text-based CSV file.  
 
### The Schema

![entity relationship diagram](spec/en/forecast-cards-erd.png?raw=true "Forecast Cards Schema Entity Relationship Diagram..slightly out of date")

Forecast Cards are compatible with the [Open Knowledge Foundation's]() [Frictionless Data](http://frictionlessdata.io) [Table Schema]( https://github.com/frictionlessdata/specs/blob/master/specs/table-schema.md) specification.


### Included Examples

This project currently includes one example, which is the Emerald City DOT's HOV expansion for the Yellow Brick Road, which is contained in `examples/emeraldcitydot-rx123-yellowbrickroadhov`

This example can be analyzed and run with the `notebooks` folder of this directory and can be run using [binder](http://www.mybinder.org) or [colaboratory](https://colab.research.google.com).

Table Validity Status:  [![goodtables.io](https://goodtables.io/badge/github/e-lo/forecast-cards.svg)](https://goodtables.io/github/e-lo/forecast-cards)

### Suggested card naming and organization

In order to leverage a common set of tools, we suggest that forecast card data is stored in the following naming and folder structure:

    agency-name-project-id-project-short-name/
       |---README.md
       |---
       |---project-<project-id>-<project-short-name>.csv
       |---scenarios-<project-id>.csv
       |---poi-<project-id>.csv
       |---observations/
       |   |---observations-<date>.csv
       |
       |---forecasts/
       |   |---forecast-<scenario-id>-<scenario-year>-<forecast-creation>-<forecast-id>.csv

## How do I start on my own?

## Making forecast cards publicly available

## Submitting forecast cards

## Getting Help

