import csv
import json

def read_csv_file(file_name):
    with open(file_name) as file:
        reader = csv.reader(file)
        records = list(reader)
    return records

def get_codon_mapping_dict():
    with open('codon_mapping.json') as f_in:
        return json.load(f_in)

def get_nucleotides(records, type):
    payload = []
    type_dict = {'wild_type': 1, 'bio_n_tech': 2}
    for row in records:
        payload.append(row[type_dict.get(type)])
    return payload[1:]

def is_guanine_or_cytosine(nucleotide):
    return nucleotide == 'G' or nucleotide == 'C'

all_nucleotides = read_csv_file('side-by-side.csv')
wild_type_covid_nucleotides = get_nucleotides(all_nucleotides, 'wild_type')
bio_n_tech_covid_nucleotides = get_nucleotides(all_nucleotides, 'bio_n_tech')

codon_mapping_dict = get_codon_mapping_dict()

my_vaccine_sequence = []

# generate my vaccine sequence
for codon in wild_type_covid_nucleotides:
    last_nucleotide = codon[2]
    if is_guanine_or_cytosine(last_nucleotide):
        my_vaccine_sequence.append(codon)
    else:
        convert_codon = str(codon_mapping_dict.get(codon))
        my_vaccine_sequence.append(convert_codon)

matches = []
differences = []

for idx, val in enumerate(my_vaccine_sequence):
    if my_vaccine_sequence[idx] == bio_n_tech_covid_nucleotides[idx]:
        matches.append(idx)
    else:
        differences.append(idx)

print('**** FASTA Sequence : ')
separator = ''
print(separator.join(my_vaccine_sequence))

total = len(my_vaccine_sequence)
percentage_similarity = (len(matches) / total) * 100
print('*****')
print('Percent similarity between my_vaccine and bio_n_tech vaccine : ',  percentage_similarity, '%')
print('*****')