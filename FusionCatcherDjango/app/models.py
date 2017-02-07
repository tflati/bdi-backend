from __future__ import unicode_literals

# Create your models here.
from neomodel import (StructuredNode, StructuredRel, StringProperty, IntegerProperty, ArrayProperty)
from neomodel.relationship_manager import RelationshipTo, RelationshipFrom

# Create your models here.

class File(StructuredNode):
    name = StringProperty()
    indels = StringProperty()
    snp = StringProperty()

   
class Statistics(StructuredNode):
    indels = StringProperty()
    snp = StringProperty()
    in_dbSNP = StringProperty()
    not_in_dbSNP = StringProperty()
    
    
#EDGES
class AT_CHROMOSOME(StructuredRel):
    fusion_point = IntegerProperty()

class AT_EXON(StructuredRel):
    fusion_partner = StringProperty()

class HAD(StructuredRel):
    predicted_effect = StringProperty()
    strand = StringProperty()
    
class IN_COUPLE(StructuredRel):
    position = IntegerProperty()
    
class WITH(StructuredRel):
    predicted_effect = StringProperty()
    strand = StringProperty()
    
class WITH_OTHER_TRANSCRIPT(StructuredRel):
    position = IntegerProperty()   
    
class WITH_VIRUSES(StructuredRel):
    count_of_mapping_reads = IntegerProperty()
    
class WITH_TRANSCRIPT(StructuredRel):
    pass
    
#NODES

class CellLine(StructuredNode):
    cell_line = StringProperty()
    #
    happen = RelationshipTo('Fusion',"HAPPEN")
    with_viruses = RelationshipTo('Virus',"WITH_VIRUSES",model=WITH_VIRUSES)
    
class Couple(StructuredNode):
    couple = IntegerProperty() 
    #
    with_other_transcript = RelationshipTo('Transcript',"WITH_OTHER_TRANSCRIPT", model=WITH_OTHER_TRANSCRIPT)
    with_protein = RelationshipTo('Protein',"WITH_PROTEIN")
    #
    fromTranscriptToCouple = RelationshipFrom('Transcript',"IN_COUPLE", model=IN_COUPLE)
    fromFusionToCouple = RelationshipFrom('Fusion',"WITH_TRANS_COUPLE")
    
class Chromosome(StructuredNode):
    chromosome = StringProperty()
    #
    of_gene = RelationshipTo('Gene',"OF_GENE")
    #
    fromFusiontoChromosome = RelationshipFrom('Fusion', "AT_CHROMOSOME", model=AT_CHROMOSOME)
    
class Exon(StructuredNode):
    exon = StringProperty()
    #
    in_gene = RelationshipTo('Gene',"IN_GENE")
    #
    fromFusionToExon = RelationshipFrom('Fusion', "AT_EXON", model=AT_EXON)
    
class Fusion(StructuredNode):
    fusion_id = IntegerProperty()
    description = ArrayProperty()
    common_mapping_reads = IntegerProperty()
    spanning_pairs = IntegerProperty()
    spanning_unique_reads = IntegerProperty()
    longest_anchor_found = IntegerProperty()
    fusion_finding_method = StringProperty()
    fusion_sequence = StringProperty()
    #
    at_chromosome = RelationshipTo('Chromosome', "AT_CHROMOSOME", model=AT_CHROMOSOME)
    at_exon = RelationshipTo('Exon', "AT_EXON", model=AT_EXON)
    with_trans_couple = RelationshipTo('Couple', "WITH_TRANSCRIPT", model=WITH_TRANSCRIPT)
    with_gene = RelationshipTo('Gene',"WITH", model=WITH)
    #
    #fromCellLineToFusion = RelationshipFrom('CellLine',"HAPPEN")
    fromGeneToFusion = RelationshipFrom('Gene', "HAD", model=HAD)
    fromFusionToCellLine = RelationshipFrom('CellLine', "HAPPEN")
    
class Gene(StructuredNode):
    gene_id = StringProperty()
    symbol = StringProperty()
    #
    had = RelationshipTo('Fusion', "HAD", model=HAD)
    #
    #fromFusion = RelationshipFrom('Fusion',"WITH", model=WITH)
    fromExonToGene = RelationshipFrom('Exon',"IN_GENE")
    fromChromosomeToGene = RelationshipFrom('Chromosome',"OF_GENE")
    
    def __eq__(self, other):
        return self.symbol == other.symbol
    
class Protein(StructuredNode):
    protein = StringProperty()
    #
    fromCoupleToProtein = RelationshipFrom('Couple',"WITH_PROTEIN")
    
class Transcript(StructuredNode):
    transcript = StringProperty()
    #
    in_couple = RelationshipTo('Couple',"IN_COUPLE", model=IN_COUPLE)
    #
    fromCoupleToTranscript = RelationshipFrom('Couple',"WITH_OTHER_TRANSCRIPT", model=WITH_OTHER_TRANSCRIPT)

    
class Virus(StructuredNode):
    name = StringProperty()
    gi = StringProperty()
    ref = StringProperty()
    #
    fromCellLineToVirus = RelationshipFrom('CellLine',"WITH_VIRUSES", model=WITH_VIRUSES)