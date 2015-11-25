"""
Usage: multiple_runs.py <dir_name> <num_runs>

Arguments
    dir_name    : Name of the directory from which to read and in data files
    num_runs    : Number of runs to run simulation for

Options
    -h          : displays this help file
"""
from __future__ import division
import asq
import csv
import docopt
import os
from math import ceil

arguments = docopt.docopt(__doc__)
dirname = arguments['<dir_name>']
num_runs = int(arguments['<num_runs>'])

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


def bin_by_month(data, bins):
    """
    Bins data by month
    """
    data_by_month = [[row for row in data if row[3] > bins[i] and row[3] <= bins[i+1]] for i in range(len(bins)-1)]
    return data_by_month




def count_demand_N2(data_by_month):
    """
    Returns a list of counts of cls 4 at N2
    Returns a list of counts of all others clss at N2
    """
    count_cls_4 = [count_class_4_N2(row) for row in data_by_month]
    count_other_cls = [count_other_class_N2(row) for row in data_by_month]
    return count_cls_4, count_other_cls

def count_class_4_N2(data):
    """
    Counts number of class 4 at Node 4
    """
    return len([row for row in data if row[2]==float(2) if row[1]==float(4)])

def count_other_class_N2(data):
    """
    Counts number of NOT class 4 at Node 4
    """
    return len([row for row in data if row[2]==float(2) if row[1]!=float(4)])

def write_results_to_file(data, file_name, directory):
    """
    Writes results to a file
    """
    results_file = open('%s%s.csv' % (directory, file_name), 'w')
    csv_wrtr = csv.writer(results_file)
    for row in data:
        csv_wrtr.writerow(row)
    results_file.close()

def average_waiting_time_per_month(data_by_month):
    """
    Finds the expected wait if a customer arrives in a given month
    """
    return [sum([obs[4] for obs in row if obs[1]==float(4)])/len([obs[4] for obs in row if obs[1]==float(4)]) for row in data_by_month], [sum([obs[4] for obs in row if obs[1]!=float(4)])/len([obs[4] for obs in row if obs[1]!=float(4)]) for row in data_by_month]



multiple_runs_demand_cls_4 = []
multiple_runs_demand_cls_other = []
multiple_runs_wait_cls_4 = []
multiple_runs_wait_cls_other = []

for i in range(num_runs):
    P = asq.load_parameters(directory)
    Q = asq.Simulation(P)
    Q.simulate_until_max_time()
    max_sim_time = Q.max_simulation_time
    bins = [obs*(365.25/12) for obs in range(int(ceil(max_sim_time / (365.25/12)))+1)]
    Q.write_records_to_file(directory, i)
    data = read_in_data(directory, i)
    data_by_month = bin_by_month(data, bins)
    count_cls_4, count_other_cls = count_demand_N2(data_by_month)
    multiple_runs_demand_cls_4.append(count_cls_4)
    multiple_runs_demand_cls_other.append(count_other_cls)
    expected_wait_by_month_cls_4, expected_wait_by_month_cls_other = average_waiting_time_per_month(data_by_month)
    multiple_runs_wait_cls_4.append(expected_wait_by_month_cls_4)
    multiple_runs_wait_cls_other.append(expected_wait_by_month_cls_other)
write_results_to_file(multiple_runs_demand_cls_4, 'demand_new', directory)
write_results_to_file(multiple_runs_demand_cls_other, 'demand_follow_up', directory)
write_results_to_file(multiple_runs_wait_cls_4, 'wait_new', directory)
write_results_to_file(multiple_runs_wait_cls_other, 'wait_follow_up', directory)