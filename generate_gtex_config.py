import json
import pandas as pd
import gzip

class FindSamplesPerTissue:
    def __init__(self, tissue_name, tissue_config_json):
        self.tissue_name = tissue_name
        self.tissue_config_json = tissue_config_json
        self.SampleAttributesDS_df = pd.read_csv("data/manifest/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt", sep="\t")
        self.SubjectPhenotypesDS = pd.read_csv("data/manifest/GTEx_Analysis_v8_Annotations_SubjectPhenotypesDS.txt", sep="\t")

    def generate_config(self): #TODO: add with TPM samples
        tissue_data = {}

        # All samples
        tissue_subset = self.SampleAttributesDS_df[self.SampleAttributesDS_df["SMTSD"] == self.tissue_name]
        tissue_data["all_samples"] = [i for i in tissue_subset["SAMPID"]]

        # Stratify by sex
        females = self.SubjectPhenotypesDS[self.SubjectPhenotypesDS["SEX"] == 2]
        males = self.SubjectPhenotypesDS[self.SubjectPhenotypesDS["SEX"] == 1]

        females_id = {i.split("-")[1] for i in females["SUBJID"]} #make a set of all the females
        tissue_data["females"] = [i for i in tissue_data["all_samples"] if i.split("-")[1] in females_id]

        males_id = {i.split("-")[1] for i in males["SUBJID"]} #make a set of all the males
        tissue_data["males"] = [i for i in tissue_data["all_samples"] if i.split("-")[1] in males_id]

        # Check if the samples have RNAseq, then stratify by sex
        with gzip.open("data/counts/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.gct.gz", "rt") as f:
            for line in f:
                if line.startswith("Name"):
                    has_rnaseq_samples = {i for i in line.rstrip("\n").split("\t")}
                    break

        tissue_data["all_samples_has_rnaseq"] = [i for i in tissue_data["all_samples"] if i in has_rnaseq_samples]
        tissue_data["females_has_rnaseq"] = [i for i in tissue_data["females"] if i in has_rnaseq_samples]
        tissue_data["males_has_rnaseq"] = [i for i in tissue_data["males"] if i in has_rnaseq_samples]

        with open(self.tissue_config_json, "w") as outfile:
            json.dump(tissue_data, outfile)


def main():
    with open("data/manifest/GTEx_Portal.csv", "r") as f:
        tissues = [line.rstrip("\n").split(",")[0].strip('"') for line in f if not line.startswith('"Tissue"')] #tissues names in GTEx such as Whole Blood

        # generating a config file for all of the gtex tissues.
        # Reformat the tissue name to remove space: from Skin - Sun Exposed (Lower leg) to Skin-SunExposed(Lowerleg)
        data = {}
        data["tissue_name"] = ["".join(i for i in tissue.split(" ")) for tissue in tissues]
        with open("config/gtex_tissue_name_config.json", "w") as outfile:
            json.dump(data, outfile)


        tissues_instances = [FindSamplesPerTissue(tissue, "config/" + "".join(i for i in tissue.split(" ")) + "_config.json") for tissue in
                            tissues]

        for tissue in tissues_instances:
            tissue.generate_config()

main()