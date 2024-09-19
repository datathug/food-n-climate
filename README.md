# SCRATCH VERSION
THIS REPO IS WIP PROTOTYPE FOR AI-DRIVEN RESEARCH ON CONSEQUENCES 
OF CLIMATE CHANGE FOR PDO AREAS IN EU27 MEMBER STATES.
NOT INTENDED FOR BROAD PUBLIC SHARING. REFER TO eugenekalinouski@gmail.com FOR INQUIRIES.

### Vocabulary

**GEOREFERENCING**: human-readable text information about location of something, 
like "Castelfranco Emilia, Modena, Italia" or "Ponte da Barca, Viana do Castelo, Portugal"

**GEOCODING**: use human-readable address to retrieve XY (lonlat) coordinates, f.e. 
"Montaldeo, Provincia di Alessandria , Italia"    --->    (8.7304, 44.6666).
Usually this coordinate is very close to province / commune geographic center.

## ANALYSIS LOGIC

STEPS:
- Download source PDO info from eAmbrosia (1864 PDOs)
- Feed PDO info one by one to ChatGPT to get address-like locations **(georeference)**
- Feed derived georeferences to Geocoder to get points for each of these locations 
(30K address references for initial dataset)
- Download official geodata for EU land administration units from Eurostat's GISCO
- Join PDO info to communes (polygons) in QGIS based on coordinates related to each PDO


#### Intro
Project-wide variables and settings like data directories amd AI temperature in _common.py_.

For georeferencing use _georeferencing.py_ (API interactions scripts in _gpt_ directory)

Geocode with Google using _geocode_gpt_suggestions.py_ (API interactions scripts in _google_ directory).

Set index on initial EAmbrosia dataset with _data_prepare.py_

To run locally with Meta's Llama LLM _ollama_ client library needs 
to be installed alongside ollama app in the system.

QGIS scripts are supposed to run in QGIS environment.

Scratch scripts and prototypes in _misc_ directory.

#### Download data
XLSX Excel spreadsheet with all EU27 PDOs from eAmbrosia search engine page.
Make sure to put ticks on all fields before exporting to spreadsheet.


#### Create accounts with OpenAI and Google Cloud platform. 
Get API keys for OpenAI's ChatGPT API (probably requires premium at least tier 1?) 
and Google Geocode API (free trial $300 + $200 for this API). Save them as credentials.json in project root directory.
Format as 

    {
        "google": "YOUR_API_KEY_XXXX",
        "openai": "YOUR_API_KEY_YYYY"
    }


#### GEOREFERECING

These eAmbrosia records have abundant data, but we only need 1. File number (unique ID) as string, 2. product name and 3. its country.
Optionally we used 4. human-readable classification category (under column name Product category (obsolete))

For example, here is the information for a single PDO:

    PDO-FR-A0588 | Roussette du Bugey | France | Wine

We use OpenAI's ChatGPT API to prompt on each of the 1864 PDOs from 
eAmbrosia dataset separately. The result we are looking for is an address-like string, 
featuring commune, municipality or town that belongs to the PDO. **We call this georeference as it refers a distinct and unambiguous area.**
Usually we would get multiple addresses per single PDO. From 3-5 in Belgium to 30-100 in Italy and France.
To automate collection, we ask ChatGPT for enumerated list output (misformed response rate below 1% out of 1864 queries).
Take a look at **georeference** suggestions for **Roussette du Bugey**, FR (total 35 communes):

    1. Ambérieu-en-Bugey, Ain, France
    2. Andert-et-Condon, Ain, France
    3. Anglefort, Ain, France
    ...
    34. Virieu-le-Grand, Ain, France
    35. Vongnes, Ain, France

Impressive at the first glance, this may actually miss some of the communes 
included in a PDO, especially for complex PDOs with vague geographic delimitations.

Each PDO is georefereced by ChatGPT independently of the rest. 
One request to ChatGRP goes per one PDO record.
This version uses double-message pattern for prompting ChatGPT.
It sends two messages in a single request: system message and user message.
The first one defines behavior of AI in the conversation, it is like a preset.
And the latter one provides a query about a particular PDO. See these in project root, `system.prompt` and 'user.prompt' correspondingly.
Please note that you should not miss out placeholders in these files, like `{product_name}`.
These are replaced with actual values every time.
ChatGPT API is different from web app, it does not have chat memory. 
That is why we send these both prompts for each PDO.
For more about prompting refer to [this article](https://platform.openai.com/docs/guides/prompt-engineering) from OpenAI

OpenAI follows pay-as-you-go billing model, so it is important to count tokens used in the process. 
Both in and out tokens a counted, approximately 1,000 tokens = 750 words. With GPT-4o price is $5 per 1M tokens,
our analysis exceeded 1.2M. For a single PDO, this results in around 600 tokens in average.

Script saves ChatGPT suggestions as JSON files to _data/gpt-georef_, one per each PDO.

#### Geocoding with Google

Geopy's Google geocoder feature is used to perform geocoding of previously collected locations a.k.a. addresses.
It parses JSONs with ChatGPT suggestions about locations that should be dumped in a directory on a disk
by the time you get to this step. It writes results to `georef_units_xy.csv` in `data` directory and
creates a clean copy of it with duplicate records removed, writes to `georef_units_xy_no_dupl.csv`.

#### Spatial data for communes in EU
Download spatial GIS data for EU communes and other land administrative units. We used 2016 data loaded as GeoJSON from
https://ec.europa.eu/eurostat/web/gisco/geodata/administrative-units/communes
This is a big archive in different coordinate systems, we are only interested in one subset of this dataset - polygons for communes.
Communes are the lowest level sub-units within countries possible to collect automatically, that is why we use them.
COMM_RG_01M_2016_4326.geojson (4326 is a code for coordinate system used in the dataset). 
It includes 122K communes of different level across the EU and some neighbor countries like Albania and Serbia.
We may filter these out at the beginning, but we better skip as those will eventually drop out from our analysis 
as they have no PDOs referencing them as their location.

#### Spatial join in QGIS (2 steps)
##### Join attributes from PDOs to georeferences
First, for each of the 30K georeferenced points populate attributes from 1864 PDO info dataset. 
Both share the same ID field (File number), like "PDO-FR-A0588". Now we should have hot
a 30K points representing locations, with each of these having information about a PDO it is a part of.

##### Perform spatial join to EU administrative units
IMPORTANT: As some georeferences (addresses) belong to more than a single PDO, these will get duplicated in this step.
It is logically correct as we are mapping PDOs, not unique addresses.

Intersect EU communes polygon layer with points layer from previous step. Now we can enrich
communes layer with attribute information about PDOs (same columns from eAmbrosia spreadsheet).
This includes product name, type, classification category and related dates.

##### Merge communes within same PDOs (OPTIONAL) 
Use _Collect geometries_ tool to merge different communes within the same PDO into
a single multipolygon (polygon that may have multiple parts, like archipelago). 
This may be useful to be able to clearly visualize separate PDO features instead of communes with attributes about PDO.


### SCRIPTS COMPONENT
All scripts run in Python 3.12, may not work properly in earlier versions. 
It relies on multiple dependencies that need to be installed prior to using it. 
Below are listed only libraries essential for GPT georeferencing & Google Geocoding.
Install each of these with

`python -m pip install <DEPENDENCY NAME>`

- pandas (tables and CSV operations)
- openapi (GhatGPT API)
- geopy (Google's Geocoder API)