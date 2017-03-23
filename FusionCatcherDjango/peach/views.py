import os
import json
import csv
from django.http import HttpResponse

from models import Chromosome, Sample

# Create your views here.
def get_info_all(request, type, howmany):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    response = {}
    header = []
    items = []
    
#     header_translation = get_ccle_infos()
    
    filename = "Accession_number_peach_1."+type+".tsv"

    format = filename.split(".")[-1]
    field_delimiter = "|"
    if format == "tsv": field_delimiter = "\t"
    elif format == "csv" : field_delimiter = ","
    
    lines = open(os.path.dirname(__file__) + "/data/" + filename)
    line_no = 0
    for line in lines:
        line_no += 1
        
        line = line.rstrip()
        
        if line_no == 1:
            if line.startswith("#"):
                line = line[1:]
            header = [el.title() if not el.isupper() else el for el in line.split(field_delimiter)]
            continue
        
        else:
            
            items.append(line.split(field_delimiter))

    lines.close()
    
    if howmany >= 0 and len(items) > howmany:
        items = items[:howmany]
    
    response['details'] = {"header": header, "items": items}
    
    return HttpResponse(json.dumps(response))

def get_distribution(request, node1, node2, howmany, sorting, parameter):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    response = {}
    labels = []
    header = []
    items = []
    
#     header_translation = get_ccle_infos()
    
    field_delimiter = "|"
    format = "csv"
    if format == "tsv": field_delimiter = "\t"
    elif format == "csv" : field_delimiter = ","
    
    lines = open(os.path.dirname(__file__) + "/statistics/" + node1 + "_" + node2 + ("_" +parameter if parameter else "") + "." + format)
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

def generate_statistics(request):
    
    basedir = os.path.dirname(__file__) + "/statistics/"
    if not os.path.exists(basedir):
        os.mkdir(basedir)
        
    filename = basedir + "Cultivar_Variants.csv"
    file = open(filename,'w')
    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(["Cultivar", "Variants"])
    
    print(len(Sample.nodes))
    for cultivar in Sample.nodes.all():
#         n = len(cultivar.hasInfo)
#         print(str(cultivar) + " " + str(n))
        print(cultivar)
        snps = indels = 0
        for info in cultivar.hasInfo:
            type = info.variant.type
            if type == "INDEL":
                indels += 1
            elif type == "SNP":
                snps += 1
        writer.writerow([cultivar.ID, snps])
        
    file.close()
    
    return HttpResponse()
    pass

def download(request, format):
    pass
    