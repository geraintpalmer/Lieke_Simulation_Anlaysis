"""
Usage: multiple_runs.py <dir_name> <num_runs> <warm_up>

Arguments
    dir_name    : Name of the directory from which to read and in data files
    num_runs    : Number of runs to run simulation for
    warm_up     : The warm up period to forget about

Options
    -h          : displays this help file
"""
from __future__ import division
import csv
import docopt
import os
from math import ceil

arguments = docopt.docopt(__doc__)
dirname = arguments['<dir_name>']
num_runs = int(arguments['<num_runs>'])
warm_up = float(arguments['<warm_up>'])

root = os.getcwd()
directory = os.path.join(root, dirname)


def read_in_data(directory, i):
    """
    Reads in a data.csv file
    """
    data = []
    data_file_name = directory + 'data%s.csv' % str(i)
    data_file = open(data_file_name, 'r')
    rdr = csv.reader(data_file)
    for row in rdr:
        data.append([float(obs) for obs in row])
    data_file.close()
    return data

def write_results_to_file(data, file_name, directory):
    """
    Writes results to a file
    """
    results_file = open('%s%s.csv' % (directory, file_name), 'w')
    csv_wrtr = csv.writer(results_file)
    for row in data:
        csv_wrtr.writerow(row)
    results_file.close()


multiple_runs_waits_cls4 = []
multiple_runs_waits_other = []
for i in range(num_runs):
    data = read_in_data(directory, i)
    waits_after_warmup_cls4 = [row[4] for row in data if row[3] >= warm_up if row[1]==float(4)]
    waits_after_warmup_other = [row[4] for row in data if row[3] >= warm_up if row[1]!=float(4)]
    multiple_runs_waits_cls4.append(waits_after_warmup_cls4)
    multiple_runs_waits_other.append(waits_after_warmup_other)
write_results_to_file(multiple_runs_waits_cls4, 'overall_waits_new', directory)
write_results_to_file(multiple_runs_waits_other, 'overall_waits_follow_up', directory)