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
import re

__version__ = '0.1'
USAGE = '''
'''
def rm_comment(x):
    if str(x).startswith("##"):
        return True
    else:
        return False

pattern1 = re.compile(r'''^##''')
pattern11 = re.compile(r'''^#''')

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

    df_custom_set_only2.to_csv(os.path.join(output_dir,"%s_custom_set_only.tsv"%(setting_name)), sep='\t',index=False, header=False)
    df_report_set_only2.to_csv(os.path.join(output_dir,"%s_report_set_only.tsv"%(setting_name)), sep='\t',index=False, header=False)
    df_two_sets_intersection2.to_csv(os.path.join(output_dir,"%s_two_sets_intersection.tsv"%(setting_name)), sep='\t', index=False, header=False)

def main1(args):
    print(args)
    input_coordinate_list=args.input_coordinate_list
    input_vcf=args.input_vcf
    setting_name=args.setting
    
    output_dir = os.path.dirname(input_coordinate_list)
    input_coordinate_list_data=pd.read_csv(input_coordinate_list,header=None,delimiter="\t")
    input_coordinate_list_data.columns = ["#CHROM","POS"]
#    input_vcf_data=pd.read_csv(input_vcf,delimiter="\t", header = 1, skiprows=lambda x: rm_comment(x))
    input_vcf_data =[]
    with open(input_vcf, "r") as fh:
        while True:
            line = fh.readline()
            if not line:
                break
            elif re.search(pattern1, line):
                pass
            else:
                input_vcf_data.append(line.rsplit("\t"))
    
    input_vcf_data2 =  pd.DataFrame(input_vcf_data[1:]) 
    input_vcf_data2.columns = input_vcf_data[0]
    input_vcf_data2["POS"] = input_vcf_data2["POS"].astype(int)   
    chr_index = pd.CategoricalDtype(["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","X","Y"], ordered = True)

#    df3 = input_coordinate_list_data.set_index(["#CHROM","POS"])
#    df3.update(input_vcf_data2.set_index(["#CHROM","POS"]))
#    df3.reset_index()

    a = set(list(zip(list(input_coordinate_list_data["#CHROM"]),list(input_coordinate_list_data["POS"]))))
    b = set(list(zip(list(input_vcf_data2["#CHROM"]),list(input_vcf_data2["POS"]))))
    coordinate_list_not_in_vcf = list(a.difference(b))
    coordinate_list_in_vcf = list(a & b)
    pd_coordinate_list_not_in_vcf = pd.DataFrame(coordinate_list_not_in_vcf)
    pd_coordinate_list_in_vcf = pd.DataFrame(coordinate_list_in_vcf)

    pd_coordinate_list_not_in_vcf.columns = ["#CHROM","POS"]
    pd_coordinate_list_in_vcf.columns = ["#CHROM","POS"]

    pd_coordinate_list_not_in_vcf['#CHROM'] = pd_coordinate_list_not_in_vcf['#CHROM'].astype(chr_index)
    pd_coordinate_list_in_vcf['#CHROM'] = pd_coordinate_list_in_vcf['#CHROM'].astype(chr_index)

    pd_coordinate_list_not_in_vcf['POS'] = pd_coordinate_list_not_in_vcf['POS'].astype('int')
    pd_coordinate_list_in_vcf['POS'] =  pd_coordinate_list_in_vcf['POS'].astype('int')



    pd_coordinate_list_not_in_vcf2 = pd_coordinate_list_not_in_vcf.sort_values(['#CHROM','POS'], ascending=[True, True])
    pd_coordinate_list_in_vcf2 = pd_coordinate_list_in_vcf.sort_values(['#CHROM','POS'], ascending=[True, True])
    

    pd_coordinate_list_not_in_vcf2.to_csv(os.path.join(output_dir,"%s_coordinate_list_NOT_in_vcf.tsv"%(setting_name)), sep='\t',index=False, header=False)
    pd_coordinate_list_in_vcf2.to_csv(os.path.join(output_dir,"%s_coordinate_list_in_vcf.tsv"%(setting_name)), sep='\t',index=False, header=False)
    
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


def main2(args):
    print(args)
    input_vcf=args.input_vcf
    input_coordinate_list=args.input_coordinate_list
    setting_name=args.setting

    output_dir = os.path.dirname( input_vcf)
    output_vcf_NOT_in_list = os.path.join( output_dir, '%s_vcf_NOT_in_list'%(args.setting))
    output_vcf_in_list = os.path.join( output_dir, '%s_vcf_in_list'%(args.setting))

    input_coordinate_list_data=pd.read_csv(input_coordinate_list,header=None,delimiter="\t")
    input_coordinate_list_data.columns = ["#CHROM","POS"]

    with open(input_vcf, 'r') as fh_input_vcf, open(output_vcf_NOT_in_list, 'w+') as fh_output_vcf_NOT_in_list, open(output_vcf_in_list, 'w+') as fh_output_vcf_in_list:
        while True:
            line = fh_input_vcf.readline()
            if not line:
                break
            elif re.search(pattern11, line):
                fh_output_vcf_NOT_in_list.write(line)
                fh_output_vcf_in_list.write(line)
            else:
                input_vcf_data = line.rsplit("\t")
                if input_coordinate_list_data.loc[(input_coordinate_list_data['#CHROM'] ==  input_vcf_data[0]) & (input_coordinate_list_data['POS'] ==  input_vcf_data[1])]:
                    fh_output_vcf_in_list.write(line)
                else:
                    fh_output_vcf_NOT_in_list.write(line)
    


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

    parser_1 = subparsers.add_parser('1', description='split coordinate list from vcf',
                                     help='split coordinate list from vcf', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_1.add_argument('-i', '--input_coordinate_list',
                          type=str, help='input coordinate list')
    parser_1.add_argument('-r', '--input_vcf',
                          type=str, help='the input vcf')
    parser_1.add_argument('-s', '--setting',
                          type=str, help='the setting name')
    parser_1.set_defaults(func=main1)

    parser_2 = subparsers.add_parser('2', description='split vcf from coordinate list',
                                     help='split vcf from coordinate list', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser_2.add_argument('-r', '--input_vcf',
                          type=str, help='the input vcf')
    parser_2.add_argument('-i', '--input_coordinate_list',
                          type=str, help='input coordinate list')
    parser_2.add_argument('-s', '--setting',
                          type=str, help='the setting name')
    parser_2.set_defaults(func=main2)

    args = parser.parse_args(sys.argv[1:])
    args.func(args)


if __name__ == '__main__':
    main()
