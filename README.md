# gtex
This repo contains scripts for parsing gtex data

## Parse .gct file
- Parsing .gct tmp file from gtex (https://storage.googleapis.com/gtex_analysis_v8/rna_seq_data/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz)
- Download: `wget https://storage.googleapis.com/gtex_analysis_v8/rna_seq_data/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz`
- Unzip: `gunzip GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz`
1. File format:
- First line: #1.2
- Second line: 56200   17382
- Third line: header, starting with Name (transcript name), Description (gene name), and then sample ID
- Rmoving the first two lines:
  ```
  tail -n +3 GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct > GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct
  ```
- The file `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct` stores tpm values for each transcript for each sample
2. Subset 
- Let's say that you only want the tpm values for a subset of samples. Here I will describe how to subset the original file to contain just the samples of interest. 
- The samples you want to subset are listed (each sample per line) in a file. The example file here is `test_sample.txt`. 
- Use the python script `subset_tpm.py`. Usage is:
  ```
  python subset_tpm.py -h
  usage: subset_tpm.py [-h] --tpm_gct_file TPM_GCT_FILE --sample_list_file
                     SAMPLE_LIST_FILE --output_file OUTPUT_FILE

  Subset tpm gct file for a subset of samples.

  optional arguments:
  -h, --help            show this help message and exit
  --tpm_gct_file TPM_GCT_FILE
                        Input the path to the tpm gct file (unzip).
  --sample_list_file SAMPLE_LIST_FILE
                        Input the path to the list of samples. Each sample is
                        a line.
  --output_file OUTPUT_FILE
                        Input the path to the output file.
  ```
 - This is how one would run this script:
  ```
  python subset_tpm.py --tpm_gct_file GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct --sample_list_file test_sample.txt --output_file test_sample_tpm.tsv
  ```
