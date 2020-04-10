import tabula
import csv
import os

# file = '2020-04-09-13-24-36-385_1586418876385_XXXCM1615X_ITRV.pdf'

def parseImportantData(pdf_file):
    
    output_file = pdf_file.split('.')[0]+'.csv'
    output_dict = {}
    tabula.convert_into(pdf_file,output_file,output_format="csv")

    with open(output_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile) 

        for row in csvreader:
            if row[0] == 'Name PAN':
                row = next(csvreader)
                output_dict['pan_number'] = row[0].split()[-1].lstrip().rstrip()
                output_dict['company_name'] = ' '.join(row[0].split()[:-1]).lstrip().rstrip()

            if 'ITR' in row[0]:
                output_dict['form_number'] = int(row[0].split('-')[-1])

            if '6Total tax,' in row[0]:
                output_dict['total_tax'] = int(row[2])

            if 'eTotal Taxes Paid' in row[0]:
                output_dict['tax_paid'] = int(row[2])

            if '3Total Income' in row[0]:
                output_dict['total_income'] = int(row[2])

            if '3bCurrent Year loss' in row[0]:
                output_dict['loss'] = int(row[2])

            if '3aDeemed Total Income' in row[0]:
                output_dict['deemed_income'] = int(row[2])
    os.remove(output_file)
    return output_dict

# print(parseImportantData(file))