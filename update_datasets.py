#!/usr/bin/env python
import requests as req

# See https://opencom.no/dataset/lokalisering-sykkeltellere-stavanger
print('Fetching counter locations')
counters_csv = req.get('https://opencom.no/dataset/1f64a769-9c10-4cc7-9db9-60ac74a7183e/resource/95d70356-d855-4430-9e04-c8d741e5761a/download/lokaliseringsykkeltellerestavanger.csv')
with open('./lokaliseringsykkeltellerestavanger.csv', 'wb') as f:
    f.write(counters_csv.content)

# See https://opencom.no/dataset/sykkeldata
print('Fetching count data')
data_csv = req.get('https://opencom.no/dataset/90cef5d5-601e-4412-87e4-3e9e8dc59245/resource/4c71d19a-adc4-42e0-9bed-c990316479be/download/sykkeldata.csv')
with open('./sykkeldata.csv', 'wb') as f:
    f.write(data_csv.content)
