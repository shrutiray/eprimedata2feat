#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 22:10:22 2017

@author: sray
"""

#import required libraries
import sys
import os
import convert_eprime as ce
import argparse


class MyParser(argparse.ArgumentParser):
    def error(self,message):
        sys.stderr.write('error: %s \n' % message)
        self.print_help()
        sys.exit(2)
        
def gracefulExit():
    parser.print_help()
    exit(2)
    
#Accept input at command line window
parser = MyParser(prog="Convert eprime .txt to .csv")
parser.add_argument('-path','--path',help="input directory with subject folders having eprime data")
parser.add_argument('-subID','--subjectID',help="The subject ID whose eprime .txt file is to be converted to .csv")

#check if required number of arguments have been passed
if len(sys.argv)==0:
    parser.print_help()
    sys.exit(1)
    
args=parser.parse_args()

#Check if subID input is given ordirectory path is given
if args.subjectID:
    subID=args.subjectID
    head,tail=os.path.split(subID)
    ID_num=tail.lstrip('sub-')
    if head=='':
        path=os.getcwd()
        eprime="ls "+os.path.join(path,"sub-"+ID_num,"originals")+ " | grep ePrimeData"
        eprimedata=os.popen(eprime).read().strip("\n")
        eprime_output="ls "+os.path.join(path,"sub-"+ID_num,"originals",eprimedata)
        e_output=os.popen(eprime_output).readlines()
        face1=e_output[0].strip("\n")
        face2=e_output[1].strip("\n")
    else:
        path=head
        eprime="ls "+os.path.join(path,"sub-"+ID_num,"originals")+ " | grep ePrimeData"
        eprimedata=os.popen(eprime).read().strip("\n")
        eprime_output="ls "+os.path.join(path,"sub-"+ID_num,"originals",eprimedata)
        e_output=os.popen(eprime_output).readlines()
        face1=e_output[0].strip("\n")
        face2=e_output[1].strip("\n")

    txtfilename1=os.path.join(path,'sub-'+ID_num,'originals',eprimedata,face1)
    txtfilename2=os.path.join(path,'sub-'+ID_num,'originals',eprimedata,face2)
    
    fname1,ext1=os.path.splitext(face1)
    fname2,ext2=os.path.splitext(face2)

    fname1_2=fname1[:-13]
    fname2_2=fname2[:-13]
           
    if not os.path.exists(os.path.join(path,'sub-'+ID_num,'eprime_csvfiles')):
        os.makedirs(os.path.join(path,'sub-'+ID_num,'eprime_csvfiles'))

    out_file1=os.path.join(path,'sub-'+ID_num,'eprime_csvfiles',fname1_2+'.csv')
    out_file2=os.path.join(path,'sub-'+ID_num,'eprime_csvfiles',fname2_2+'.csv')
    ce.text_to_csv(txtfilename1, out_file1)
    ce.text_to_csv(txtfilename2, out_file2)  
elif args.path:
    direc=args.path
    path=os.chdir(direc)
    cmd="ls | grep sub- > eprime_subject_list.txt"
    os.system(cmd)
    for f in open("eprime_subject_list.txt"):
        f=f.strip("\n")
        f=f.strip("sub-")
        eprime="ls "+os.path.join(direc,"sub-"+f,"originals")+ " | grep ePrimeData"
        eprimedata=os.popen(eprime).read().strip("\n")
        txtpath=os.path.join(direc,"sub-"+f,'originals',eprimedata)
        os.chdir(txtpath)
        cmd2="ls | grep run1.txt > eprime_txt_list.txt"
        os.system(cmd2)
        for f1 in open("eprime_txt_list.txt"):
            f1=f1.strip("\n")
            fname,ext=os.path.splitext(f1)
            fname_2=fname[:-13]
            file_name=fname_2[:-6]
            out_file=os.path.join(direc,'sub-'+file_name.strip("sub-"),'eprime_csvfiles',fname_2+'.csv')
            txtfile=os.path.join(direc,"sub-"+f,'originals',eprimedata,f1)
            if not os.path.exists(os.path.join(direc,'sub-'+file_name.strip("sub-"),'eprime_csvfiles')):
                os.makedirs(os.path.join(direc,"sub-"+file_name.strip("sub-"),"eprime_csvfiles"))
            ce.text_to_csv(f1, out_file)                            