# helpers.py
from multiprocessing import Pool
from process_image import process_image

def process_image_full(args):
    """
    Expects args as a tuple:
      (frame_number, image, masks, threshold, max_iters, step_size, n_steps, n_wedges, n_rad_bins)
    Calls process_image with these arguments.
    """
    return process_image(*args)

# Define a helper function to process a chunk of images.
def process_chunk(start_idx, images_chunk, mask, pbar, threshold, max_iters, step_size, n_steps, n_wedges, n_rad_bins):
    # Build argument list for each image in the chunk.
    args = []
    for idx, img in enumerate(images_chunk):
        frame_number = start_idx + idx
        args.append((
            frame_number,
            img,
            mask,
            threshold,
            max_iters,
            step_size,
            n_steps,
            n_wedges,
            n_rad_bins
        ))
    results = []
    with Pool() as pool:
        # Use imap_unordered to yield results as they become available.
        for result in pool.imap_unordered(process_image_full, args):
            results.append(result)
            pbar.update(1)
    return results
