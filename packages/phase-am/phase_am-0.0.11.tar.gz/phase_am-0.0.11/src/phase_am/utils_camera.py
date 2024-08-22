import cv2
import numpy as np
import glob
import math
import os
import argparse



def three_step_phase_shift(img_input, cxy = None):
    ### img_input:  dictionary of the three images {}"1", "2", "3"}
    ### return the wrapped phase map
    Y = 0
    X = 0
    for i in range(1,4):
        II = img_input[str(i)]
        sigma = 2*(i-1)*np.pi/3
        Y = Y = Y + np.sin(sigma) *II
        X = X + np.cos(sigma) * II
    phase_map = np.arctan2(-Y,X)
    return phase_map

def unwrap_phase(phase_map):
    """
    Unwrap a 2D wrapped phase map.

    Parameters:
    - phase_map: 2D numpy array containing the wrapped phase values.

    Returns:
    - 2D numpy array containing the unwrapped phase values.
    """
    # Unwrap along the first axis (e.g., rows)
    unwrapped_phase_along_first_axis = np.unwrap(phase_map, axis=0)
    
    # Then, unwrap along the second axis (e.g., columns) on the already row-unwrapped phase map
    unwrapped_phase = np.unwrap(unwrapped_phase_along_first_axis, axis=1)
    
    return unwrapped_phase




def unwrap_ref_phase(phase_map, unwrapped_ref):
    phi_u = phase_map + 2*np.pi*np.round((unwrapped_ref-phase_map)/(2*np.pi))
    return phi_u

def manual_fft_filter(phi, filter_freq, x_step, y_step):
    FT=np.fft.fftshift(np.fft.fft2(phi))
    FT[filter_freq[0]:filter_freq[0]+x_step,filter_freq[1]:filter_freq[1]+y_step]=0
    uphi = np.abs(np.fft.ifft2(np.fft.ifftshift(FT)))
    return uphi