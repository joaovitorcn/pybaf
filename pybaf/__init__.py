import pandas as pd
import requests
import json



class pybaf():

    def __init__(self, key: 'api key str' = None):

        if key is None:
            raise ValueError('Key must be inserted')
        self.api_key = key
    def __version__():
        version = '0.0.2'
        print(version)
    # checks that will ensure correct variable type is passed
    def _check_error(self, df_destination, df_origin, destination_id, origin_id):
        self._check_if_df(df_destination)
        self._check_if_df(df_origin)

        self._check_if_column_in_df(df_destination, destination_id, 'df_destination')
        self._check_if_column_in_df(df_origin, origin_id, 'df_origin')

        self._check_if_column_in_df(df_destination, 'latitude', 'df_destination')
        self._check_if_column_in_df(df_origin, 'latitude', 'df_origin')

        self._check_if_column_in_df(df_destination, 'longitude', 'df_destination')
        self._check_if_column_in_df(df_origin, 'longitude', 'df_origin')

    def _check_if_df(self, df):
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Value is not a pd.DataFrame")

    def _check_if_column_in_df(self, df: 'data frame', column_name: 'Column Name', df_name=None):

        if not column_name in df.columns:
            print(df.columns)
            raise ValueError("Column {} is not on DataFrame : {}".format(str(column_name), df_name))

    # transforms data received from bing to pd.DataFrame()

    def _data_to_df(self, data):
        number = len(data['resourceSets'][0]['resources'][0]['results'])
        df_data = pd.DataFrame(columns=[self.destination_id, self.origin_id, "distancia", "duracao"])
        for x in range(0, (number)):
            id_origem = data['resourceSets'][0]['resources'][0]['results'][x]['originIndex']
            id_destination = data['resourceSets'][0]['resources'][0]['results'][x]['destinationIndex']
            distance = data['resourceSets'][0]['resources'][0]['results'][x]['travelDistance']
            duration = data['resourceSets'][0]['resources'][0]['results'][x]['travelDuration']
            df_data.loc[x] = [id_origem, id_destination, distance, duration]

            df_data.reset_index(inplace=True, drop=True)
        return df_data

    # get latitude and longitude from pd.DataFrame to API format .

    def _get_lat_lon(self, df):
        rows = len(df.index)
        lat_long = []
        lat_long_list = []
        for y in range(0, (rows)):
            lat = df.iloc[y]['latitude']
            lon = df.iloc[y]['longitude']
            lat_long.append([lat, lon])

        return lat_long

    # post request to API

    def _post_request(self, payload):

        url = 'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={}'.format(self.api_key)

        # Adding empty header as parameters are being sent in payload
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(payload), headers=headers)

        return (json.loads(r.text))

    # will split pd.DataFrame to ensure API limit of combinations is respect

    def _split_origin_destination(self, origins, destinations,lista_origin):

        number = 2500
        len_origins = len(origins)
        len_destinations = len(destinations)

        combinations = len_origins * len_destinations

        if combinations < number:
            return True, origins, destinations
        else:
            n_origins = number // len_destinations
            teste = [origins[x:(x + n_origins)] for x in range(0, len(origins), n_origins)]
            names = [lista_origin[x:(x + n_origins)] for x in range(0, len(lista_origin), n_origins)]
            print('loops: {} || origens: {} || destinations: {} || limite ={}'
                  .format(len(teste), len(origins), len(destinations), number))

            return False, teste, destinations,names

    # create text that will be used on api request
    def _create_text(self, origins, destinations):

        origins_rows = len(origins)
        rows = len(destinations)

        if len(origins) == 1:

            teste3 = {
                "origins": [{
                    "latitude": origins[0],
                    "longitude": origins[1]
                }
                ],
                "destinations": [{
                    "latitude": destinations[0][0],
                    "longitude": destinations[0][1]
                },
                ],
                "travelMode": 'driving',
            }

        else:
            teste3 = {
                "origins": [{
                    "latitude": origins[0][0],
                    "longitude": origins[0][1]
                }
                ],
                "destinations": [{
                    "latitude": destinations[0][0],
                    "longitude": destinations[0][1]
                },
                ],
                "travelMode": 'driving',
            }
            for x in range(1, (origins_rows)):
                teste3['origins'].append(
                    {'latitude': origins[x][0],
                     'longitude': origins[x][1]})

        for x in range(1, rows):
            teste3['destinations'].append(
                {'latitude': destinations[x][0],
                 'longitude': destinations[x][1]}
            )

        return teste3

    # attach the api results to the IDs from original pd.DataFrames
    def _attach_ids(self, df_final, lista_origin, lista_destination):

        for x in range(0, len(lista_origin)):
            df_final[self.destination_id] = df_final[self.destination_id].replace(x, lista_origin[x])
        for x in range(0, len(lista_destination)):
            df_final[self.origin_id] = df_final[self.origin_id].replace(x, lista_destination[x])

        return df_final

    # distance matrix will return the combinations of distance between df_destination and df_origin

    def distance_matrix(self, df_destination, df_origin, destination_id, origin_id):

        self.destination_id = destination_id
        self.origin_id = origin_id

        df_final = pd.DataFrame()
        check = self._check_error(df_destination, df_origin, destination_id, origin_id)

        lista_destination = list(df_destination[self.destination_id])
        lista_origin = list(df_origin[self.origin_id])

        origins = [x for x in self._get_lat_lon(df_origin)]
        destinations = self._get_lat_lon(df_destination)

        var1, origins, destinations,lista_origin = self._split_origin_destination(origins, destinations,lista_origin)

        if var1:
            payload = self._create_text(origins, destinations)
            json_text = self._post_request(payload)

            df = self._data_to_df(json_text)
            df_final = df_final.append(df)

            df_final = self._attach_ids(df_final, lista_origin, lista_destination)

        else:

            for origin in origins:
                print('loop number {}'.format(origins.index(origin)))
                payload = self._create_text(origin, destinations)

                json_text = self._post_request(payload)

                df = self._data_to_df(json_text)

                df_final = df_final.append(df)
                origin_name = lista_origin[origins.index(origin)]



                df_final = self._attach_ids(df_final, origin_name, lista_destination)


        return df_final

    # n_smallest will return the n smallest of calculated distance matrix

    def n_smallest(self, df_final, origin_id: 'Origin id', destination_id: 'Destination Id',
                   value: 'value that will be considered', n=1):

        self._check_if_df(df_final)

        if value is None or origin_id is None or destination_id is None:
            raise ValueError('id and value must be column names')

        self._check_if_column_in_df(df_final, origin_id)
        self._check_if_column_in_df(df_final, value)

        df_final = df_final.sort_values(by=origin_id)

        df_groupby = df_final.groupby([origin_id, destination_id])[value].nsmallest(n).reset_index()

        df_groupby = df_groupby.drop(columns='level_2')

        result = pd.merge(df_groupby, df_final, on=[origin_id, value], how='inner')

        return result
