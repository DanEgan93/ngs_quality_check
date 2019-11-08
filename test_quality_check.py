import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--test_ws_dir', action='store', required=True)
parser.add_argument('--test_out_dir', action='store', required=True)
parser.add_argument('--pairing', action='store', required=True)
args = parser.parse_args()


pair_xls = args.pairing
ws_dir = args.test_ws_dir
out_dir = args.test_out_dir

def sort_pairing(inp_xls):
	# take pair xls and assign pairs
	pairing_dict = {}

	pair_df = pd.DataFrame()
	pair_xls = pd.ExcelFile(inp_xls)
	pair_df = pd.read_excel(pair_xls,'pair', converters={'Worksheet_1':'{:0>6}'.format, 'Worksheet_2':'{:0>6}'.format})
	print(pair_df)

	for index,value in enumerate(pair_df.values):
		test_num = index + 1
		test_pair = value

		pairing_dict[test_num] = test_pair.tolist()

	return pairing_dict

def run_quality_check(ws_1, ws_2, out_dir, base):

	ws_1_num = ws_1
	ws_2_num = ws_2

	panel = 'TSHC'
	version = 'v.0.5.2'
	ws_1 = base + f'{ws_1}/' + f'{panel}_{ws_1_num}_{version}/'
	ws_2 = base + f'{ws_2}/' + f'{panel}_{ws_2_num}_{version}/'

	command = f'python quality_check.py --ws_1 {ws_1} --ws_2 {ws_2} --out_dir {out_dir}'

	# os.system(command)
	print(f'HTML report for worksheets {ws_1_num}_{ws_2_num} is available!')

def results_comparison(html_report):
	pass

def generate_html_output(summary_df):
	base_html = '<h1>Test Run Summary<h1/><h3>Results<h3/>'
	summary_html = summary_df.to_html(index=False, justify='left')
	html = base_html + summary_html
	file_name = 'test_quality_check.html'

	with open(file_name, 'w') as file:
	    file.write(html)

ws_pairs = sort_pairing(pair_xls)
worksheet_dirs = os.listdir(ws_dir)


for k,v in ws_pairs.items():
	ws_1 = v[0]
	ws_2 = v[1]

	if ws_1 in worksheet_dirs and ws_2 in worksheet_dirs:
		run_quality_check(ws_1, ws_2, out_dir, ws_dir)


os.chdir(out_dir)
file_list = os.listdir()
summary_df = pd.DataFrame(columns=['Test case','Worksheet pair','Check 1', 'Check 2', 
									'Check 3', 'Check 4', 'Check 5','Check 6', 
									'Check 7', 'Check 8', 'Check 9', 'Check 10',
									'Check 11'])


test_case = 1
for i in file_list:
	with open(i , 'r') as file:
		html = file.read()
		html_tables = pd.read_html(i)
		pair = html_tables[1][6:7]['Worksheet'].values[0]
		results = html_tables[1]['Result'].values.tolist()

		results =  html_tables[1]['Result'].values.tolist()
		summary_df = summary_df.append({'Test case': test_case,
										'Worksheet pair': pair, 
										'Check 1': results[0],
										'Check 2': results[1], 
										'Check 3': results[2],
										'Check 4': results[3],
										'Check 5': results[4],
										'Check 6': results[5], 
										'Check 7': results[6],
										'Check 8': results[7],
										'Check 9': results[8],
										'Check 10': results[9],
										'Check 11': results[10]}, ignore_index=True)
	test_case += 1

os.chdir('..')
print(summary_df)
generate_html_output(summary_df)
