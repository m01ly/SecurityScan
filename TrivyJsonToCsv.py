import json
import pandas as pd
import json
import os
import glob
##使用trivy扫描镜像导出格式是json的，不方便阅读，通过该脚本实现json转为csv
all_dfs = []
folder_path = os.getcwd()
print(folder_path)
for filename in os.listdir(folder_path):
    print(filename)
    filename='orch-components-init.json'
    if filename.endswith('.json'):
        file_path = os.path.join(folder_path,filename)

        with open(file_path,'r',encoding='utf-8') as fd:
            data = json.load(fd)

            print(data['Results'])
            for sub_dict in data['Results']:
                if 'Vulnerabilities' not in sub_dict.keys():
                    sub_dict['Vulnerabilities'] = []

            df_nested_list = pd.json_normalize(data['Results'], record_path=['Vulnerabilities'], meta=['Target'], errors='ignore')
            df_nested_list['image'] = filename.replace(".json","")
            all_dfs.append(df_nested_list)
        fd.close()
    df = pd.concat(all_dfs)
    df.to_csv(r'orch-components-init.csv', index = None)


