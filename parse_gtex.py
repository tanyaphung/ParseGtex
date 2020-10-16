import pandas as pd
import argparse
import subprocess
import json

class ParseRna:
    def __init__(self, gtex_counts_path):
        self.gtex_counts_path = gtex_counts_path

    def return_all_samples(self):
        with open(self.gtex_counts_path, "r") as f:
            first_line = f.readline()
            return first_line.rstrip("\n").split("\t")[2:]

    def select_sample(self, sample, subset_sample_out):
        if sample in self.return_all_samples():
            self.select_samples([sample], subset_sample_out)
        else:
            print("The sample is not in the file to be subsetted. Exiting.")
            exit()

    def parse_samples(self, samples_file):
        missing_samples_outfile = open("missing_samples.txt", "w")
        with open(samples_file, "r") as f:
            samples_to_select = [line.rstrip("\n").split()[0] for line in f]
            samples_to_select_present = []
            all_samples = self.return_all_samples()
            for i in samples_to_select:
                if i in all_samples:
                    samples_to_select_present.append(i)
                else:
                    print(i, file=missing_samples_outfile)
            return samples_to_select_present

    def select_samples(self, samples_list, subset_samples_out):
        print(len(samples_list))
        if len(samples_list) != 0:
            data = pd.read_csv(self.gtex_counts_path, sep='\t', chunksize=1000)

            chunk_list = []  # to store all the chunks together
            for data_chunk in data:
                data_chunk_subset = data_chunk[["Name", "Description"] + samples_list]
                chunk_list.append(data_chunk_subset)

            data_subset = pd.concat(chunk_list) # concatenate all the chunks together

            data_subset.to_csv(subset_samples_out, sep="\t", index=False) # save to a file
        else:
            print("None of the samples are in the file to be subsetted. Exiting.")
            exit()

class ParseDna: #TODO: add handling of missing samples in the VCF file
    def __init__(self, vcf_path):
        self.vcf_path = vcf_path

    def select_sample(self, sample, subset_sample_out):
        command_line = "bcftools view -s {sample} {vcf_path} > {subset_vcf}".format(sample=sample, vcf_path=self.vcf_path, subset_vcf=subset_sample_out)
        subprocess.check_output(command_line, shell=True)

    def select_samples(self, samples_file, subset_sample_out):
        command_line = "bcftools view -S {samples_file} {vcf_path} > {subset_vcf}".format(samples_file=samples_file, vcf_path=self.vcf_path, subset_vcf=subset_sample_out)
        subprocess.check_output(command_line, shell=True)

def main(args):
    if args.data_type == "rna":
        if not args.gtex_file or not args.subset_samples_outfile:
            print("ERROR. Missing arguments for parsing the RNAseq data."
                  "To subset samples from the RNAseq tpm or count data, these arguments are required:"
                  "--gtex_file, --sample (for a sample), or --samples_file, and --subset_samples_outfile")
            exit()
        else:
            instance = ParseRna(args.gtex_file)
            if args.sample:
                instance.select_sample(args.sample, args.subset_samples_outfile)
            elif args.samples_file:
                instance.select_samples(instance.parse_samples(args.samples_file), args.subset_samples_outfile)
            elif args.config_file:
                with open(args.config_file) as json_file:
                    data = json.load(json_file)
                    for i in data:
                        if i == "all_samples_has_rnaseq": #TODO: change so that this is not hard-coded
                            instance.select_samples([sample for sample in data[i]], args.subset_samples_outfile)
            else:
                print("ERROR. Missing arguments for parsing the RNAseq data."
                      "You need to provide a sample name via --sample or a file with a list of samples via --samples_file or config file via --config.")
                exit()
    if args.data_type == "dna":
        if not args.vcf_file or not args.subset_samples_outfile:
            print("ERROR. Missing arguments for parsing DNAseq data."
                  "To subset samples from the DNAseq VCF data, these arguments are required:"
                  "--vcf_file, --sample (for a sample), or --samples_file, and --subset_samples_outfile")
            exit()
        else:
            instance = ParseDna(args.vcf_file)
            if args.sample:
                instance.select_sample(args.sample, args.subset_samples_outfile)
            elif args.samples_file:
                instance.select_samples(args.samples_file, args.subset_samples_outfile)
            else:
                print("ERROR. Missing arguments for parsing the DNAseq data."
                      "You need to provide a sample name via --sample or a file with a list of samples via --samples_file")



def parse_args():
    parser = argparse.ArgumentParser(description='Subset samples from GTEx RNAseq (TPM or raw counts) or from DNAseq (VCF file).')
    parser.add_argument('--data_type', required=True, help='Input either dna or rna')
    parser.add_argument('--gtex_file', required=False, help='Input the path to the tpm or count gct file (unzip).')
    parser.add_argument('--vcf_file', required=False, help='Input the path to the vcf file.')
    parser.add_argument('--samples_file', required=False,
                        help='Input the path to the list of samples. Each sample is a line.')
    parser.add_argument('--config_file', required=False,
                        help='')
    parser.add_argument('--sample', required=False, help='Input the sample id')
    parser.add_argument('--subset_samples_outfile', required=False, help='Input the path to the output file.')

    return parser.parse_args()
main(parse_args())