# Automating TSHC Quality Checks

A script to automate 11 manual quality checks completed after each paired MiSeq Universal pipeline run. The script performs a series of checks on the paired output directories from a MiSeq Univeral (TSHC) run. The checks have been described in table 1. The script records PASS/FAIL values for each check and saves this to a static HTML file. The file, by default, is saved in the TSHC pipeline output folder.

Table 1- checks completed by the quality_check.py script.
 
|\#  | Worksheet | Check                              | Description                                                                                   |
|----|-----------|------------------------------------|-----------------------------------------------------------------------------------------------|
| 1  | ws_1      | VerifyBamId check                  | A check to determine if all samples in a worksheet have contamination < 3%                    |
| 2  | ws_1      | 20x coverage check                 | A check to determine if 96% of all target bases in each sample are covered at 20X or greater  |
| 3  | ws_1      | VCF file count check               | A check to determine if 48 VCFs have been generated                                           |
| 4  | ws_1      | FASTQ-BAM check                    | A check to determine that the expected number of reads are present in each FASTQ and BAM file |
| 5  | neg_excel | Number of exons in negative sample | A check to determine if 1204 exons are present in the negative control (Coverage-exon tab)    |
| 6  | neg_excel | Contamination of negative sample   | A check to determine if the max read depth of the negative sample is equal to 0               |
| 7  | ws_2      | Kinship check                      | A check to determine if any sample in the worksheet pair has a kinship value of 0.48 or higher|
| 8  | ws_2      | VerifyBamId check                  | A check to determine if all samples in a worksheet have contamination < 3%                    |
| 9  | ws_2      | 20x coverage check                 | A check to determine if 96% of all target bases in each sample are covered at 20X or greater  |
| 10 | ws_2      | VCF file count check               | A check to determine if 48 VCFs have been generated                                           |
| 11 | ws_2      | FASTQ-BAM check                    | A check to determine that the expected number of reads are present in each FASTQ and BAM file |



## Running the quality check script


Example:

```
$ cd /path/to/ngs_quality_check/

$ python quality_check.py -ws_1 /path/to/000001/TSHC_000001_v0.5.2/ -ws_2 /path/to/000002/TSHC_000002_v0.5.2/

```

Full arguments:


| Argument    | Description                                                      |
|-------------|------------------------------------------------------------------|
| ws_1 	      | Path to the 1st TSHC output folder  						     |
| ws_2        | Path to the 2nd TSHC output folder 							     |
| out_dir     | Path to a folder to store the HTML report outputed from the script. If no out_dir is specified the html report will saved in each of the TSHC output folders.|


## Quality script testing

A mock set of TSHC output data has been generated to test the quality check script. The test_quality_check.py scipt can used to test multiple pairs of the mock TSHC data. The mock outputs and pairing excel spreadsheet are available on the S drive. The script generates a HTML report to summarise the results quality check results. The summary hmtl report will be stored in the test output directory.

Example:

```
$ cd /path/to/ngs_quality_check/

$ python test_quality_checks.py  -ws_dir /path/to/s_drive/test_worksheet/ -out_dir /path/to/s_drive/test_output -pairing /path/to/ws_pairing.xlsx

```

Full arguments:


| Argument    | Description                                                      	 |
|-------------|----------------------------------------------------------------------|
| ws_dir 	  | Path to folder containing 26 mock TSHC output data 					 |
| test_out    | Path to a folder to store all HTML quality reports and summary report|
| pairing     | Path to an excel spreadsheet describing TSHC worksheet pairs		 |
