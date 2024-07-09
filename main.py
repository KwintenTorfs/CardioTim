import numpy as np
import pandas as pd
from Calculations.dicomProcessing import Image, ImageStack



def calculate_offcenter(image):
    mask = image.mask
    columns = np.any(mask, axis=1)
    rows = np.any(mask, axis=0)

    left = rows.nonzero()[0][0]
    right = rows.nonzero()[0][-1]
    up = columns.nonzero()[0][0]
    down = columns.nonzero()[0][-1]

    patient_center = np.array([(right + left) / 2 * image.PixelSize, (down + up) / 2 * image.PixelSize, 0])
    patient_center_upper_limit = np.array(
        [(right + left + 4) / 2 * image.PixelSize, (down + up + 4) / 2 * image.PixelSize, 0])
    patient_center_lower_limit = np.array(
        [(right + left - 4) / 2 * image.PixelSize, (down + up - 4) / 2 * image.PixelSize, 0])

    Isocenter = image.MatrixCenter + image.DataCollectionCenter - image.ReconstructionTargetCenter

    offcenter = Isocenter - patient_center
    offcenter_upper_limit = Isocenter - patient_center_upper_limit
    offcenter_lower_limit = Isocenter - patient_center_lower_limit

    return offcenter, offcenter_upper_limit, offcenter_lower_limit

results = []

path = r'C:\Users\tbusse1\cardiac_studies\ct_14\flash_coronary_CTA_IQ65\study_11\full_FOV'


image_stack = ImageStack(path)

for idx, slab in enumerate(image_stack.slices):

    offcenter, offcenter_upper_limit, offcenter_lower_limit = calculate_offcenter(slab)
    # if up == 1:
    #     print('Carefull, lower edge truncated')
    # if left == 1:
    #     print('Carefull, right edge truncated')
    # if down == 512:
    #     print('Carefull, upper edge truncated')
    # if right == 512:
    #     print('Carefull, left edge truncated')

    result = {
        'ImageIndex': idx,
        'OffcenterX': offcenter[0], 'OffcenterY': offcenter[1],
        'UpperLimitX': offcenter_upper_limit[0], 'UpperLimitY': offcenter_upper_limit[1],
        'LowerLimitX': offcenter_lower_limit[0], 'LowerLimitY': offcenter_lower_limit[1]
    }
    results.append(result)

df = pd.DataFrame(results)
df.to_excel("study_11_positioning.xlsx")



# isocenter_coordinates = np.true_divide(image.ISOCENTER[1:], image.dimensions)
# patient_center_matrix = np.true_divide(patient_center[1:], image.dimensions)
#
#
# centers = np.zeros(image.raw_hu.shape)
#
# x1, y1 = int(isocenter_coordinates[0]), int(isocenter_coordinates[1])
# x2, y2 = int(patient_center_matrix[0]), int(patient_center_matrix[1])
#
# r = 5
#
# centers[x1-r:x1+r, y1-r:y1+r] = 10
# centers[x2-r:x2+r, y2-r:y2+r] = 5
#
#
# plt.imshow(image.raw_hu, cmap='gray', vmin=-1500, vmax=300)
# plt.imshow(centers, cmap='Reds', alpha=0.5)
# plt.show()

