# Automating TSHC Quality Checks

A script to automate 11 manual quality checks completed after each paired MiSeq Universal pipeline run. 
The script performs a series of checks on the paired output directories from a MiSeq Univeral (TSHC) run.
The checks have been described in table 1. The script records PASS/FAIL values for each check and saves
these as a static HTML output.

table 1- checks completed by the quality_check.py script.
\# | Worksheet| Check | Description
---|----------|-------|------------
 1 | ws_1 | VerifyBamId check | A check to determine if all samples in a worksheet have contamination < 3%
 2 | ws_1 | 20x coverage check | A check to determine if 96% of all target bases in each sample are covered at 20X or greater
 3 | ws_1 | VCF file count check | A check to determine if 48 VCFs have been generated
 4 | ws_1 | FASTQ-BAM check | A check to determine that the expected number of reads are present in each FASTQ and BAM file
 5 | neg_excel | Number of exons in negative sample | A check to determine if 1204 exons are present in the negative control (Coverage-exon tab)
 6 | neg_excel | Contamination of negative sample | A check to determine if the max read depth of the negative sample is equal to 0 
 7 | ws_2 | Kinship check | A check to determine if any sample in the worksheet pair has a kinship value of 0.48 or higher
 8 | ws_2 | VerifyBamId check | A check to determine if all samples in a worksheet have contamination < 3%
 9 | ws_2 | 20x coverage check | A check to determine if 96% of all target bases in each sample are covered at 20X or greater
 10 | ws_2 | VCF file count check | A check to determine if 48 VCFs have been generated
 11 | ws_2 | FASTQ-BAM check | A check to determine that the expected number of reads are present in each FASTQ and BAM file 	


## Running the quality check script

Example:
'''
$ cd /path/to/ngs_quality_check/

$ python quality_check.py --ws_1 /path/to/000001/TSHC_000001_v0.5.2/ --ws_2 /path/to/000002/TSHC_000002_v0.5.2/

'''

