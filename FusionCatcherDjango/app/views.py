from app.models import Gene, File, Chromosome, CellLine, Fusion, Protein, Virus, Exon,\
    Transcript
import json
import os
import csv
from sets import Set
from neomodel import db
import glob

# Create your views here.
from django.http import HttpResponse
import dis

def fusion_events(request, chromosome):
    return HttpResponse("You asked for fusion events of chromosome " + chromosome)

def genes(request, howmany):
    return HttpResponse("Genes: " + str(Gene.nodes.all()[0:int(howmany)]))

def count_genes(request, prefix):
    return HttpResponse(len(Gene.nodes.filter(symbol__startswith=prefix)))

# def statistics_all(request):
#     files = File.nodes.all()
#     
#     response = {}
#     details = []
#     header = ["Filename", "Indels", "Snp"]
#     response['details'] = {"header": header, "items": details}
# 
#     for exp_file in files:
#         item = vars(exp_file)
#         details.append(item)
# 
#     return HttpResponse(json.dumps(response))

# def statistics(request, filename):
#     File.nodes.filter(filename__exact=filename)
#     return HttpResponse("Unimplemented API")

def print_file(request):
    f = open("test.txt", "r")
    return HttpResponse(f.read())

def chromosomes(request):
    return HttpResponse(json.dumps(open(os.path.dirname(__file__) + "/" + "chromosomes.txt").read().splitlines()))

# def cell_lines(request):
#     response = []
#     for cell_line in CellLine.nodes.all():
#         response.append(cell_line.cell_line)
#         
#     return HttpResponse(json.dumps(response))

def search_indels_by_region(request, chromosome, start, end):
    
    print("Chromosome: " + chromosome + ", start="+start + ", end="+end)
    
    details = []
    response = {}
    response['details'] = {"header": ["id", "fusion point 1", "fusion point 2"], "items": details}
    
    for chrom in Chromosome.nodes.filter(chromosome__exact=chromosome):
        for res in chrom.fusion_events.filter(fusion_point_1__startswith=start):
            details.append([{"value": res.id}, {"value": res.fusion_point_1}, {"value": res.fusion_point_2}])
        
    return HttpResponse(json.dumps(response))

def get_chromosomes_cell_lines(request, cell_line):
    response = []
    
    c = CellLine.nodes.get(cell_line=cell_line)
    print(vars(c.fusion_events))
#     for fusion in c.fusion_events:
#         response.append(str(fusion.fusion_point_1) + "-" + str(fusion.fusion_point_2))
    
    return HttpResponse(json.dumps(response))

def show_info(request, filename):
    response = {}
    details = []
    header = []
    
    line_no = 0
    for line in open(os.path.dirname(__file__) + "/" + filename):
        line_no += 1
        
        fields = line.split("\t")
        if line_no <= 2:
            if line_no == 1:
                header = fields
                print(header)
            else:
                for i in range(0, len(header)):
                    header[i] = header[i] + " " + fields[i]
                    
        else:
            details.append(fields)
            
    response['details'] = {"header": header, "items": details}
    
    return HttpResponse(json.dumps(response))

def search_for_cell_line(request,c_line):
    response = {}
    
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        fusions.append(fusion)
    
    rows = build_rows(fusions)
    
    response['rows'] = {"header": header, "items": rows}
    
    return HttpResponse(json.dumps(response))

def search_for_chromosome(request,c_line,chromos,start_point,end_point):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        if fusion.at_chromosome.match(fusion_point__gte=start_point) and fusion.at_chromosome.match(fusion_point__lte=end_point):
            if fusion.at_chromosome.filter(id__exact=chromos):
                fusions.append(fusion)
    
    rows = build_rows(fusions)
#     print(rows)
    
    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_single_gene(request, gene_one, c_line):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []

    if c_line == "ALL":
        for fusion in Gene.nodes.get(symbol = gene_one).had:
#             print(fusion)
            fusions.append(fusion)
    else:
        for fusion in CellLine.nodes.get(cell_line = c_line).happen:
            if fusion.fromGeneToFusion.filter(symbol__exact=gene_one) or fusion.fromGeneToFusion.filter(gene_id__exact=gene_one) or fusion.with_gene.filter(symbol__exact=gene_one) or fusion.with_gene.filter(gene_id__exact=gene_one):
                fusions.append(fusion)
            
    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_pair_gene(request, gene_one, gene_two, c_line):
    print("search for pair gene")
    response = {}
    rows = []
    header = get_header()
    
    fusions = []

    # recupero fusioni nella linea cellulare
    if c_line == "ALL":
        for fusion in Gene.nodes.get(symbol = gene_one).had:
            if fusion.with_gene.filter(symbol__exact=gene_two):
#                 print(fusion)
                fusions.append(fusion)
    else:
        for fusion in CellLine.nodes.get(cell_line = c_line).happen:
            if (fusion.fromGeneToFusion.filter(symbol__exact=gene_one) and fusion.with_gene.filter(symbol__exact=gene_two)) or (fusion.fromGeneToFusion.filter(symbol__exact=gene_two) and fusion.with_gene.filter(symbol__exact=gene_one)):
                fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_single_exon(request,c_line,exon_one):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        if fusion.at_exon.filter(exon__exact=exon_one):
            fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_pair_exon(request,c_line,exon_one,exon_two):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        if fusion.at_exon.filter(exon__exact=exon_one) and fusion.at_exon.filter(exon__exact=exon_two):
            fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_single_transcript(request,c_line,transcript_one):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        for couple in fusion.with_trans_couple:
            if couple.fromTranscriptToCouple.filter(transcript__exact=transcript_one) or couple.with_other_transcript.filter(transcript__exact=transcript_one):
                fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_pair_transcript(request,c_line,transcript_one,transcript_two):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        for couple in fusion.with_trans_couple:
            if (couple.fromTranscriptToCouple.filter(transcript__exact=transcript_one) and couple.with_other_transcript.filter(transcript__exact=transcript_two)) or (couple.fromTranscriptToCouple.filter(transcript__exact=transcript_two) and couple.with_other_transcript.filter(transcript__exact=transcript_one)):
                fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def search_for_fusion_information(request,c_line,algorithm,fusion_description,predicted_effect1,predicted_effect2):
    response = {}
    rows = []
    header = get_header()
    
    # recupero fusioni nella linea cellulare
    fusions = []
    for fusion in CellLine.nodes.get(cell_line = c_line).happen:
        predicted_effect_1 = fusion.fromGeneToFusion.relationship(fusion.fromGeneToFusion.all()[0]).predicted_effect
        predicted_effect_2 = fusion.with_gene.relationship(fusion.with_gene.all()[0]).predicted_effect
        if (algorithm in fusion.fusion_finding_method) and (fusion_description in fusion.description) and (predicted_effect1 == predicted_effect_1) and (predicted_effect2 == predicted_effect_2):
            fusions.append(fusion)

    rows = build_rows(fusions)
#     print(rows)

    response['rows'] = {"header": header, "items": rows}
    return HttpResponse(json.dumps(response))

def build_rows(fusions):
    rows = []
    # ora che ho solo le fusioni interessate recupero le informazioni e mi costruisco la riga
    for myfusion in fusions:
        # recupero cell line
        cellLine = myfusion.fromFusionToCellLine.all()[0].cell_line
        
        #recupero dati dai geni
        gene1 = myfusion.fromGeneToFusion.all()[0]
        strand_1 = myfusion.fromGeneToFusion.relationship(gene1).strand
        predicted_effect_1 = myfusion.fromGeneToFusion.relationship(gene1).predicted_effect
        gene2 = myfusion.with_gene.all()[0]
        strand_2 = myfusion.with_gene.relationship(gene2).strand
        predicted_effect_2 = myfusion.with_gene.relationship(gene2).predicted_effect

        #recupero cromosomi 
        chromosome1 = []
        chromosome2 = []
        fusion_point_1 = ''
        fusion_point_2 = ''
        for chrom in myfusion.at_chromosome:
            if chrom.of_gene.filter(symbol__exact=gene1.symbol):
                fusion_point_1 = myfusion.at_chromosome.relationship(chrom).fusion_point
                chromosome1 = chrom
            if chrom.of_gene.filter(symbol__exact=gene2.symbol):
                fusion_point_2 = myfusion.at_chromosome.relationship(chrom).fusion_point
                chromosome2 = chrom

        #recupero esoni
        exon1 = []
        exon2 = []
#         fusion_partner_1 = ''
#         fusion_partner_2 = ''
        for exon in myfusion.at_exon:
            if exon.in_gene.filter(symbol__exact=gene1.symbol):
#                 fusion_partner_1 = myfusion.at_exon.relationship(exon).fusion_partner
                exon1 = exon
            if exon.in_gene.filter(symbol__exact=gene2.symbol):
#                 fusion_partner_2 = myfusion.at_exon.relationship(exon).fusion_partner
                exon2 = exon
                
        #recupero trascritti e proteine
        transcript_couples = []
        proteins = []
        for couple in myfusion.with_trans_couple:
            transcript1 = couple.fromTranscriptToCouple.all()[0]
#             print(transcript1)
            transcript1_position = couple.fromTranscriptToCouple.relationship(transcript1).position
            transcript2 = couple.with_other_transcript.all()[0]
#             print(transcript2)
            transcript2_position = couple.with_other_transcript.relationship(transcript2).position
            
            transcript_couples.append(transcript1.transcript+":"+str(transcript1_position)+" - "+transcript2.transcript+":"+str(transcript2_position))
            proteins.append(couple.with_protein.all()[0].protein)
            
        #costruisco la riga
        row = []
        row.append(cellLine)
        row.append(gene1.symbol+" - "+gene2.symbol)
        row.append(str(gene1.gene_id)+" - "+str(gene2.gene_id))
        if exon1 or exon2:
            row.append(str(exon1.exon)+" - "+str(exon2.exon))
        else:
            row.append("No exons")
        row.append(str([str(chromosome1.chromosome)+":"+str(fusion_point_1)+":"+str(strand_1), str(chromosome2.chromosome)+":"+str(fusion_point_2)+":"+str(strand_2)]))
        row.append(myfusion.description)
        row.append(myfusion.common_mapping_reads)
        row.append(myfusion.spanning_pairs)
        row.append(myfusion.spanning_unique_reads)
        row.append(myfusion.longest_anchor_found)
        row.append(myfusion.fusion_finding_method)
        row.append(myfusion.fusion_sequence)
        if(predicted_effect_1!=predicted_effect_2):
            row.append(predicted_effect_1+"/"+predicted_effect_2)
        else:
            row.append(predicted_effect_1)
        row.append(transcript_couples)
        row.append(proteins)

        rows.append(row)
    return rows

def cell_lines(request):
    response = []

    response.append("ALL")
    
    for cell_line in CellLine.nodes.all():
        response.append(cell_line.cell_line)
        
    return HttpResponse(json.dumps(response))

def statistics_all(request):
    response = {}

    header = ['Fusion events', 'Transcripts', 'Genes', 'Predicted proteins', 'Exons', 'Viruses']
    rows = []
    response['details'] = {"header": header, "items": rows}
    fusion_events = 90319 # len(Fusion.nodes.all())
    transcripts = 25626 # len(Transcript.nodes.all())
    genes = 15601 # len(Gene.nodes.all())
    protein = 36828 # len(Protein.nodes.all())
    exon = 12976 # len(Exon.nodes.all())
    virus = 2793 # len(Virus.nodes.all())
    
    rows.append([fusion_events, transcripts, genes, protein, exon, virus])

    return HttpResponse(json.dumps(response))

def statistics_by_chromosome(request, chrom):
    response = {}
 
    header = ['Fusion events', 'Transcripts', 'Genes', 'Predicted proteins', 'Exons', 'Viruses']
    rows = []
    response['details'] = {"header": header, "items": rows}
    
    fusion_events = []
    transcripts = []
    genes = []
    proteins = []
    exons = []
    viruses = []
    
    node = Chromosome.nodes.get(chromosome = chrom)
    
    for fusion in node.fromFusiontoChromosome:
        
        fusion_events.append(fusion)
        
        for exon in fusion.at_exon:
            exons.append(exon)
            
        for gene in fusion.with_gene:
            genes.append(gene)
        
        for couple in fusion.with_trans_couple:
            for protein in couple.with_protein:
                proteins.append(protein)
            for transcript in couple.fromTranscriptToCouple:
                transcripts.append(transcript)
        
        for cell_line in fusion.fromFusionToCellLine:
            for virus in cell_line.with_viruses:
                viruses.append(virus)
                
    rows.append([len(fusion_events), len(transcripts), len(Set(genes)), len(proteins), len(exons), len(viruses)])
 
    return HttpResponse(json.dumps(response))

def sort_chromosomes(c):
    try:
        return int(c)
    except ValueError:
        return c
    
def fusion_by_chromosome(request):
    response = {}
    
    header = []
    rows = []
    
    response['details'] = {"header": header, "items": rows}
    
    chromosomes = Chromosome.nodes.all()
    sorted_chromosomes = sorted(chromosomes, key=lambda c: sort_chromosomes(c.chromosome))
    
    for chrom in sorted_chromosomes:
        
        header.append("chr " + chrom.chromosome)
        rows.append(len(chrom.fromFusiontoChromosome))
        
    return HttpResponse(json.dumps(response))

def download_data(request):
    
    response = {}

    header = ['Cell line', 'Fusion gene', 'Viruses', 'Summary']
    rows = []
    response['details'] = {"header": header, "items": rows}
    
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    for cell in CellLine.nodes.all():
        cell_line_id = cell.cell_line
        
#         size_bytes = os.path.getsize(url)
#         size_converted = size_bytes
#         size_human_index = 0
#         
#         while size_converted/1024 > 1:
#             size_converted = size_converted / 1024
#             size_human_index += 1
#         
#         size_human = size_converted + " " + sizes[size_human_index]
        
        rows.append([
            cell_line_id,
            {"label": "candidate fusion genes",
             "url": "downloads/cells/" + cell_line_id + ".txt"},
            {"label": "viruses bacteria phages",
             "url": "downloads/viruses/" + cell_line_id + ".txt"},
            {"label": "summary",
             "url": "downloads/summary/" + cell_line_id + ".txt"}])

    return HttpResponse(json.dumps(response))

def generate_statistics(request):
    
#     pairs = {
#         CellLine:('CellLine','cell_line'),
#         Fusion:('Fusion','fusion_id'),
#         Chromosome:('Chromosome','chromosome'),
#         Gene:('Gene','symbol'),
#         Transcript: ('Transcript', 'transcript'),
#         Protein: ('Protein', 'protein'),
#         Exon: ('Exon', 'exon'),
#         Virus: ('Virus', 'name')
#         }
#     
#     for node1,node_data1 in pairs.items():
# #         if node1 == Gene: continue
# #         if node1 == CellLine: continue
#         if node1 != Chromosome: continue
#         
#         for node2,node_data2 in pairs.items():
#             if node1 != node2:
#                 print(node_data1[0],node_data2[0])
#                 
#                 filename = os.path.dirname(__file__) + "/statistics/" + node_data1[0]+'_'+node_data2[0]+'.csv' 
#                 file =  open(filename,'w')
#                 writer = csv.writer(file, lineterminator='\n')
#                 writer.writerow([node_data1[0],node_data2[0]])
#                 for x in node1.nodes.all():
#                     print(x, node_data2[0])
#                     query = "match (x:"+node_data1[0]+"{"+node_data1[1]+":'"+str(eval("x."+str(node_data1[1])))+"'})-[*..2]-(y:"+str(node_data2[0])+") return x, count(distinct y)"
#                     if(db.cypher_query(query)[0]): #ho la linea cellulare vuota, machecazz?
#                         #print([db.cypher_query(query)[0][0][0].properties[eval("'"+node_data1[1]+"'")],db.cypher_query(query)[0][0][1]])
#                         writer.writerow([db.cypher_query(query)[0][0][0].properties[eval("'"+node_data1[1]+"'")],db.cypher_query(query)[0][0][1]])
#                 file.close()

    infos = get_ccle_infos()
    distribution = {}
    for row in infos["items"]:
        disease = row[2]
        
        if disease not in distribution:
            distribution[disease] = 0
            
        distribution[disease] += 1
        
    filename = os.path.dirname(__file__) + "/statistics/Disease_CellLine.csv"
    file = open(filename,'w') 
    writer = csv.writer(file, lineterminator='\n')
    writer.writerow(["Disease", "CellLine"])
    for disease in distribution:
        writer.writerow([disease, distribution[disease]])
    file.close()
    
    return HttpResponse()

def get_header():
    return ["Cell line",
        "Gene pair symbols",
        "Gene pair EnsIDs",
        "Exon pair",
        "Chromosome : fusion point : strand",
        "Description",
        "Counts of common mapping reads",
        "Spanning pairs",
        "Spanning unique reads",
        "Longest anchor found",
        "Fusion finding method",
        "Fusion sequence",
        "Predicted effect",
        "Predicted fused transcripts",
        "Predicted fused proteins"]

def get_ccle_infos():
    header = ["ID","Cell Line","Disease","Disease name"]
    rows = []
    
    txt_file = open(os.path.dirname(__file__) + "/ccle_ids.txt", "r")
    next(txt_file)
    for line in txt_file:
        words = line.split("\t")
        rows.append([words[0].replace(" ",""),words[1],words[2],words[3].replace("\n","")])
        #print(words)
    
    response = {"header": header, "items": rows}

#     print(response)
    
    return response

    #prendo in input una stringa che <E8> il nome della malattia, mi ricavo le linee cellulari corrispondenti e mi ricavo la tabella relativa
def get_cell_line_from_disease(disease):
    ccle_infos = get_ccle_infos()["items"]
    
    cls = []
    for row in ccle_infos:
        if disease in row:
            cls.append(row[0])
    
    return cls

def search_for_disease(request, disease):
    cls = get_cell_line_from_disease(disease)
    fusions = []
    
    response = {}
    header = get_header()
    
    for cl in cls:
        
        for fusion in CellLine.nodes.get(cell_line = cl).happen:
            fusions.append(fusion)
        
    rows = build_rows(fusions)
    
    response['rows'] = {"header": header, "items": rows}    
        
    return HttpResponse(json.dumps(response))

def get_distribution(request, node1, node2, howmany, sorting):
    
    if not howmany: howmany = -1
    howmany = int(howmany)
    
    response = {}
    labels = []
    header = []
    items = []
    
    lines = open(os.path.dirname(__file__) + "/statistics/" + node1 + "_" + node2 + ".csv")
    line_no = 0
    for line in lines:
        line_no += 1
        line = line.rstrip()
        fields = line.split(",")
        if line_no == 1:
            labels = fields
            continue
        
        header.append(fields[0])
        items.append(fields[1])
    lines.close()
    
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
    
    response['details'] = {"labels": labels, "header": header, "items": items}
    
    return HttpResponse(json.dumps(response))

def get_single_distribution(request, label, value):
    
    response = {}
    header = []
    items = []
    
    files = glob.glob(os.path.dirname(__file__) + "/statistics/" + label + "_*.csv")
    
    for filename in files:
        lines = open(filename)

        line_no = 0
        
        for line in lines:
            line_no += 1
            line = line.rstrip()
            fields = line.split(",")
            
            if line_no == 1:
                header_fields = fields
                continue
            
            if fields[0] == value:
                header.append(header_fields[1])
                items.append(fields[1])
                break
            
        lines.close()
    
#     header, items = zip(*sorted(zip(header, items), key=lambda pair: (not pair[0].isdigit(), pair[0].zfill(3))))
    
    response['details'] = {"header": header, "items": items}
    
    return HttpResponse(json.dumps(response))

