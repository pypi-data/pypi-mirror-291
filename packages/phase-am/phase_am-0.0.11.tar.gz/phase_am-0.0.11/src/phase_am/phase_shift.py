import cv2
import numpy as np
import glob
import math
import os
import argparse
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from utils_camera import three_step_phase_shift, unwrap_phase, manual_fft_filter, unwrap_ref_phase
from utils_phase_generate import fringe_generation
from scipy import signal
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import make_axes_locatable



def height_reconstruction(ref_img, target_img):
    ref_wrapped = three_step_phase_shift(ref_img)
    target_wrapped = three_step_phase_shift(target_img)
    ref_unwrapped = unwrap_phase(ref_wrapped)
    target_unwrapped = unwrap_ref_phase(target_wrapped, ref_unwrapped)
    #target_unwrapped = unwrap_phase(target_wrapped)
    # height = np.abs(manual_fft_filter(target_unwrapped)-manual_fft_filter(ref_unwrapped))
    height = np.abs(manual_fft_filter(target_unwrapped - ref_unwrapped))


