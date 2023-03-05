import os
import requests

api_url = "http://127.0.0.1:5003/reports"

# folder path
tags_files_dir_path = r'.\\subtrack2_linking\\'
labeled_reports_path = r'.\\NEL_engine_output\\labeled_reports_2.csv'
output_validation_path = r'.output_validation_2.csv'

# list to store files
res = []
tags_files_tags = {}
labeled_reports_tags = {}

# Read NEL engine labels
with open(labeled_reports_path, 'r', encoding='utf8') as f:
    first_item = True
    for row in f:
        if first_item:
            first_item = False
            continue
        values = row.strip().split(",")
        #id,idreport,idtermino,termino,cosine_similarity,source_text
        #print(values)
        termino = {}
        termino["id"] = values[0];
        termino["idreport"] = values[1];
        termino["idtermino"] = values[2];
        termino["termino"] = values[3];
        termino["cosine_similarity"] = values[4];
        termino["source_text"] = values[5];
        #print(termino)
        if termino["idreport"] not in labeled_reports_tags: 
            labeled_reports_tags[termino["idreport"]] = []
        labeled_reports_tags[termino["idreport"]].append(termino)

f.close();


# Iterate directory
for path in os.listdir(tags_files_dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(tags_files_dir_path, path)):
        res.append(path)

        # Read Distemist tags file
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
                termino["idreport"] = values[0];
                termino["id"] = values[6];
                termino["term"] = values[5];
                termino["relation"] = values[7];
                #print(termino)
                if termino["idreport"] not in tags_files_tags: 
                    tags_files_tags[termino["idreport"]] = []
                tags_files_tags[termino["idreport"]].append(termino)

        f.close();


f = open(output_validation_path, 'w', encoding='utf8')
f.write("Idreport,Matches,Mismatches,Missing\n" )

#Compare tags   
# Iterate over NEL engine labeled reports
for key_1 in labeled_reports_tags:
    num_matches = 0
    num_mismatches = 0
    num_missing = 0
    # Iterate over NEL engine labels
    for termino in labeled_reports_tags[key_1]:
        match = False
        if key_1 in tags_files_tags:
            # Iterate over Distemist labels for that report
            for termino2 in tags_files_tags[key_1]:
                if termino["idtermino"] == termino2["id"]:
                    #Label correctly linked
                    match = True
                    num_matches = num_matches + 1
                    break;
        if match == False:
            #Label incorrectly linked (error)
            num_mismatches = num_mismatches + 1
    if key_1 in tags_files_tags:
        #Number of labels not linked (error)
        num_missing = len(tags_files_tags[key_1]) - num_matches
    print( key_1 + " Matches: " + str(num_matches) + "(" + str(int(num_matches/(num_mismatches+num_matches)*100))  + "%) Mismatches: " + str(num_mismatches) + "(" + str(int(num_mismatches/(num_mismatches+num_matches)*100)) + "%) Missing: " + str(num_missing) )
    f.write( key_1 + "," + str(num_matches) + "," + str(num_mismatches) + "," + str(num_missing) + "\n" )
        
            
f.close();
