You are provided a dataset that represents a 21 minute sample from the vessel in a file seaflow_21min.csv. This sample has been pre-processed to remove the calibration "beads" that are passed through the system for monitoring, as well as some other particle types.

The columns of this dataset are as follows:

file_id, time, cell_id, d1, d2, fsc_small, fsc_perp, fsc_big, pe, chl_small, chl_big, pop     
file_id: The data arrives in files, where each file represents a three-minute window; this field represents which file the data came from. The number is ordered by time, but is otherwise not significant.
time: This is an integer representing the time the particle passed through the instrument. Many particles may arrive at the same time; time is not a key for this relation.
cell_id: A unique identifier for each cell WITHIN a file. (file_id, cell_id) is a key for this relation.
d1, d2: Intensity of light at the two main sensors, oriented perpendicularly. These sensors are primarily used to determine whether the particles are properly centred in the stream. Used primarily in pre-processing; they are unlikely to be useful for classification.
fsc_small, fsc_perp, fsc_big: Forward scatter small, perpendicular, and big. These values help distinguish different sizes of particles.
pe: A measurement of phycoerythrin fluorescence, which is related to the wavelength associated with an orange colour in micro organisms
chl_small, chl_big: Measurements related to the wavelength of light corresponding to chlorophyll.
pop: This is the class label assigned by the clustering mechanism used in the production system. It can be considered "ground truth" for the purposes of the assignment, but note that there are particles that cannot be unambiguously classified, so you should not aim for 100% accuracy. The values in this column are crypto, nano, pico, synecho, and ultra
