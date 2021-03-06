import os
import json
import csv
from django.http import HttpResponse

from django.views.decorators.csrf import ensure_csrf_cookie

from models import Variant, Sample
from collections import Set

MAX_RESULTS_NUMBER = 1000

# Create your views here.
def get_total_stats(request):

    snps = get_stats_of_type("TOTAL_SNPS")[0]
    indels = get_stats_of_type("TOTAL_INDELS")[0]
    total = ["Cultivar number", 146]

    data = {}
    data["details"] = {"header": [], "items": [snps, indels, total]}

    return HttpResponse(json.dumps(data))

def get_stats_of_type(stat_type):
    data = []
    raw_file = os.path.dirname(__file__) + "/statistics/statistics.txt"
    #Per leggere la prima colonna e riportare tutti i campi
    with open(raw_file) as stat_file:
        for i in stat_file.readlines():
            i = i.rstrip()
            cols=i.split('\t')
            if stat_type in cols[0]:
                data.append(cols[1:])
    stat_file.close()

    return data

def get_info_all_simple(request, type, howmany):
    
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
            header = [el.title() if not el.isupper() else el for el in line.split(field_delimiter)[0:3]]
            continue
        
        else:

            items.append(line.split(field_delimiter)[0:3])

    lines.close()
    
    if howmany >= 0 and len(items) > howmany:
        items = items[:howmany]

    response['details'] = {"header": header, "items": items}
    
    return HttpResponse(json.dumps(response))

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

def get_chromosomes(request):
    filename = "chromosomes.txt"
    return HttpResponse(json.dumps([line.rstrip('\n') for line in open(os.path.dirname(__file__) + "/data/" + filename)]))

def get_genes(request):
    filename = "genes.txt"
    return HttpResponse(json.dumps([line.rstrip('\n') for line in open(os.path.dirname(__file__) + "/data/" + filename)]))

def get_genes_info():
    filename = "genes.gff"
    
    genes = []
    for line in open(os.path.dirname(__file__) + "/data/" + filename):
        if line.startswith("#"): continue
        line = line.rstrip()
        pieces = line.split("\t")
        chrom = pieces[0]
        type = pieces[2]
        start = pieces[3]
        end = pieces[4]
        ID = pieces[8].split(";")[0].replace("ID=", "")
        
        gene = {"chrom": chrom, "type": type, "start": start, "end": end, "ID": ID}
        genes.append(gene)
    
    return genes

def get_cultivars_info():
    filename = "PEACH_CODE.txt"
    
    cultivars = []
    for line in open(os.path.dirname(__file__) + "/data/" + filename):
        if line.startswith("#"): continue
        line = line.rstrip()
        pieces = line.split("\t")
        cultivar = pieces[0]
        sample_name = pieces[1]
        
        cultivar = {"name": cultivar, "sample": sample_name}
        cultivars.append(cultivar)
    
    return cultivars

def get_gene_types(request):
    filename = "gene_types.txt"
    return HttpResponse(json.dumps([line.rstrip('\n') for line in open(os.path.dirname(__file__) + "/data/" + filename)]))

def get_cultivars(request):
    filename = "cultivars.txt"
    return HttpResponse(json.dumps([line.rstrip('\n') for line in open(os.path.dirname(__file__) + "/data/" + filename)]))

@ensure_csrf_cookie
def search_by_cultivar(request):
    
    cultivars = json.loads(request.body)[0]
    print("CULTIVARS:" + str(cultivars))
    
    data = set()
    header = ['ID', 'pos', 'ref', 'alt', 'type', 'sample(s)']
    
    cultivar_info = get_cultivars_info()
    samples = []
    for info in cultivar_info:
        if info["name"] in cultivars:
            samples.append(info["sample"])
    print("CULTIVARS:" + str(samples))
    
    for cultivar in Sample.nodes.filter(ID__in=samples):
        
        for variantInfo in cultivar.hasInfo[0: MAX_RESULTS_NUMBER]:
            
            if len(data) >= MAX_RESULTS_NUMBER: break
            
            for variant in variantInfo.variant:
                var = (variant.ID, variant.pos, variant.ref, variant.alt, variant.type, len(variantInfo.sampleInfo))
                data.add(var)

    print(str(len(data)) + " results")
    response = {'header': header, 'items': [list(el) for el in data], 'length': len(data)}

    return HttpResponse(json.dumps(response))

def search_by_chromosome(request, chromosome, start, end, include_snps = True, include_indels = True):
    
    data = []
    header = ['ID', 'pos', 'ref', 'alt', 'type', 'sample(s)']
    
    include_indels = include_indels.lower() == "true"
    include_snps = include_snps.lower() == "true"
    
    total = 0
    for variant in Variant.nodes.filter(chrom__exact=chromosome).filter(pos__gte=start).filter(pos__lte=end)[0: MAX_RESULTS_NUMBER]:
        
        if total >= MAX_RESULTS_NUMBER: break
        if variant.type == "SNP" and not include_snps: continue
        if variant.type == "INDEL" and not include_indels: continue
        
        samples = 0
        for info in variant.info:
            samples = len(info.sampleInfo)
        
        var = [variant.ID, variant.pos, variant.ref, variant.alt, variant.type, samples]
        data.append(var)
        total += 1

    response = {'header': header, 'items': data, 'length': total}

    return HttpResponse(json.dumps(response))

def search_by_gene_type(request, gene_type):
    return search_by_gene(request, gene_type, None)
    
def search_by_gene_name(request, gene_name):
    return search_by_gene(request, None, gene_name)
    
def search_by_gene(request, gene_type, gene_name):
    
    data = []
    header = ['ID', 'pos', 'ref', 'alt', 'type', 'sample(s)']
    
    print("REQ: " + str(gene_type) + " NAME="+str(gene_name))    
    genes = [gene for gene in get_genes_info() if gene["type"] == gene_type or gene["ID"] == gene_name]
    
    print("Genes found: " + str(len(genes)))

    total = 0
    for gene in genes:
        if total >= MAX_RESULTS_NUMBER: break
        
        print("Total="+str(total) + " - Searching for gene="+str(gene))
        for variant in Variant.nodes.filter(chrom__exact=gene["chrom"]).filter(pos__gte=gene["start"]).filter(pos__lte=gene["end"])[0:MAX_RESULTS_NUMBER]:
             
            if total >= MAX_RESULTS_NUMBER: break
            
            total = 0
            for variantInfo in variant.info:
                total += len(variantInfo.sampleInfo)
            
            var = [variant.ID, variant.pos, variant.ref, variant.alt, variant.type, total]
            data.append(var)
            total += 1

    response = {'header': header, 'items': data, 'length': total}

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
        n = len(cultivar.hasInfo)
#         print(str(cultivar) + " " + str(n))
#         print(cultivar)
#         snps = indels = 0
#         for info in cultivar.hasInfo:
#             type = info.variant.type
#             if type == "INDEL":
#                 indels += 1
#             elif type == "SNP":
#                 snps += 1
        writer.writerow([cultivar.ID, n])
        
    file.close()
    
    return HttpResponse()
    pass

def download(request, format):
    pass
    
