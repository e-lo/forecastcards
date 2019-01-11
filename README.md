[![Build Status](https://travis-ci.org/e-lo/forecastcards.svg?branch=master)](https://travis-ci.org/e-lo/forecastcards)

# What are forecast cards?

Forecast cards are a simple data specification for storing key information about your travel forecast in order to:  
 - evaluate performance of a forecast over time,    
 - analyze the collective performance of forecasting systems and institutions over time, and
 - identify contributing factors to high performing forecasts.  


## Overview of forecast cards

There five are types of Forecast Cards:
 - Points of Interest, such as a roadway segment or transit line,
 - Projects, such as a roadway expansion, an HOV designation,
 - Scenarios or runs, including information about the forecasting system
 - Forecasts, which are predictions at the points of interest about what the project will do,
 - Observations, which are points of data used to evaluate the the forecasts

Each "card" is a text-based CSV file.  

The forecastcards Python library is designed to validate and organize
data that conforms to the forecast cards data schema and consists of four main classes:   
 1. Cardset: a set of forecast data projects that conforms to the forecastcards data schema
 2. Dataset: turns a cardset into a [pandas](https://pandas.pydata.org/) dataset suitable for estimation purposes
 3. Project: to validate single projects (much of the same functionality as Cardset)
 4. Schema: to manage and validate the data schemas

### Basic Usage

**Validate Single Project**

```shell
validate_project.py  "forecastcards/examples/ecdot-lu123-munchkin_tod"
```

**Project**

```python

import forecastcards

# project locations can either be
#  - a dictionary describing a github location,
#  - a local directory, or
#  - a github web address.

gh_project = {'username':'e-lo',
              'repository':'forecastcards',
              'branch':'master',
              'subdir':'examples/ecdot-rx123-ybr_hov'}

# load project and validate using default data schema
project = forecastcards.Project(project_location = gh_project)

# check if project is valid
project.valid
```
**Cardset**

```python

import forecastcards

# project locations can either be
#  - a dictionary describing a github location or
#  - a local directory

gh_data = {'username':'e-lo',
              'repository':'forecastcards',
              'branch':'master',
              'subdir':'examples'}

# cardset walks through a directory, finds projects, and validates them
# according to the right schema.

# projects can be excluded or explicitly selected using keyword options
cardset = forecastcards.Cardset(data_loc = gh_data, exclude_projects=['lu123'])
cardset.add_projects(data_loc=ex_data, select_projects=['lu123'])
```

**Dataset**  
Create a dataset suitable for estimating quantile regressions. 

```python

import forecastcards

# project locations can either be
#  - a dictionary describing a github location or
#  - a local directory

gh_data = {'username':'e-lo',
              'repository':'forecastcards',
              'branch':'master',
              'subdir':'examples'}

cardset = forecastcards.Cardset(data_loc = gh_data)
dataset = forecastcards.Dataset(card_locs_by_type  = cardset.card_locs_by_type,
                                file_to_project_id = cardset.file_to_project_id )

# access to the dataframe
dataset.df
```


### The Schema

![entity relationship diagram](spec/en/forecast-cards-erd.png?raw=true "Forecast Cards Schema Entity Relationship Diagram")

![Overview of data relationships](spec/en/forecast-cards-rg.png?raw=true "Forecast Cards Data Relationships")

Forecast Cards are compatible with the [Open Knowledge Foundation's]() [Frictionless Data](http://frictionlessdata.io) [Table Schema]( https://github.com/frictionlessdata/specs/blob/master/specs/table-schema.md) specification.

Explore the data schema from your web browser using [colaboratory](https://colab.research.google.com):

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Explore_Data_Schemas.ipynb)

### Included Examples

This project currently includes one example, which is the Emerald City DOT's HOV expansion for the Yellow Brick Road, which is contained in `forecastcards/examples/emeraldcitydot-rx123-yellowbrickroadhov`

This example can be analyzed and run with the `notebooks` folder of this directory and can be run using [binder](http://www.mybinder.org) or [colaboratory](https://colab.research.google.com).

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Estimate_Quantiles.ipynb)

Table Validity Status:  [![goodtables.io](https://goodtables.io/badge/github/e-lo/forecast-cards.svg)](https://goodtables.io/github/e-lo/forecastcards)

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

1. Make sure you have the required data by examining the schema.

2. Create or Format Data as Forecast Cards

 - Enter data into browser and download: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Create_Forecast_Cards.ipynb)

 - Use [csv templates](https://github.com/e-lo/forecastcards/tree/master/forecastcards/template/) and enter data using a text browser or a spreadsheet application

 - Convert existing data using the [helper scripts on the way](https://github.com/e-lo/forecastcards/issues/1)*

3. Use template notebooks locally or on a hosted remote server (i.e. colaboratory) to clean data and estimate quantile regressions.  


## Installing forecastcards

Note: If you don't want to install forecastcards locally, you can run the code
notebooks in the cloud using Google Colab.

### Requirements
Forecast cards requires Python 3.6 or higher and it is recommended that
you install it in a virtual environment (i.e. [Conda](https://conda.io/docs/)).

### Installing
You can install forecastcards from this github repository using pip:  
`pip install --upgrade git+https://github.com/e-lo/forecastcards.git@master#egg=forecastcards`

If you plan to make changes, you can clone this git repository install
from your local, cloned directory  using pip:
`pip install --upgrade .`

### Troubleshooting
For people using a newer version of MacOS, they may have trouble installing one of the dependencies because its setuplpy settings are not up to date. You can successfully install it by overriding the default compiler using:

`CFLAGS='-stdlib=libc++' pip install cchardet`

## Suggested Workflow

### Initial setup
 - decide where your data will live: local file server or github repository
 - catalog and convert historic data

### Starting a new project

Use the Create_Forecast_Cards notebook locally, or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Create_Forecast_Cards.ipynb)

You can also just use the templates:

1. Copy the folder from `\template` folder in the `forecastcards` package to your folder for holding all the project forecastcards.  
2. Rename project folder according to schema, taking care to not duplicate any - roject IDs within your analysis scope (usually your agency of the [forecastcarddata store](https://github.com/e-lo/forecastcarddata)).  
3. Add observations, POIs, forecast runs, and forecasts for specific POIs as they are determined or created.  
4. Confirm data in new project conforms to data schema by running `validate_project.py  <project_directory>` or for all the projects in a directory by running `validate_cardset.py` from that directory or `validate_project.py  <cardset_directory>`

### Adding a forecast to an existing project

Use the Create_Forecast_Cards notebook locally, or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Create_Forecast_Cards.ipynb)

You can also just use the templates from `\template` folder:

1. add a new forecast csv file with relevant data for points of interest  
2. add an entry to scenario csv file about the model run  
3. Add any additional points of interest to poi csv file  
4. Confirm new data in project conforms to data schema by running `validate_project.py  <project_directory>` or for all the projects in a directory by running `validate_cardset.py` from that directory or `validate_project.py  <cardset_directory>`

### Adding observed data to existing project

Use the Create_Forecast_Cards notebook locally, or [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Create_Forecast_Cards.ipynb)

You can also just use the templates from `\template` folder:
1. Add a new observations csv  
2. Confirm new data in project conforms to data schema by running `validate_project.py  <project_directory>` or for all the projects in a directory by running `validate_cardset.py` from that directory or `validate_project.py  <cardset_directory>`   

### Run analysis

As summarized in [![the Estimate_Quantiles.ipynb notebook](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/e-lo/forecastcards/blob/master/forecastcards/notebooks/Estimate_Quantiles.ipynb)

1. Select cards to use  
2. Clean and merge cards  
3. Create any additional categorical variables  
4. Perform regressions  

# Making forecast cards publicly available

There are three likely options for making your data available:
1. Github (not great for extremely large datasets)
2. Amazon S3 / Microsoft Azure / Google Cloud (functionality coming soon)
3. Other agency-hosted web services (i.e. Socrata, webserver, etc.)

## Submitting forecast cards to community data store

You can submit forecast cards to the [community data store](https://github.com/e-lo/forecastcardsdata) by:

1. submitting a [pull-request to the forecastcardsdata repository](https://github.com/e-lo/forecastcardsdata/pulls)
2. submitting [an issue](https://github.com/e-lo/forecastcardsdata/issues) with a link to the location of the data along with permission to host it on the repository.
3. set up the public data store as a mirror.

# Getting Help
Please [submit an issue!](https://github.com/e-lo/forecastcards/issues)
