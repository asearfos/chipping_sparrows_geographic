import glob
import time

directory = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation/"
files = glob.glob(directory + '/**/*_tossed.txt', recursive=True)
output_name = directory + "/tossed_compiled_list_" + time.strftime("%Y%m%d_T%H%M%S")

tossed = []
for file in glob.glob(directory + '/**/*_tossed.txt', recursive=True):
    f = open(file)
    tossed.extend(f.read().splitlines()[1:])
print(tossed)


output_file = open(output_name, 'w')
for bout in tossed:
    output_file.write(bout + '\n')
