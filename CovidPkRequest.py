import requests
import json
import payloads

class collectData():
    def __init__(self):
        self.url = "https://datastudio.google.com/embed/batchedDataV2"
        self.querystring = {"appVersion":"20200415_01020016"}
        self.headers = {'content-type': "application/json"}
        self.payload = None

    def get_response(self, payload):
        payload=json.dumps(payload)
        response = requests.request("POST", self.url, data = payload, headers = self.headers, params = self.querystring)
        return json.loads(response.text[5:])

    def get_data(self):
        data = payloads.get_payloads()
        data_list = []
        for pl in data['payloads']:
            array = {'Title':pl['Title'],'data':[]}
            array_data = array['data']
            response = self.get_response(pl['payload'])

            i=0
            for arr in response['default']['dataResponse'][0]['dataSubset'][0]['dataset']["tableDataset"]['column']:
                try:
                    values = arr['stringColumn']['values']
                    array_data.append({'column_data':values, 'columnId': pl['Columns'][i]['columnId'],'columnName':pl['Columns'][i]['columnName']})
                except:
                    pass
                try:
                    values = arr['doubleColumn']['values']
                    array_data.append({'column_data':values, 'columnId': pl['Columns'][i]['columnId'],'columnName':pl['Columns'][i]['columnName']})
                except:
                    pass
                i=i+1
            data_list.append(array)
        return data_list

# c=collectData()
# list = c.get_data()
# for graph in list:
#     if graph['Title']=='Overview of Cases in Pakistan':
#         for columns in graph['data']:
#             print(columns['columnName'])
#             print(columns['column_data'])
#             # print(int(columns['column_data'][int(len(columns['column_data'])-1)]))
#
#     if graph['Title'] == 'Provinces Details':
#         for columns in graph['data']:
#             print(columns['columnName'])
#             print(columns['column_data'])
