import os
import requests

api_url = "http://127.0.0.1:5003/reports"

# folder path
reports_files_dir_path = r'.\\subtrack2_linking\\'
text_files_dir_path = r'.\\text_files\\'

# list to store files
res = []

# Iterate directory
for path in os.listdir(text_files_dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(text_files_dir_path, path)):
        res.append(path)

        # Get idreport
        reportid = path[0:-4]

        # Read text file
        with open(text_files_dir_path + path, 'r', encoding='utf8') as f:
            reportbody = f.readlines()

        f.close();

        #Send to NEL engine

        headers =  {"Content-Type":"text/plain", "user":"distemist_reports_loader", "reportid":reportid, "token":""}
        response = requests.put(api_url, data=' '.join(reportbody).encode('utf-8'), headers=headers)
        print(response.status_code)
        print(response.json())
        
        #[print(line.strip()) for line in reportbody]

    #break
