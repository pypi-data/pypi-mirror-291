import cv2
import numpy as np 

def fringe_generation(w,h,f,out_dir):
    """
    Create fringe pattern for three phases shifted by 0, 2π/3, 4π/3
    Parameters:
    - w: image width
    - h: image height
    - f: pitch frequency
    - out_dir: output directory
    """
    width, height = w, h  # Image dimensions
    fringe_frequency = f  # Fringe frequency
    # Create a meshgrid
    x = np.linspace(0, 2 * np.pi * fringe_frequency, width)
    y = np.linspace(0, height, height)
    X, Y = np.meshgrid(x, y)
    fringes = {}
    for i in range(3):
        phase_shift = i * 2 * np.pi / 3  # Phase shift: 0, 2π/3, 4π/3
        pattern = 0.5 + 0.5 * np.cos(X + phase_shift)  # Fringe pattern
        pattern *= 255 / pattern.max()
        fringes[str(i)] = pattern
        cv2.imwrite(out_dir + "sin" + str(i) + ".jpg", pattern)
    return fringes
    