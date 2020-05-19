import json
import pandas as pd
import sys
import os

import argparse

parser = argparse.ArgumentParser(description='Generate a config file for each tissue from GTEX version 8.\n'
                                             '(1): {tissue}: a list of sample ids for this tissue\n'
                                             '(2): {tissue}_female: a list of sample ids for this tissue that are female\n'
                                             '(3): {tissue}_male: a list of sample ids for this tissue that are male\n'
                                             '(4): {tissue}_with_TPM: a list of sample ids for this tissue that have TPM values\n'
                                             '(5): {tissue}_female_with_TPM: a list of sample ids for this tissue that are female that have TPM value\n'
                                             '(6): {tissue}_male_with_TPM: a list of sample ids for this tissue that are male that have TPM value')
parser.add_argument('--tissue',required=True,help='Input the tissue name with quote. For example: "Whole Blood"')
parser.add_argument('--output_filepath',required=True,help='Input the path to the output file')

args = parser.parse_args()

tissue = args.tissue #obtain the name of the tissue from the command line

tissue_data = {}
tissue_data[tissue] = [] #This is a list of sample ids for this tissue

# 1. Find all sample ids for this tissue
data = pd.read_csv('/scratch/tphung3/SmallProjects/ParseGtex/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt', sep='\t') #read in the attribute files as a panda dataframe
data_tissue_subset = data[data['SMTSD'] == tissue] #subset for the tissue
for i in data_tissue_subset['SAMPID']:
    tissue_data[tissue].append(i)

# 2. Find sample ids that are females or males for this tissue
phenotypes = pd.read_csv('/scratch/tphung3/SmallProjects/ParseGtex/GTEx_Analysis_v8_Annotations_SubjectPhenotypesDS.txt', sep='\t') #read in the phenotype file that has sex information
females_phenotypes = phenotypes[phenotypes['SEX'] == 2]
females_id = set()
for i in females_phenotypes['SUBJID']:
    females_id.add(i)

males_phenotypes = phenotypes[phenotypes['SEX'] == 1]
males_id = set()
for i in males_phenotypes['SUBJID']:
    males_id.add(i)

tissue_female_str = tissue + '_female'
tissue_data[tissue_female_str] = [] #This is a list of sample ids that are female for this tissue

tissue_male_str = tissue + '_male'
tissue_data[tissue_male_str] = [] #This is a list of sample ids that are male for this tissue

for i in tissue_data[tissue]:
    items = i.split('-')
    id = items[0] + '-' + items[1]
    if id in females_id:
        tissue_data[tissue_female_str].append(i)
    elif id in males_id:
        tissue_data[tissue_male_str].append(i)
    else:
        print ('Cannot find the sex information for sample ' + i)

# 3. Find sample ids that have TPM values
sample_ids_with_tpm = set()
with open('/scratch/tphung3/SmallProjects/ParseGtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct') as f:
    first_line = f.readline()
    for sample in first_line.rstrip('\n').split('\t')[2:]:
        sample_ids_with_tpm.add(sample)

tissue_with_tpm_str = tissue + '_with_TPM'
tissue_data[tissue_with_tpm_str] = [] #This is a list of sample ids for this tissue that have TPM values
for i in tissue_data[tissue]:
    if i in sample_ids_with_tpm:
        tissue_data[tissue_with_tpm_str].append(i)

tissue_female_with_tpm_str = tissue + '_female_with_TPM'
tissue_data[tissue_female_with_tpm_str] = [] #This is a list of sample ids for this tissue that are female that have TPM value
for i in tissue_data[tissue_female_str]:
    if i in sample_ids_with_tpm:
        tissue_data[tissue_female_with_tpm_str].append(i)

tissue_male_with_tpm_str = tissue + '_male_with_TPM'
tissue_data[tissue_male_with_tpm_str] = [] #This is a list of sample ids for this tissue that are male that have TPM value
for i in tissue_data[tissue_male_str]:
    if i in sample_ids_with_tpm:
        tissue_data[tissue_male_with_tpm_str].append(i)

# Save the number of samples in each categories to a file

out = [tissue, str(len(tissue_data[tissue])), str(len(tissue_data[tissue_female_str])), str(len(tissue_data[tissue_male_str])), str(len(tissue_data[tissue_with_tpm_str])), str(len(tissue_data[tissue_female_with_tpm_str])), str(len(tissue_data[tissue_male_with_tpm_str]))]

if os.path.exists('/scratch/tphung3/SmallProjects/ParseGtex/number_of_samples.csv'):
    outfile = open('/scratch/tphung3/SmallProjects/ParseGtex/number_of_samples.csv', 'a')
    print (','.join(out), file=outfile)

else:
    outfile = open('/scratch/tphung3/SmallProjects/ParseGtex/number_of_samples.csv', 'w')
    header = ['tissue', 'n_sample', 'n_sample_female', 'n_sample_male', 'n_sample_TPM', 'n_sample_female_TPM', 'n_sample_male_TPM']
    print(','.join(header), file=outfile)
    print(','.join(out), file=outfile)


with open(args.output_filepath, 'w') as outfile:
    json.dump(tissue_data, outfile)
