import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Subset tpm gct file for a subset of samples.')
parser.add_argument('--tpm_gct_file',required=True,help='Input the path to the tpm gct file (unzip).')
parser.add_argument('--sample_list_file',required=True,help='Input the path to the list of samples. Each sample is a line.')
parser.add_argument('--output_file',required=True,help='Input the path to the output file.')
parser.add_argument('--output_missing_samples',required=True,help='Input the path to the output file that lists the missing samples.')

args = parser.parse_args()

data = pd.read_csv(args.tpm_gct_file, sep='\t', chunksize=1000) #Load data into a pandas dataframe. Do this in chunks because the tpm file is large.

# Generate a list of samples of interest
sample_list = []
with open(args.sample_list_file, 'r') as f:
    for line in f:
        sample_list.append(line.rstrip('\n'))

chunk_list = [] #to store all the chunks together

missing_samples = set() #save a list of samples that were not found in the tpm file

# Pull out the sample of interest. If the sample is missing in the tpm file, save it in the missing_samples set
for data_chunk in data:
    data_chunk_subset = data_chunk[['Name', 'Description']]
    for sample in sample_list:
        try:
            sample_subset = data_chunk[[sample]]
            data_chunk_subset = data_chunk_subset.join(sample_subset)
        except:
            missing_samples.add(sample)
            continue
    chunk_list.append(data_chunk_subset)

data_subset = pd.concat(chunk_list) #concatenate all the chunks together

data_subset.to_csv(args.output_file, sep='\t', index=False) #save to a file

outfile = open(args.output_missing_samples, 'w') #save the missing samples in a file
for i in missing_samples:
    print (i, file=outfile)