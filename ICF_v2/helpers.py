# helpers.py (or at the top of your main script)
from process_image import process_image

def process_image_full(args):
    """
    Expects args as a tuple:
      (frame_number, image, masks, threshold, max_iters, step_size, n_steps, n_wedges, n_rad_bins, plot_profiles)
    Calls process_image with these arguments.
    """
    return process_image(*args)
