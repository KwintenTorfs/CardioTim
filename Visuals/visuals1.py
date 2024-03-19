import os

from Calculations.dicomProcessing import Image
import matplotlib.pyplot as plt
import numpy as np


def segment_tissue(patient, hounsfield):
    low, high = hounsfield
    segment = np.logical_and(patient >= low, patient < high).astype(float)
    segment[segment == 0] = np.nan
    return patient * segment


# Map with scan data
source = r'E:\Ani Nikoghosyan - CT11 vs CT14\Data\Studie_014\CT14_Soft'
# Where your image will be saved (map on pc)
save_location = r'\\mixer\home1\ktorfs5\Mijn afbeeldingen'
# If you want to save the image
save = False
# Name of the file
filename = 'Lung 1'
# In which slice of the scan you want to measure
slice_nb = 20
# Window level of the CT image determines the hounsfield range
#  c = window center and w = window width
# So Hounsfield window from c - w/2 -> c + w/2
# Standard Lung window = -600, 1500
# Abdomen = 10, 400
#  ETC...
c, w = -600, 1500

# If you want a tissue overlay
tissue_overlay = True
# Hounsfield range for tissue segmentation
Hounsfield_range = [0, 170]

# If you want to zoom in on a region
zoom_in = False
position = (250, 250)
size_of_zoomed_window = 200


color_map = 'plasma'


ct = None
scan = None
for i, scan in enumerate(os.listdir(source)):
    if i == slice_nb:
        break

slab = Image(source, scan)
image = slab.raw_hu
ct = slab.body

if zoom_in:
    half = size_of_zoomed_window // 2
    image = image[position[0] - half: position[0] + half, position[1] - half: position[1] + half]
    ct = ct[position[0] - half: position[0] + half, position[1] - half: position[1] + half]


m, M = Hounsfield_range
segment_image = segment_tissue(ct, Hounsfield_range)
plt.imshow(image, cmap='gray', vmin=c - w / 2, vmax=c + w / 2)
if tissue_overlay:
    plt.imshow(segment_image, cmap=color_map, alpha=0.8)
plt.axis('off')
savefig = save_location + r'%s.png' % filename
if save:
    plt.savefig(savefig, dpi=300, bbox_inches='tight', pad_inches=0)
plt.show()
