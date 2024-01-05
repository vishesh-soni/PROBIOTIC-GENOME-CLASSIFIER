import sys
import math
import zipfile
import os
import tempfile
import secrets
import string

def generate_random_string(length):
    # Define the character set for the random string
    characters = string.ascii_letters + string.digits

    # Generate a random string of the specified length
    random_string = ''.join(secrets.choice(characters) for _ in range(length))

    return random_string

def unzip_and_list_files(zip_file_path, extract_to):
    # Create the specified directory if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)

    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all the contents of the zip file to the specified directory
            zip_ref.extractall(extract_to)

            # Get the list of files in the zip file with full paths
            file_list = [os.path.join(extract_to, file) for file in zip_ref.namelist()]

        # Return the list of files and the extraction directory path
        return file_list, extract_to

    except zipfile.BadZipFile:
        # Handle the case where the provided file is not a valid zip file
        print(f"The file '{zip_file_path}' is not a valid zip file.")
        return [], None

def read_fasta_sequence (numeric,
                         fasta_file):

    # Read 1 byte.  
    first_char = fasta_file.read(1)
    # If it's empty, we're done.
    if (first_char == ""):
        return(["", ""])
    # If it's ">", then this is the first sequence in the file.
    elif (first_char == ">"):
        line = ""
    else:
        line = first_char

    # Read the rest of the header line.
    line = line + fasta_file.readline()

    # Get the rest of the ID.
    words = line.split()
    if (len(words) == 0):
      sys.stderr.write("No words in header line (%s)\n" % line)
      sys.exit(1)
    id = words[0]
        
    # Read the sequence, through the next ">".
    first_char = fasta_file.read(1)
    sequence = ""
    while ((first_char != ">") and (first_char != "")):
        if (first_char != "\n"): # Handle blank lines.
            line = fasta_file.readline()
            sequence = sequence + first_char + line
        first_char = fasta_file.read(1)

    # Remove EOLs.
    clean_sequence = ""
    for letter in sequence:
        if (letter != "\n"):
            clean_sequence = clean_sequence + letter
    sequence = clean_sequence

    # Remove spaces.
    if (numeric == 0):
        clean_sequence = ""
        for letter in sequence:
            if (letter != " "):
                clean_sequence = clean_sequence + letter
        sequence = clean_sequence.upper()
        
    return([id, sequence])


def compute_quantile_boundaries (num_bins,
                                 k_values,
                                 number_filename):

    if (num_bins == 1):
        return

    # The boundaries are stored in a 2D dictionary.
    boundaries = {}
#     print(k_values)

    # Enumerate all values of k.
    for k in k_values:

        # Open the number file for reading.
        number_file = open(number_filename, "r")
        
        # Read it sequence by sequence.
        all_numbers = []
        [id, numbers] = read_fasta_sequence(1, number_file)
        while (id != ""):
            
            # Compute and store the mean of all k-mers.
            number_list = numbers.split()
            num_numbers = len(number_list) - k
            for i_number in range(0, num_numbers):
                if (i_number == 0):
                    sum = 0;
                    for i in range(0, k):
                        sum += float(number_list[i])
                else:
                    sum -= float(number_list[i_number - 1])
                    sum += float(number_list[i_number + k - 1])
                all_numbers.append(sum / k)
            [id, numbers] = read_fasta_sequence(1, number_file)
        number_file.close()

        # Sort them.
        all_numbers.sort()

        # Record the quantiles.
        boundaries[k] = {}
        num_values = len(all_numbers)
        bin_size = float(num_values) / float(num_bins)
        sys.stderr.write("boundaries k=%d:" % k)
        for i_bin in range(0, num_bins):
            value_index = int((bin_size * (i_bin + 1)) - 1)
            if (value_index == num_bins - 1):
                value_index = num_values - 1
            value = all_numbers[value_index]
            boundaries[k][i_bin] = value
            sys.stderr.write(" %g" % boundaries[k][i_bin])
        sys.stderr.write("\n")

    return(boundaries)

upto = 1
revcomp = 0
normalize_method = "none"
alphabet = "ACGT"
mismatch = 0
num_bins = 1
pseudocount = 0
number_filename = ""

k = 8
# fasta_filename = "E:\chrome downloads\sequence.fasta"

# Check for reverse complementing non-DNA alphabets.
# if ((revcomp == 1) and (alphabet != "ACGT")):
#     sys.stderr.write("Attempted to reverse complement ")
#     sys.stderr.write("a non-DNA alphabet (%s)\n" % alphabet)

# Make a list of all values of k.
k_values = []
if (upto == 1):
    start_i_k = 1
else:
    start_i_k = k
k_values = range(start_i_k, k+1)
print(k_values)

# If numeric binning is turned on, compute quantile boundaries for various
# values of k.
boundaries = compute_quantile_boundaries(num_bins, k_values, number_filename)
print(boundaries)

def make_kmer_list(k, alphabet):

    # Base case.
    if (k == 1):
        return(alphabet)

    # Handle k=0 from user.
    if (k == 0):
        return([])

    # Error case.
    if (k < 1):
        sys.stderr.write("Invalid k=%d" % k)
        sys.exit(1)

    # Precompute alphabet length for speed.
    alphabet_length = len(alphabet)

    # Recursive call.
    return_value = []
    for kmer in make_kmer_list(k-1, alphabet):
        for i_letter in range(0, alphabet_length):
            return_value.append(kmer + alphabet[i_letter])
              
    return(return_value)

def make_upto_kmer_list (k_values,
                         alphabet):

    # Compute the k-mer for each value of k.
    return_value = []
    for k in k_values:
        return_value.extend(make_kmer_list(k, alphabet))

    return(return_value)

mer_list = make_upto_kmer_list(k_values, alphabet)
import pandas as pd

def generate_kmers(sequence, k):
    kmers = [sequence[i:i + k] for i in range(len(sequence) - k + 1)]
    return kmers

def count_kmers_in_sequence(sequence, kmer_list):
    kmer_counts = {kmer: sequence.count(kmer) for kmer in kmer_list}
    return kmer_counts

def fasta_to_dataframe(fasta_file, kmer_list):
    with open(fasta_file, 'r') as file:
        lines = file.readlines()

    accession = lines[0].strip().lstrip('>')
    sequence = ''.join([line.strip() for line in lines[1:]])

    kmer_counts = count_kmers_in_sequence(sequence, kmer_list)

    return kmer_counts

def process_multiple_sequences(fasta_files, kmer_list):
    data = {}

    for fasta_file in fasta_files:
        with open(fasta_file, 'r') as file:
            lines = file.readlines()

        accession = lines[0].strip().lstrip('>')
        sequence = ''.join([line.strip() for line in lines[1:]])

        kmer_counts = count_kmers_in_sequence(sequence, kmer_list)
        kmer_counts['Assembly Accession'] = accession  # Add Accession column
        data[accession] = kmer_counts

    result_df = pd.DataFrame(data).T
    # result_df.index.name = 'Assembly Accession'
    result_df.columns.name = 'kmer'

    return result_df