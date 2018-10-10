import csv
import yaml
import json

def read_input_nodes(file_name):
    '''
    Reads a csv file that contains information detailing a network of node_list
    Param - file_name: Name of the csv file
    Returns: A dictionary of nodes in the network
    '''
    with open(file_name) as file:
        csv_reader = csv.DictReader(file)
        nodes = []

        for row in csv_reader:
            node = {'name': row['name'],
                    'address': row['address (S)'],
                    'latitude': row['latitude (N)'],
                    'longitude': row['longitude (N)']}

            nodes.append(node)

    return nodes

def read_yml(file_name):
    '''
    Reads in a yaml configuration file that contains values for the parameters that power the genetic algorithm
    Param - file_name: Name of the yaml file that contains the configuration values
    Returns: A yaml file
    '''
    with open(file_name, 'r') as f:
        yaml_file = yaml.load(f)
    return yaml_file

def read_json_states(file_name):
    '''
    reads in a json file of state capitals and there coordinates
    retu
    '''
    with open(file_name) as file:
        data = json.load(file)

    nodes = []
    for row in data:
        node = {'name': row['capital'] + ', ' + row['name'],
                'address': '',
                'latitude': row['lat'],
                'longitude': row['long']}

        nodes.append(node)

    return nodes
