import os

configfile: "/scratch/tphung3/SmallProjects/ParseGtex/gtex_version8_config.json"

rule all:
    input:
        expand("{tissue}_gtex_version8_config.json", tissue=config["tissues"])


rule find_sample_ids_for_each_tissue:
    input:
    output:
        "{tissue}_gtex_version8_config.json"
    params:
        tissue = "{tissue}",
        script = "/scratch/tphung3/SmallProjects/ParseGtex/find_sample_ids_for_each_tissue.py"
    shell:
        """
        python {params.script} --tissue "{params.tissue}" --output_filepath "{output}"
        """
