# In this script, I'm generating the config file with the names of the tissues
import json

data = {}
data['tissues'] = []

with open('/scratch/tphung3/SmallProjects/ParseGtex/GTEx_Portal.csv', 'r') as f:
    for line in f:
        if not line.startswith('"Tissue"'):
            data['tissues'].append(line.rstrip('\n').split(',')[0].strip('"'))

with open('/scratch/tphung3/SmallProjects/ParseGtex/gtex_version8_config.json', 'w') as outfile:
    json.dump(data, outfile)