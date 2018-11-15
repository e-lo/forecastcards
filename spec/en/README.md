# What are forecast cards?

Forecast cards are a simple data specification for storing key information about your travel forecast in order to:  
 - evaluate performance of a forecast over time,    
 - analyze the collective performance of forecasting systems and institutions over time, and 
 - identify contributing factors to high performing forecasts.  


## Overview of forecast cards

There four are types of Forecast Cards:
 - Points of Interest, such as a roadway segment or transit line,
 - Projects, such as a roadway expansion, an HOV designation,
 - Forecasts, which are predictions at the points of interest about what the project will do,
 - Observations, which are points of data used to evaluate the the forecasts
 
 Each "card" is a text-based CSV file.  
 
Forecast Cards are compatible with the [Open Knowledge Foundation's]() [Frictionless Data](http://frictionlessdata.io) [Tabular Data Package]( http://frictionlessdata.io/docs/tabular-data-package) format.

### Included Examples

Table Validity Status:  [![goodtables.io](https://goodtables.io/badge/github/e-lo/forecast-cards.svg)](https://goodtables.io/github/e-lo/forecast-cards)



### Suggested card naming and organization

In order to leverage a common set of tools, we suggest that forecast card data is stored in the following naming and folder structure:

`agency-name`-`project-id`-`project-short-name`/
   |---`README.md`
   |---`
   |---`project-<project-id>-<project-short-name>.csv`
   |---`poi-<project-id>.csv`
   |---`observations`/
   |   |---`observations-<date>.csv`
   |
   |---`forecasts`/
   |   |---`forecast-<scenario-id>-<scenario-year>-<forecast-creation>-<forecast-id>.csv`



## How do I start on my own?


## Making forecast cards publicly available

## Submitting forecast cards

## Getting Help

