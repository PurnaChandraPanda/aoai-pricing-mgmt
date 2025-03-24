import pandas as pd
import json

class CSVProcessor:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)

    def filter_resource_cost(self, resource_name):
        aoai_resource_df = self.df[self.df['ResourceId'].str.contains(resource_name)]
        aoai_resource_df = aoai_resource_df.copy()
        aoai_resource_df.loc[:, 'deployment'] = aoai_resource_df['tags'].apply(lambda x: json.loads(x).get('deployment', None))
        
        ## Display the filtered DataFrame
        # print(aoai_resource_df[['date', 'meterName', 'ProductName', 'deployment', 'PayGPrice']].to_string(index=False))
        # print(aoai_resource_df[['date', 'meterName', 'PayGPrice']].to_string(index=False))

        grouped_df = aoai_resource_df.groupby(['date', 'meterName'])['costInUsd'].sum().reset_index()

        # Print the result
        print(grouped_df.to_string(index=False))

