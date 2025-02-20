# -------------------------
# Automate Evaluation and Integration
# -------------------------
import traceback
from tqdm import tqdm
from process_all_stream_files import process_all_stream_files
from read_stream_write_sol import read_stream_write_sol
from append_event_count import append_event_count
def automate_evaluation(stream_file_folder: str, weight_list, lattice: str):

    """
    Process a stream file to extract and normalize chunk metrics.

    This function reads a stream file from the given file path, extracts data chunks
    (delimited by "----- Begin chunk -----"), and computes several metrics for each chunk.
    It filters out chunks that are unindexed (i.e., those containing "indexed_by = none").
    For each valid chunk, the function collects metrics such as weighted RMSD, length deviation,
    angle deviation, and others (including a new metric: percentage_indexed). It then normalizes
    these metrics to a value between 0 and 1 and computes a combined metric using provided or
    default weights.

    Parameters:
        stream_file_path (str):
            The full path to the stream file that contains the data chunks.
        
        metric_weights (dict, list, tuple, optional):
            Weights to be applied to each metric when computing the combined metric.
            The order (or keys) should correspond to the following metric names:
                - 'weighted_rmsd'
                - 'length_deviation'
                - 'angle_deviation'
                - 'peak_ratio'
                - 'percentage_indexed'
            
            If a list or tuple is provided, it must have the same number of elements as the
            metrics above. If not provided (or None), a set of default weights is used.
    """
    
    append_event_count(stream_file_folder)
    for weight in weight_list:
        try:
            wrmsd_weight, wrmsd_pi_weight, cld_weight, cad_weight, pr_weight, ipp_weight = weight

            IQM = f"IQM_SUM_{wrmsd_weight}_{wrmsd_pi_weight}_{cld_weight}_{cad_weight}_{pr_weight}_{ipp_weight}"

            # Evaluate multiple stream files
            print(f"Evaluating multiple stream files with weights: {weight}")
            process_all_stream_files(stream_file_folder, weight)

            # # Write stream file to .sol file
            best_results_stream = f"{stream_file_folder}/best_results_{IQM}.stream"
            tqdm.write(f"Writing .sol file from stream: {best_results_stream}")
            num_indexed_frames = read_stream_write_sol(best_results_stream, lattice)
            print(f"Total number of indexed frames : {num_indexed_frames}")
        
        except Exception as e:
            tqdm.write(f"An error occurred during processing of weights {weight}: {e}")
            traceback.print_exc()
