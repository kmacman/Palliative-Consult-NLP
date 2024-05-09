# Palliative Consult Question NLP API

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Description

This project uses rule-based entity tagging and logic, developed with the MedSpacy package, to extract structured data from free-text palliative care consult questions.

The various categories of diagnoses and consult reasons are based on the [PCQC](https://palliativequality.org/) codes for palliative care referrals.

Most of the work is done by the extensive target rules found in `App/data_processing/target_rules.py`. Feel free to modify this file to fit your needs. 

When matched entities are tagged, they are also associated with diagnosis or reason codes. These are then extracted using the MedSpacy DocConsumer.

Some additional logic is found in the `classes` modules. The one with the most impact on the function of the program is the diagnosis heirarchy within `ExtractProblem.py`. Changes to the order of this heirarchy will change the logic for how a primary diagnosis is selected in the event that multiple diagnoses are present.

## Table of Contents

- [Installation and Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [To-Do](#to-do)

## Usage

This tool can be used multiple ways. You can use it within Jupyter Notebooks, or you can deploy it locally as an API using Docker.

Either way, I recommend creating a local copy of the repository on your machine first.

### Jupyter Notebook:

See `notebook.ipynb` for example of how to import the modules and use them directly on data within Jupyter and Pandas dataframes.

### Dockerized API:

To run this program as a Docker API, you need to have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your computer.

If you navigate to the root folder of the repository on your machine and run: `docker-compose up --build` it should automatically build and launch the docker image on http://localhost:80. 

To stop the program, run `docker-compose down`.

For an example of how to use the API, see the `api_nb.ipynb` notebook.

Note, there is an API hosted on-line at http://palliapi.kentmccannmd.com/analyze however this is meant strictly for demonstration purposes. Do not send any protected patient information to this URL. 

## To-Do:

- [ ] Fix naming conventions of modules to better reflect their functionality.


## Contributing

If you are interested in contributing, please reach out to me at KentMcCannMD@Gmail.Com


## License

This project is licensed under the [MIT License](LICENSE).