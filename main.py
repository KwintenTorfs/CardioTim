from Calculations.dicomProcessing import Image, ImageStack
import matplotlib.pyplot as plt

location = r'E:\Ani Nikoghosyan - CT11 vs CT14\Data\Studie_014\CT14_Soft'

file = r'Studie_014_CT14_Soft_054.dcm'

stack = ImageStack(location)

slab = stack.slices[50]