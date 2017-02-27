from django.http import HttpResponse
import glob
import os
import json

# Create your views here.
def statistics_all(request):
    
    response = {}

    header = ['Total fasta', 'Total sam', 'Total bam', 'Total gtf']
    rows = []
    labels = ['Information']
    response['details'] = {"header": header, "items": rows, "labels": labels}
    
    total_fastq = len(get_elements("File", "Path", "FASTA", None, None)[1])
    total_sam = len(get_elements("File", "Path", "SAM", None, None)[1])
    total_bam = len(get_elements("File", "Path", "BAM", None, None)[1])
    total_gtf = len(get_elements("File", "Path", "GTF", None, None)[1])
    
    rows.append(total_fastq)
    rows.append(total_sam)
    rows.append(total_bam)
    rows.append(total_gtf)

    return HttpResponse(json.dumps(response))

def get_elements(node1, node2, item, howmany, sorting):
    
    labels = []
    items = []
    
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
        
    return (labels, items)

def get_list(request, node1, node2, item, howmany, sorting):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    print(node1 + " " + node2 + " " + item)
    
    response = {}
    labels, items = get_elements(node1, node2, item, howmany, sorting)    
    
    response['details'] = {"labels": labels, "header": [], "items": items}
    
    return HttpResponse(json.dumps(response))

def download_data(request):
    
    header = ['Sample', 'BAM file', 'GTF file', "Fasta file"]
    rows = []
    response = {}
    details = {"header": header, "items": rows}
    response['details'] = details
    
#     sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    labels, gtf_files = get_elements("File", "Path", "GTF", None, None)
    labels, bam_files = get_elements("File", "Path", "BAM", None, None)
    labels, fastq_files = get_elements("File", "Path", "FASTA", None, None)
    
    for i in range(len(gtf_files)):
#     for cell in CellLine.nodes.all():
#         cell_line_id = cell.cell_line
        
#         size_bytes = os.path.getsize(url)
#         size_converted = size_bytes
#         size_human_index = 0
#         
#         while size_converted/1024 > 1:
#             size_converted = size_converted / 1024
#             size_human_index += 1
#         
#         size_human = size_converted + " " + sizes[size_human_index]
        
        bam_file = bam_files[i]
        gtf_file = gtf_files[i]
        fastq_file = fastq_files[i]
        
        print(gtf_file)
        
        rows.append([
            "Sample " + str(i+1),
            {"label": "Bam file",
             "url": "downloads/bam/" + bam_file},
            {"label": "Gtf file",
             "url": "downloads/gtf/" + gtf_file},
            {"label": "Fasta file",
             "url": "downloads/fasta/" + fastq_file}
            ])

    return HttpResponse(json.dumps(response))

def see_file(request, file, skip, limit):
    
    skip = int(skip)
    limit = int(limit)
    
    response = {}
    rows = []
    header = []
    
    ids = []
    with open(os.path.dirname(__file__) + "/data/" + "ENST.to.extract", "r") as lines:
        for line in lines:
            ids.append(line.strip())
    
    line_no = 0
    filename = os.path.dirname(__file__) + "/data/" + file
    print(filename)
    with open(filename, "r") as lines:
        for line in lines:
            
            line_no += 1
            
            fields = line.strip().split("\t")
            
            if line_no == 1:
                header = ["Transcript id"] + fields
                continue

            if(line_no-1 <= skip): continue
            
            if len(rows) < limit:
                fields.insert(0, ids[line_no-2])
                rows.append(fields)
            
    response["details"] = {"header": header, "items": rows, "total": line_no, "page": int(skip/limit), "limit": limit}
    
    return HttpResponse(json.dumps(response))
    