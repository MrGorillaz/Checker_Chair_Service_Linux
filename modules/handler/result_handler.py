##########################################
## Name:    result_handler              ##
## Author:  Alexander Orlowski          ##
## Company: Sedus Sysems GmbH           ##
## Date:    28.07.2020                  ##
## Version: 1.0                         ##
##########################################
## Description:                         ##
## This Module is for handling Results  ##
## given in a Pandas DataFrame          ##
##########################################

from numpy import nan

def set_results (params,results):
    for column in params.columns:
        if column in results.columns:
            results[column] = params[column]

    results.replace(nan, '<NULL>', inplace=True)
    return results

def write_results(params,results,resultPath):

    results = set_results(params,results)
    results.to_csv(resultPath, sep=';', index=False)

def print_results(results):
    for column in results.columns:
        print(f'{column:20} : {results[column].values}')


