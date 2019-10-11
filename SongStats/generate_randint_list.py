import numpy as np

seed_array = np.random.randint(1048576, size=1000)

np.savetxt('C:/Users/abiga\Box '
           'Sync\Abigail_Nicole\ChippiesProject\FinalDataCompilation'
           '\RandomSeeds.csv',
           seed_array, delimiter=",", fmt='%s')

print(seed_array)

