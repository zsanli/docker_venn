'''
Created on 2021.3.30

@author: Zhi Zhang

@email: zhi.zhang@lns.etat.lu

draw picture for venn
=====================

'''

#!/usr/bin/env python
import os
import re
import sys
import glob
import argparse
import shutil
from time import time, ctime
import datetime
import logging
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

__version__ = '0.1'
USAGE = '''
'''
def main0(args):
    print(args)
    input_custom=args.input_custom
    input_report=args.input_report
    setting_name=args.setting
    
    output_dir = os.path.dirname(input_custom)
    input_custom_data=pd.read_csv(input_custom,delimiter="\t")
    input_report_data=pd.read_csv(input_report,delimiter="\t")
    chr_index = pd.CategoricalDtype(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X","Y"], ordered = True)

    input_custom_set=set(input_custom_data['#Position'])
    input_report_set=set(input_report_data['#Position'])

    venn2([input_custom_set, input_report_set], (setting_name, 'report'))
    plt.savefig(os.path.join(output_dir,setting_name+"_venn.png"))

    custom_set_only = pd.DataFrame({'#Position': list(input_custom_set.difference(input_report_set))})
    report_set_only = pd.DataFrame({'#Position': list(input_report_set.difference(input_custom_set))})
    two_sets_intersection = pd.DataFrame({'#Position': list(input_custom_set & input_report_set)})

    custom_set_only2 = pd.DataFrame({'#Position': custom_set_only["#Position"].str.replace("chr", "")})
    report_set_only2 = pd.DataFrame({'#Position': report_set_only["#Position"].str.replace("chr", "")})
    two_sets_intersection2 = pd.DataFrame({'#Position': two_sets_intersection["#Position"].str.replace("chr", "")})

    df_custom_set_only = pd.DataFrame({'#CHROM': [],'POS':[]})
    df_report_set_only = pd.DataFrame({'#CHROM': [],'POS':[]})
    df_two_sets_intersection = pd.DataFrame({'#CHROM': [],'POS':[]})

    df_custom_set_only[['#CHROM','POS']] = custom_set_only2['#Position'].str.split(':',expand=True)
    df_report_set_only[['#CHROM','POS']] = report_set_only2['#Position'].str.split(':',expand=True)
    df_two_sets_intersection[['#CHROM','POS']] = two_sets_intersection2['#Position'].str.split(':',expand=True)

    df_custom_set_only['#CHROM'] = df_custom_set_only['#CHROM'].astype(chr_index)
    df_report_set_only['#CHROM'] =  df_report_set_only['#CHROM'].astype(chr_index)
    df_two_sets_intersection['#CHROM'] = df_two_sets_intersection['#CHROM'].astype(chr_index)

    df_custom_set_only['POS'] = df_custom_set_only['POS'].astype('int')
    df_report_set_only['POS'] =  df_report_set_only['POS'].astype('int')
    df_two_sets_intersection['POS'] = df_two_sets_intersection['POS'].astype('int')

    df_custom_set_only2 = df_custom_set_only.sort_values(['#CHROM','POS'], ascending=[True, True])
    df_report_set_only2 = df_report_set_only.sort_values(['#CHROM','POS'], ascending=[True, True])
    df_two_sets_intersection2 = df_two_sets_intersection.sort_values(['#CHROM','POS'], ascending=[True, True])

    df_custom_set_only2.to_csv(os.path.join(output_dir,"custom_set_only.tsv"), sep='\t',index=False, header=False)
    df_report_set_only2.to_csv(os.path.join(output_dir,"report_set_only.tsv"), sep='\t',index=False, header=False)
    df_two_sets_intersection2.to_csv(os.path.join(output_dir,"two_sets_intersection.tsv"), sep='\t', index=False, header=False)



#    with open(os.path.join(output_dir,"custom_set_only.tsv"),"w+") as fh:
#        for i in custom_set_only:
#            fh.write("".join([i.split(":")[0].replace("chr",""),"\t",i.split(":")[1],"\n"]))
#
#    with open(os.path.join(output_dir,"report_set_only.tsv"),"w+") as fh:
#        for i in report_set_only:
#            fh.write("".join([i.split(":")[0].replace("chr",""),"\t",i.split(":")[1],"\n"]))
#
#    with open(os.path.join(output_dir,"two_sets_intersection.tsv"),"w+") as fh:
#        for i in two_sets_intersection:
#            fh.write("".join([i.split(":")[0].replace("chr",""),"\t",i.split(":")[1],"\n"]))



def main():
    parser = argparse.ArgumentParser(
        description='draw venn diagram for two tsv')
    subparsers = parser.add_subparsers(help='sub-command help')
    parser_0 = subparsers.add_parser('0', description='draw venn diagram for two tsv',
                                     help='draw venn diagram for two tsv', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_0.add_argument('-i', '--input_custom',
                          type=str, help='the input custom tsv')
    parser_0.add_argument('-r', '--input_report',
                          type=str, help='the input report tsv')
    parser_0.add_argument('-s', '--setting',
                          type=str, help='the setting name')
    parser_0.set_defaults(func=main0)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == '__main__':
    main()
