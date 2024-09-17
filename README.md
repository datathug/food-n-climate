# SCRATCH VERSION
THIS REPO IS WIP PROTOTYPE FOR AI-DRIVEN RESEARCH ON CONSEQUENCES 
OF CLIMATE CHANGE FOR PDO AREAS IN EU27 MEMBER STATES.
NOT INTENDED FOR BROAD PUBLIC SHARING. REFER TO eugenekalinouski@gmail.com FOR INQUIRIES.

## Vocabulary

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
- 

#### Download data
XLSX Excel spreadsheet with all EU27 PDOs from eAmbrosia search engine page.
Make sure to put ticks on all fields before exporting to spreadsheet.

#### Create accounts with OpenAI and Google Cloud platform. 
Get API keys for OpenAI's ChatGPT API (probably requires premium at least tier 1?) 
and Google Geocode API (free). Save them as credentials.json in project root directory.
Format as 
````
{
    "google": "YOUR_API_KEY_XXXX",
    "openai": "YOUR_API_KEY_YYYY"
}
````

#### GEOREFERECING
These eAmbrosia records have abundant data, but we only need 1. File number (unique ID) as string, 2. product name and 3. its country.
Optionally we used 4. human-readable classification category (under column name Product category (obsolete))

For example, here is the information for a single PDO:
````
PDO-FR-A0588 | Roussette du Bugey | France | Wine
````

We use OpenAI's ChatGPT API to prompt on each of the 1864 PDOs from 
eAmbrosia dataset separately. The result we are looking for is an address-like string, 
featuring commune, municipality or town that belongs to the PDO. **We call this georeference as it refers a distinct and unambiguous area.**
Usually we would get multiple addresses per single PDO. From 3-5 in Belgium to 30-100 in Italy and France.
To automate collection, we ask ChatGPT for enumerated list output (misformed response rate below 1% out of 1864 queries).
Take a look at **georeference** suggestions for **Roussette du Bugey**, FR (total 35 communes):

````
1. Ambérieu-en-Bugey, Ain, France
2. Andert-et-Condon, Ain, France
3. Anglefort, Ain, France
...
34. Virieu-le-Grand, Ain, France
35. Vongnes, Ain, France
````

Impressive at the first glance, this may actually miss some of the communes 
included in a PDO, especially for complex PDOs with vague geographic delimitations.

Script saves ChatGPT suggestions on JSON files, one per each PDO.

#### Geocoding with GPT

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
This relies on multiple dependencies that need to be installed prior to using it. 
Below are listed only libraries essential for GPT georeferencing & Google Geocoding.
Install each of these with

`python -m pip install <DEPENDENCY NAME>`

- pandas (tables and CSV operations)
- tiktoken (count tokens used with ChatGPT - important for billing)
- openapi (GhatGPT API)
- geopy (Google's Geocoder API)