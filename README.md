## Directory structure
* The directory `data\` is not included in this github repo because of size, but the content is described below:
`data/` directory includes:
- `data/manifest`:
    + `GTEx_Analysis_v8_Annotations_SubjectPhenotypesDS.txt`
    + `GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt`
    + `participant.tsv`
    + `GTEx_Portal.csv`
- `data/counts`:
    + `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct`
    ```
    gunzip GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct.gz
    tail -n +3 GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm.gct > GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_tpm_clean.gct
    ```
    + `GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.gct`
- `data/vcf`:
    + `GTEx_Analysis_2017-06-05_v8_WholeExomeSeq_979Indiv_VEP_annot.vcf.gz`
    + `GTEx_Analysis_2017-06-05_v8_WholeExomeSeq_979Indiv_VEP_annot.vcf.gz.tbi`
    
## Generate config file
```
python generate_gtex_config.py
```
- The above script outputs: in the directory `config/`:
    + `gtex_tissue_name_config.json`: this is the config file for all the tissue names
    + `{tissue_name}_config.json` (example: `Muscle-Skeletal_config.json`): this is the config file for each tissue that includes the following list:
        + all_samples
        + females
        + males
        + all_samples_has_rnaseq
        + females_has_rnaseq
        + males_has_rnaseq
        
## Parsing GTEx data
- Script: `parse_gtex.py`
1. Subset samples from the GTEx TPM or raw count file:
- Example using liver where one specifies the samples to be subsetted via the config file
```
python parse_gtex.py --data rna --config config/Liver_config.json --gtex_file data/counts/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads_clean.gct --subset_samples_outfile Liver_counts.tsv
```
- Instead of providing the samples to be subsetted via the config file, you can also provide a sample via `--sample` or a file with each sample on a row via `--samples_file`

2. Subset samples from the VCF file:
- Example to subset an individual from the VCF file:
```
python parse_gtex.py --data dna --sample GTEX-1117F --vcf_file data/vcf/GTEx_Analysis_2017-06-05_v8_WholeExomeSeq_979Indiv_VEP_annot.vcf.gz --subset_samples_outfile GTEX-1117F.vcf
```