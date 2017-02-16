import os
import json
from django.http import HttpResponse
import random

# Create your views here.
def get_distribution(request, node1, node2, howmany, sorting):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    response = {}
    labels = []
    header = []
    items = []
    
#     header_translation = get_ccle_infos()
    
    field_delimiter = "|"
    format = "tsv"
    if format == "tsv": field_delimiter = "\t"
    elif format == "csv" : field_delimiter = ","
    
    lines = open(os.path.dirname(__file__) + "/statistics/" + node1 + "_" + node2 + "." + format)
    line_no = 0
    for line in lines:
        line_no += 1
        line = line.rstrip()
        fields = line.split(field_delimiter)
        if line_no == 1:
            labels = fields[0:2]
            continue
        
        header_item = fields[0]
        if '#' in header_item:
            header_item = " ".join(header_item.split("#")[0:2])
        header.append(header_item)
                
        item = fields[1]
        items.append(item)
    lines.close()
    
    # if random: random.choice(foo)
    
    if sorting == "DESC" or sorting == "ASC":
        header, items = zip(*sorted(zip(header, items), key=lambda pair: int(pair[1])))
        if sorting == "DESC":
            header = list(reversed(header))
            items = list(reversed(items))
    else:
        header, items = zip(*sorted(zip(header, items), key=lambda pair: (not pair[0].isdigit(), pair[0].zfill(3))))

    if howmany >= 0 and len(items) > howmany:
        items = items[:howmany]
        header = header[:howmany]
    
    header = list(header)
    
#     if node1 == "CellLine":
#         for i,item in enumerate(header):
#             for ccle in header_translation["items"]:
#                 if ccle[0] == item:
#                     header[i] = ccle[1]
#                     break
    
    response['details'] = {"labels": labels, "header": header, "items": items}
    
    return HttpResponse(json.dumps(response))

def statistics_all(request):
    
    response = {}

    header = ['Total breeds', 'Total genotypes', 'Total variants']
    rows = []
    labels = ['Information']
    response['details'] = {"header": header, "items": rows, "labels": labels}
    
    total_breeds = 8
    total_genotypes = 295
    total_variants = 179859
    
    rows.append(total_breeds)
    rows.append(total_genotypes)
    rows.append(total_variants)

    return HttpResponse(json.dumps(response))

def get_list(request, node1, node2, item, howmany, sorting):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    print(node1 + " " + node2 + " " + item)
    
    response = {}
    labels = []
    header = []
    items = []
    
#     header_translation = get_ccle_infos()
    
    field_delimiter = "|"
    format = "tsv"
    if format == "tsv": field_delimiter = "\t"
    elif format == "csv" : field_delimiter = ","
    
    lines = open(os.path.dirname(__file__) + "/statistics/" + node1 + "_" + node2 + "_table." + format)
    line_no = 0
    for line in lines:
        line_no += 1
        line = line.rstrip()
        fields = line.split(field_delimiter)
        if line_no == 1:
            labels.append(fields[1])
            continue

#         print(line)

        if fields[0] == item:
            items.append(fields[1])
            
    lines.close()
    
    if sorting == "DESC" or sorting == "ASC":
        
        items = sorted(items, key=lambda pair: int(pair[1]))
        
        if sorting == "DESC":
            items = reversed(items)

    if howmany >= 0 and len(items) > howmany:
        items = items[:howmany]
    
    response['details'] = {"labels": labels, "header": header, "items": items}
    
    return HttpResponse(json.dumps(response))
