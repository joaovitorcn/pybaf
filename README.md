# Python Bing API Facilitator 

Python Bing API Facilitator is a Python library created to simplify the usage of the bing api for distance between two geographic coordination. The project is on current development and future methods may be implemented 

## Installation

Import the package from Pypi

```python
pip install pybaf
```

## Usage

Import the class pybaf from the package

```python
from pybaf import pybaf
```

Define the bing_api with your [Bing key](https://www.bingmapsportal.com/)
```python
pybaf = pybaf(key = 'key')
```


You need to define two dataframes that contain latitude and longitude and their IDs to calculate a Distance Matrix

```python
df_origin = 'Insert the origin dataframe here'
df_destination = 'Insert the origin dataframe here'
```

The **distance_matrix** method returns a pd.DataFrame with all cross IDs (origin and destination) with their relative distance(KM) and time(minutes).

Note that you will need to pass the destination_id and origin_id to identify the returning pd.DataFrame

```python
df_matrix = pybaf.distance_matrix(df_destination='', df_origin='', destination_id='', origin_id='',)
```

The **n_smallest** method returns the n_smallest value between id_origin the id_destinations

```python
n_smallest_df = pybaf.n_smallest(df_final, n=1,origin_id='', destination_id='',value='')

# default n=1
```




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.


## Authors

developed by [joaovitorncn](https://github.com/joaovitocn)
