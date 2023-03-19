import pandas as pd
import numpy as np
import json
#Numpy>Dataframe>JSON
columns = ['tag','patterns','responses','context']
df = pd.DataFrame(columns=columns)
#np.array(["Bye","See ya"])
#tag.csv
#patterns.npy
#responses.npy
#context.npy
df = df.append({'tag':tagdata,'patterns':patternsdata,'responses':responsesdata,'context':contextdata}, ignore_index=True)



# Data Frame to JSON Compiler #
df.to_json('temp.json', orient='records', lines=False)
with open('temp.json') as f:
    data = json.load(f)

print(data)
entry = {}
entry['intents']=data
print(entry)
with open('temp.json', mode='w', encoding='utf-8') as feedsjson:
    json.dump(entry, feedsjson)
###############################
