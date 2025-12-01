"""
Configuration for Member 1: Entity and Relation Type Definitions
"""

# Entity types to extract from biomedical space research papers
ENTITY_TYPES = [
    "gene",           # Gene names (TP53, BRCA1, FYN, etc.)
    "protein",        # Protein names
    "organism",       # Model organisms (mouse, rat, drosophila, Arabidopsis, human)
    "condition",      # Experimental conditions (microgravity, radiation, hindlimb unloading)
    "tissue",         # Tissues and organs (heart, bone, liver, muscle, brain)
    "process",        # Biological processes (oxidative stress, apoptosis, bone resorption)
    "assay",          # Experimental techniques (RNA-seq, qPCR, Western blot, flow cytometry)
    "disease",        # Diseases and pathological conditions
    "cell_type",      # Cell types (osteoblast, osteoclast, stem cell, T cell)
    "chemical"        # Chemicals and drugs
]

# Relation types for knowledge graph edges
RELATION_TYPES = [
    "affects",            # X affects Y (microgravity affects muscle mass)
    "associated_with",    # X is associated with Y (radiation associated with oxidative stress)
    "expressed_in",       # X is expressed in Y (TP53 expressed in heart tissue)
    "regulates",          # X regulates Y (gene A regulates gene B)
    "used_in",            # X used in Y (RNA-seq used in mouse studies)
    "increases",          # X increases Y
    "decreases",          # X decreases Y
    "induces",            # X induces Y (microgravity induces bone loss)
    "inhibits",           # X inhibits Y
    "causes",             # X causes Y
    "measured_in",        # X measured in Y (protein expression measured in tissue)
    "part_of",            # X is part of Y (gene part of pathway)
]

# Space biology specific keywords for condition entity extraction
SPACE_CONDITIONS = [
    "microgravity", "µg", "μg", "spaceflight", "space flight",
    "simulated microgravity", "real microgravity", 
    "hindlimb unloading", "HLU", "tail suspension",
    "radiation", "cosmic radiation", "space radiation", "ionizing radiation",
    "ISS", "International Space Station",
    "parabolic flight", "clinostat", "random positioning machine", "RPM",
    "hypergravity", "centrifugation",
    "space environment", "space conditions"
]

# Common synonyms for normalization
ENTITY_SYNONYMS = {
    # Space conditions
    "µg": "microgravity",
    "μg": "microgravity",
    "space flight": "spaceflight",
    "simulated microgravity": "microgravity_simulated",
    "real microgravity": "microgravity_real",
    
    # Biological processes (common abbreviations)
    "ROS": "reactive oxygen species",
    "oxidative stress": "oxidative_stress",
    
    # Techniques
    "qPCR": "quantitative PCR",
    "RT-PCR": "reverse transcription PCR",
    "RNA-seq": "RNA sequencing",
    
    # Model organisms
    "mice": "mouse",
    "rats": "rat",
}

# Patterns for relation extraction (will be used in relation_pipeline.py)
RELATION_PATTERNS = {
    "affects": [
        r"\b(\w+)\s+affects?\s+(\w+)",
        r"\b(\w+)\s+impact[s]?\s+(\w+)",
        r"\b(\w+)\s+influence[s]?\s+(\w+)"
    ],
    "increases": [
        r"\b(\w+)\s+increase[s|d]?\s+(\w+)",
        r"\b(\w+)\s+elevate[s|d]?\s+(\w+)",
        r"\b(\w+)\s+upregulate[s|d]?\s+(\w+)",
        r"\b(\w+)\s+enhance[s|d]?\s+(\w+)"
    ],
    "decreases": [
        r"\b(\w+)\s+decrease[s|d]?\s+(\w+)",
        r"\b(\w+)\s+reduce[s|d]?\s+(\w+)",
        r"\b(\w+)\s+downregulate[s|d]?\s+(\w+)",
        r"\b(\w+)\s+inhibit[s|ed]?\s+(\w+)",
        r"\b(\w+)\s+suppress[es|ed]?\s+(\w+)"
    ],
    "induces": [
        r"\b(\w+)\s+induce[s|d]?\s+(\w+)",
        r"\b(\w+)\s+trigger[s|ed]?\s+(\w+)",
        r"\b(\w+)\s+promote[s|d]?\s+(\w+)"
    ],
    "associated_with": [
        r"\b(\w+)\s+associated with\s+(\w+)",
        r"\b(\w+)\s+linked to\s+(\w+)",
        r"\b(\w+)\s+correlated with\s+(\w+)",
        r"\b(\w+)\s+related to\s+(\w+)"
    ],
    "causes": [
        r"\b(\w+)\s+cause[s|d]?\s+(\w+)",
        r"\b(\w+)\s+lead[s]? to\s+(\w+)",
        r"\b(\w+)\s+result[s]? in\s+(\w+)"
    ]
}
