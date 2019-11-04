import os
import pandas as pd
import argparse
import sys
import re


#A script to parse outputs from the pipeline to determine if quality criteria has been met or not.
#    Quality criteria include:
#        1) If any samples within a run have a 20x coverage < 96%
#        2) If number of exons in gene-exon tab == 1419
#        3) If reads are present in the negative control
#        4) If any kinship values in the kinship > 0.48 
#        ( Is this necessary? 5) Log file quality checks e.g. pipeline version, path, worksheet number...)
#        6) VCF file count
#        7) FASTQ-BAM output check
#        8) Verify bam id check

# The checks will be separated by input file used:
#    1) 1 x results excel output file:
#        a) checks 1 & 8
#    2) 1 x negative excel results: 
#        a) checks 2 & 3
#    3) Kinship excel file:
#        a) check 4
#    4) Command log file:
#        a) check 5
#    5) VCF directory:
#        a) check 6
#    6) FASTQ-BAM excel file:
#        a) check 7


# TODO add version of pipeline to input
def get_inputs(ws_1, ws_2):


    ws_1_run_info = re.search(r'\/([A-Z]*)_(\d{6})_(v\d\.\d\.\d)\/', ws_1)    
    ws_2_run_info = re.search(r'\/([A-Z]*)_(\d{6})_(v\d\.\d\.\d)\/', ws_2)  

    ws_1_panel = ws_1_run_info.group(1)
    ws_1_name = ws_1_run_info.group(2)
    ws_1_version = ws_1_run_info.group(3)
    ws_2_panel = ws_2_run_info.group(1)
    ws_2_name = ws_2_run_info.group(2)
    ws_2_version = ws_2_run_info.group(3)
    
    # defining excel inputs
    ws_1_excel_reports = ws_1 + 'excel_reports_{}_{}/'.format(ws_1_panel, ws_1_name)
    ws_1_list = pd.DataFrame(os.listdir(ws_1_excel_reports), columns=['sample_name'])
    ws_2_excel_reports = ws_2 + 'excel_reports_{}_{}/'.format(ws_2_panel, ws_2_name)
    ws_2_list = pd.DataFrame(os.listdir(ws_2_excel_reports), columns=['sample_name'])

    xls_rep_1 = ws_1_list[~ws_1_list['sample_name'].str.contains('Neg')]
    xls_rep_2 = ws_2_list[~ws_2_list['sample_name'].str.contains('Neg')]
    neg_rep_1 = ws_1_list[ws_1_list['sample_name'].str.contains('Neg')]
    neg_rep_2 = ws_2_list[ws_2_list['sample_name'].str.contains('Neg')]
    fastq_xls_1 = ws_1_list[ws_1_list['sample_name'].str.contains('fastq-bam-check')]
    fastq_xls_2 = ws_2_list[ws_2_list['sample_name'].str.contains('fastq-bam-check')]

    xls_rep_1 = ws_1_excel_reports + xls_rep_1.values[0][0]
    xls_rep_2 = ws_2_excel_reports + xls_rep_2.values[0][0]

    #determine which ws contains the negative sample
    if len(neg_rep_1) != 0:
        neg_rep = ws_1_excel_reports + neg_rep_1.values[0][0]
    elif len(neg_rep_2) != 0:
        neg_rep = ws_2_excel_reports + neg_rep_2.values[0][0]
    else:
        raise Exception('Error the negative sample is no present!')

    # get fastq-bam-check file names 
    fastq_bam_1 = ws_1_excel_reports + fastq_xls_1.values[0][0]
    fastq_bam_2 = ws_2_excel_reports + fastq_xls_2.values[0][0]

    # defining vcf directory path 
    vcf_dir_1 = ws_1 + 'vcfs_{}_{}/'.format(ws_1_panel, ws_1_name)
    vcf_dir_2 = ws_2 + 'vcfs_{}_{}/'.format(ws_2_panel, ws_2_name)

    # defining cmd_log and kin
    cmd_log_1 = ws_1 + '{}.commandline_usage_logfile'.format(ws_1_name)
    cmd_log_2 = ws_2 + '{}.commandline_usage_logfile'.format(ws_2_name)
    kin_xls = ws_1 + '{}_{}.king.xlsx'.format(ws_1_name, ws_2_name)

    return xls_rep_1, xls_rep_2, neg_rep, fastq_bam_1, fastq_bam_2, kin_xls, vcf_dir_1, vcf_dir_2, cmd_log_1, cmd_log_2



def results_excel_check(res, check_result_df):
    # 1) If any samples within a run have a 20x coverage < 96%
    # 8) Verify bam id check

    # create dfs with data from excel output
    xls = pd.ExcelFile(res)
    hybqc_df = pd.read_excel(xls, 'Hyb-QC')
    verify_bam_id_df = pd.read_excel(xls, 'VerifyBamId')
    
    worksheet_name = re.search(r'\/(\d{6})-.*', res).group(1)
    
    # list of all % coverage at 20x (excluding control) 
    coverage_list = hybqc_df[~hybqc_df['Sample'].str.contains('D00-00000')]['PCT_TARGET_BASES_20X'].values
    coverage_check = '20x coverage check'
    coverage_check_des = 'A check to determine if all samples are 96% 20x'
    coverage_result = 'PASS'
    
    for value in coverage_list:
        if value < 0.96:
            coverage_result = 'FAIL'
            
    #list all VerifyBamId results (inc control)
    verify_bam_list = verify_bam_id_df['%CONT'].values
    verify_bam_check = 'VerifyBamId check'
    verify_bam_check_des = 'A check to determine if all samples in a worksheet have contamination < 3%'
    verify_bam_result = 'PASS'
    for value in verify_bam_list:
        if value > 3:
            verify_bam_result = 'FAIL'
    
    check_result_df = check_result_df.append({'Check': verify_bam_check,
                            'Description': verify_bam_check_des,
                            'Result': verify_bam_result, 'Worksheet': worksheet_name}, ignore_index=True)
    
    check_result_df = check_result_df.append({'Check': coverage_check,
                            'Description': coverage_check_des,
                            'Result': coverage_result, 'Worksheet':worksheet_name}, ignore_index=True)
    
    return check_result_df
    
    

def neg_excel_check(neg_xls, check_result_df):
    
    worksheet_name = re.search(r'\/(\d{6})-.*', neg_xls).group(1)
    
    xls = pd.ExcelFile(neg_xls)
    neg_exon_df = pd.read_excel(xls, 'Coverage-exon')

    # number of exons check
    num_exons_check = 'Number of exons'
    num_exons_check_des = 'A check to determine if 1419 exons are present in the negative control'
    
    if len(neg_exon_df) == 1419:
        num_exons_check_result = 'PASS'
    else:
        num_exons_check_result = 'FAIL'
    
    
    # max coverage of exons checks
    cov_neg_exons_check = 'Contamination of negative sample'
    cov_neg_exons_check_des = 'A check to determine if the max read depth of negative sample > 0'
    max_neg_coverage = neg_exon_df['Max'].values

    over_1x = []
    for i in set(max_neg_coverage):
        if i >= 1:
            over_1x.append(i)

    if len(over_1x) >= 1:
        cov_neg_exons_check_result = 'FAIL'
    else:
        cov_neg_exons_check_result = 'PASS'

    ## Removed - criteria changed for TSHC
    # over_15x = []
    # over_9x = []
    # for i in max_neg_coverage:
    #     if i >= 15:
    #         over_15x.append(i)
    #     elif i >= 9:
    #         over_9x.append(i)
    #     else:
    #         continue
    # if len(over_15x) >= 1 or len(over_9x) >= 2:
    #     cov_neg_exons_check_result = 'FAIL'
    # else:
    #     cov_neg_exons_check_result = 'PASS'
            

    check_result_df = check_result_df.append({'Check': num_exons_check,
                                                'Description': num_exons_check_des,
                                                'Result': num_exons_check_result,
                                                'Worksheet': worksheet_name}, ignore_index=True)

    check_result_df = check_result_df.append({'Check': cov_neg_exons_check,
                                                'Description': cov_neg_exons_check_des,
                                                'Result': cov_neg_exons_check_result,
                                                'Worksheet': worksheet_name}, ignore_index=True)
    
    return check_result_df



def kinship_check(kin_xls, check_result_df):
    #check if any sample has a kinship value >0.48
    worksheet_name = re.search(r'\/(\d{6}_\d{6}).king.xlsx.*', kin_xls).group(1)

    kinship_check = 'Check of kinship values'
    kinship_check_des = 'A check to determine if any sample in worksheet pair has a kinship values of >0.48'
    
    xls = pd.ExcelFile(kin_xls)
    kinship_df = pd.read_excel(xls, 'Kinship')
    
    kinship_values = kinship_df['Kinship'].values
    
    if max(kinship_values) > 0.48:
        kinship_check_result = 'FAIL'
    else:
        kinship_check_result = 'PASS'
    
    check_result_df = check_result_df.append({'Check': kinship_check,
                                                'Description': kinship_check_des,
                                                'Result': kinship_check_result,
                                                'Worksheet': worksheet_name}, ignore_index=True)
    
    return check_result_df



def vcf_dir_check(vcf_dir, check_result_df):

    worksheet_name = str(re.search(r'\/vcfs_\w{4}_(\d{6})\/', vcf_dir).group(1))
    vcf_dir_check = 'Check the number of VCFs created'
    vcf_dir_check_des = 'A check to determine if 48 VCFs are generated from the run'
    
    if len(os.listdir(vcf_dir)) == 48:
        vcf_dir_check_result = 'PASS'
    else:
        vcf_dir_check_result = 'FAIL'
    
    check_result_df = check_result_df.append({'Check': vcf_dir_check,
                                                'Description': vcf_dir_check_des,
                                                'Result': vcf_dir_check_result,
                                                'Worksheet': worksheet_name}, ignore_index=True)
    
    return check_result_df


def fastq_bam_check(fastq_xls, check_result_df):
    
    worksheet_name = re.search(r'\/(\d{6})-.*', fastq_xls).group(1)

    fastq_bam_check = 'Check number of reads in FASTQ and BAM'
    fastq_bam_check_des = 'A check to determine that the expected number of reads are present in each FASTQ and BAM file'
    xls = pd.ExcelFile(fastq_xls)
    fastq_bam_df = pd.read_excel(xls, 'Check')
    
    if len(set(fastq_bam_df['Result'].values)) != 1:
        fastq_bam_check_result = 'FAIL'
    else:
        fastq_bam_check_result = 'PASS'
    
    check_result_df = check_result_df.append({'Check': fastq_bam_check,
                                                'Description': fastq_bam_check_des,
                                                'Result': fastq_bam_check_result,
                                                'Worksheet': worksheet_name}, ignore_index=True)

    return check_result_df

def generate_html_output(check_result_df, run_details_df, output_dir):
    html = check_result_df.to_html(index=False, justify='left')
    cmd = run_details_df.to_html(index=False, justify='left') + '\n<br>\n'
    html = cmd + html
    ws_names = "_".join(run_details_df['Worksheet'].values.tolist()) + '_quality_checks.html'

    os.chdir(output_dir)

    with open(ws_names, 'w') as file:
        file.write(html)

def run_details(cmd,xls_rep,run_details_df):
    # A function to get the following run details:
    #   1) worksheet
    #   2) pipeline version
    #   3) experiment name
    #   4) bed files
    #   5) AB threshold

    worksheet = 'ERROR'
    pipe_version = 'ERROR'
    experiment_name = 'ERROR'
    target_bed = 'ERROR'
    refined_target_bed = 'ERROR'
    coverage_bed = 'ERROR'
    allele_balance = 'ERROR'
    bed_files = []

    # get ws names for the cmd file and
    cmd_ws = re.search(r'(\d{6})\.commandline_usage_logfile', cmd).group(1)
    xls_ws = re.search(r'(\d{6})-\d{2}-D\d{2}-\d{5}-\w{2,3}_S\d{1,2}\.v\d\.\d\.\d-results\.xlsx', xls_rep).group(1)

    # check that the cmd and xls report are from the same worksheet
    if cmd_ws != xls_ws:
        raise Exception('The worksheet numbers: {} and {} do not match!'.format(cmd_ws, xls_ws))

    worksheet = cmd_ws

    # get experiment name from command output
    with open(cmd, 'r') as file:
        cmd_text = file.read()
    search_term = r'-s\s\n\/network\/sequenced\/MiSeq_data\/\w*\/shire_worksheet_numbered\/' + re.escape(worksheet) + r'\/(\d{6}_M\d{5}_\d{4}_\d{9}-\w{5})\/SampleSheet.csv'
    experiment_name = re.search(search_term, cmd_text).group(1)

    # get pipeline version, bed file names and AB threshold

    xls = pd.ExcelFile(xls_rep)
    config_df = pd.read_excel(xls, 'config_parameters')

    allele_balance = config_df[config_df['key']=='AB_threshold']['variable'].values[0]
    pipe_version = config_df[config_df['key']=='pipeline version']['variable'].values[0]

    # Some TSHC samples may not contain all Bed files
    if 'target_regions' in config_df['key'].values:
        target_bed = config_df[config_df['key']=='target_regions']['variable'].values[0].split('/')[-1]
    if 'refined_target_regions' in config_df['key'].values:
        refined_target_bed = config_df[config_df['key']=='refined_target_regions']['variable'].values[0].split('/')[-1]
    if 'coverage_regions' in config_df['key'].values:
        coverage_bed = config_df[config_df['key']=='coverage_regions']['variable'].values[0].split('/')[-1]

    bed_files.append(target_bed)
    bed_files.append(refined_target_bed)
    bed_files.append(coverage_bed)

        
    bed_files = ", ".join(bed_files)

    run_details_df = run_details_df.append({'Worksheet': worksheet,
                                            'Pipeline version': pipe_version,
                                            'Experiment name': experiment_name,
                                            'Bed files': bed_files,
                                            'AB threshold': allele_balance
                                            }, ignore_index=True)


    return run_details_df
    

parser = argparse.ArgumentParser()
parser.add_argument('--ws_1', action='store', required=True)
parser.add_argument('--ws_2', action='store', required=True)
parser.add_argument('--out_dir', action='store', required=True)
args = parser.parse_args()

xls_rep_1, xls_rep_2, neg_rep, fastq_bam_1, fastq_bam_2, kin_xls, vcf_dir_1, vcf_dir_2, cmd_log_1, cmd_log_2 = get_inputs(args.ws_1, args.ws_2)

check_result_df = pd.DataFrame(columns=[ 'Worksheet','Check', 'Description','Result'])
run_details_df = pd.DataFrame(columns=['Worksheet', 'Pipeline version', 'Experiment name', 'Bed files', 'AB threshold'])
out_dir = args.out_dir

# ws_1 checks
check_result_df = results_excel_check(xls_rep_1, check_result_df)
check_result_df = vcf_dir_check(vcf_dir_1, check_result_df)
check_result_df = fastq_bam_check(fastq_bam_1, check_result_df)

# ws_2 checks
check_result_df = results_excel_check(xls_rep_2, check_result_df)
check_result_df = vcf_dir_check(vcf_dir_2, check_result_df)
check_result_df = fastq_bam_check(fastq_bam_2, check_result_df)

# pair checks
check_result_df = neg_excel_check(neg_rep, check_result_df)
check_result_df = kinship_check(kin_xls, check_result_df)

# run details
run_details_df = run_details(cmd_log_1, xls_rep_1, run_details_df)
run_details_df = run_details(cmd_log_2, xls_rep_2, run_details_df)
# sort
check_result_df = check_result_df.sort_values(by=['Worksheet'])
run_details_df = run_details_df.sort_values(by=['Worksheet'])
#create static html output
generate_html_output(check_result_df,run_details_df, out_dir)
