# Automating TSHC Quality Checks

A script to automate 11 manual quality checks completed after each paired MiSeq Universal pipeline run. 
The table bellow describes the checks completed by the script.

\# | Check | Description
---|-------|------------
1 | VerifyBamId check | A check to determine if all samples in a worksheet have contamination < 3%
2 | 20x coverage check | A check to determine if 96% of all target bases in each sample are covered at 20X or greater
3 | VCF file count check | A check to determine if 48 VCFs have been generated
4 | FASTQ-BAM check | A check to determine that the expected number of reads are present in each FASTQ and BAM file
5 | Number of exons in negative sample | A check to determine if 1204 exons are present in the negative control (Coverage-exon tab)
6 | Contamination of negative sample | A check to determine if the max read depth of the negative sample is equal to 0 
7 | Kinship check | A check to determine if any sample in the worksheet pair has a kinship value of 0.48 or higher
8 | VerifyBamId check | A check to determine if all samples in a worksheet have contamination < 3%
9 | 20x coverage check | A check to determine if 96% of all target bases in each sample are covered at 20X or greater
10 | VCF file count check | A check to determine if 48 VCFs have been generated
11 | FASTQ-BAM check | A check to determine that the expected number of reads are present in each FASTQ and BAM file 	