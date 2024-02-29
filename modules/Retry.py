import yaml

# Variables
store_words = []

# Reading configuration file (Check config/config.yml)
with open("../config/config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

# File name and location
filename = '..\\logs\\Metric\\Metric_Logs.txt'
tmp_filename = '..\\tmp\\retry_count.txt'

with open(filename, 'r') as file:
    for line in file:
        for word in line.split():
            store_words.append(word)

# if 'PASS' in store_words:
#     with open(tmp_filename, 'w') as tmp_file:
#         if line in file == '0':
#             print("One")
#             tmp_file.write('1')
#         elif line in file == '1':
#             print("One")
#             tmp_file.write('2')
#         elif line in file == '2':
#             print("Two")
#             tmp_file.write('3')
#         elif line in file == '3':
#             tmp_file.write('0')
# tmp_file.close()