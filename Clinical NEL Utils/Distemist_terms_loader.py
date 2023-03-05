import os
import requests

api_url = "http://127.0.0.1:5003/terminosclinicos"

# folder path
tags_files_dir_path = r'.\\subtrack2_linking\\'
text_files_dir_path = r'.\\text_files\\'

# list to store files
res = []

# dictionary of terms (to avoid duplicates)
terms = {}

# Iterate directory
for path in os.listdir(tags_files_dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(tags_files_dir_path, path)):
        res.append(path)

        # Read tags file
        with open(tags_files_dir_path + path, 'r', encoding='utf8') as f:
            first_item = True
            for row in f:
                if first_item:
                    first_item = False
                    continue
                values = row.strip().split("\t")
                #id	effectiveTime	active	moduleId	refsetId	referencedComponentId	term
                #print(values)
                termino = {}
                termino["id"] = values[6];
                termino["term"] = values[5];
                #print(termino)
                terms[termino["id"]] = termino["term"]

        f.close();

#Sorting terms by name
sorted_terms = dict(sorted(terms.items(), key=lambda x:x[1]))

#Send to NEL engine
      
for key in sorted_terms:
    print(key + " - " + sorted_terms[key])
    headers =  {"Content-Type":"text/plain", "user":"distemist_terms_loader", "idtermino":key, "termino":sorted_terms[key], "token":""}
    response = requests.put(api_url, data=''.encode('utf-8'), headers=headers)
    print(response.status_code)
    print(response.json())
       
        #[print(line.strip()) for line in reportbody]

    #break
