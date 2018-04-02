import glob
import time
import os

directory = "C:/Users/abiga\Box Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation/"
# files = glob.glob(directory + '/**/*_tossed.txt', recursive=True)
# output_name = directory + "/tossed_compiled_list_" + time.strftime("%Y%m%d_T%H%M%S")

# get list of all tossed files coming out of chipper
tossed = []
for tossed_file in glob.glob(directory + '/**/*_tossed.txt', recursive=True):
    tf = open(tossed_file)
    tossed.extend(tf.read().splitlines()[1:])
print(len(tossed))

# get list of all tossed files that I either re-ran or chose another bout to run (chipping sparrow tossed retry bouts)
retry = []
for retry_file in glob.glob(directory + '/chipping sparrow tossed retry bouts/*/*.wav', recursive=True):
    retry.append(os.path.basename(retry_file))
print(len(retry))

# get list of all the files I tossed a second time (after retrying)
tossed_again = []
for again_file in glob.glob(directory + '/chipping sparrow tossed retry bouts/**/*_tossed.txt', recursive=True):
    ta = open(again_file)
    tossed_again.extend(ta.read().splitlines()[1:])
print(len(tossed_again))

# create list of the files I recovered by retrying (difference between retry and tossed_again)
recovered = [x for x in retry if x not in tossed_again]
print(len(recovered))

# get list of the missing bouts that I ran through chipper and tossed
missing_tossed = []
for missing_file in glob.glob(directory + '/chipping sparrow missing recordings bouts/**/*_tossed.txt', recursive=True):
    mt = open(missing_file)
    missing_tossed.extend(mt.read().splitlines()[1:])
print(len(missing_tossed))

output_name = directory + "/tossed_retry_bouts_compiled_list_" + time.strftime("%Y%m%d_T%H%M%S") + '.csv'
output_file = open(output_name, 'w')
for bout in tossed_again:
    output_file.write(bout + '\n')
