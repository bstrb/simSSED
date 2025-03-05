import csv

def read_metric_csv(csv_path, group_by_event=True):
    """
    Reads a CSV of metrics, keeping 'event_number' as a string.
    Skips rows like:  "Event number: 0-1,,,,,,,".
    Parses all metric columns as floats (including negative values).

    Returns:
      - If group_by_event=True:
          A dictionary of { event_number_str -> list of row dicts }
      - If group_by_event=False:
          A flat list of row dicts.
    """

    rows = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)

        for r in reader:
            # Skip lines where stream_file starts with "Event number:"
            # Those are just group-heading lines, not data rows.
            if r['stream_file'].startswith("Event number:"):
                continue

            # Keep event_number as a string. For example, "0-1", "1-1", etc.
            event_str = r['event_number']

            # Parse numeric metrics as floats, skipping rows that can't parse
            try:
                r['event_number']         = event_str  # e.g. "0-1"
                r['combined_metric']      = float(r['combined_metric'])
                r['weighted_rmsd']       = float(r['weighted_rmsd'])
                r['fraction_outliers']    = float(r['fraction_outliers'])
                r['length_deviation']     = float(r['length_deviation'])
                r['angle_deviation']      = float(r['angle_deviation'])
                r['peak_ratio']           = float(r['peak_ratio'])
                r['percentage_unindexed'] = float(r['percentage_unindexed'])
            except (ValueError, KeyError):
                # This row doesn't have valid floats in the right columns, skip it
                continue

            rows.append(r)

    if not group_by_event:
        return rows

    # Group rows by their (string) event_number
    grouped = {}
    for row in rows:
        evt_id = row['event_number']
        grouped.setdefault(evt_id, []).append(row)

    return grouped


def select_best_results_by_event(grouped_data, sort_metric='combined_metric'):
    """
    Given a dict { event_number_str -> list of row dicts },
    return a flat list of the 'best' row (lowest `sort_metric`) per event.
    """
    best_list = []
    for evt_str, rowlist in grouped_data.items():
        # Pick the row with the smallest 'sort_metric'
        best = min(rowlist, key=lambda x: x[sort_metric])
        best_list.append(best)
    return best_list


def get_metric_ranges(rows, metrics=None):
    """
    Given a list of row dicts (all with the same keys),
    compute (min, max) for each metric in `metrics`.

    Returns a dict:
      {
        'combined_metric': (min_val, max_val),
        'weighted_rmsd': (min_val, max_val),
        ...
      }

    If `metrics` is None, we use a default list of known metrics.
    If a metric has no data in 'rows', we default to (0.0, 1.0).
    """
    if not metrics:
        metrics = [
            'combined_metric', 'weighted_rmsd', 'fraction_outliers',
            'length_deviation', 'angle_deviation', 'peak_ratio',
            'percentage_unindexed'
        ]

    ranges = {}
    for m in metrics:
        vals = [r[m] for r in rows if m in r]
        if len(vals) == 0:
            ranges[m] = (0.0, 1.0)  # Fallback
        else:
            mn = min(vals)
            mx = max(vals)
            ranges[m] = (mn, mx)
    return ranges


def filter_rows(rows, thresholds):
    """
    Filter a list of row dicts by threshold dict, e.g.:
      thresholds = { 'combined_metric': 0.5, 'weighted_rmsd': 1.0, ... }

    We keep the row if row[metric] <= threshold for all metrics in the dict.
    """
    def passes(r):
        for metric, thr in thresholds.items():
            if r[metric] > thr:
                return False
        return True

    return [r for r in rows if passes(r)]


def write_filtered_stream(rows, original_stream_path, output_stream_path):
    """
    Writes a new stream file containing only events in 'rows'.
    We assume each chunk in 'original_stream_path' has a line "Event: X"
    matching row['event_number'] as a string.

    - read original stream chunk-by-chunk
    - parse out the event ID from lines containing "Event:"
    - if event_number is in the set of kept IDs, write that chunk
    """
    keep_evt_ids = set(r['event_number'] for r in rows)

    with open(original_stream_path, 'r') as infile, open(output_stream_path, 'w') as outfile:
        lines = infile.readlines()

        header_lines = []
        chunk_lines = []
        inside_chunk = False
        wrote_header = False

        for line in lines:
            if line.startswith("----- Begin chunk -----"):
                inside_chunk = True
                if not wrote_header:
                    # Write any lines we collected as "header" so far
                    outfile.writelines(header_lines)
                    wrote_header = True
            elif line.startswith("----- End chunk -----"):
                inside_chunk = False

                # see if chunk_lines has an "Event: ???"
                evt_str = None
                for cl in chunk_lines:
                    if "Event:" in cl:
                        # parse out the entire string after "Event:"
                        evt_str = cl.split("Event:")[1].strip()
                        break

                if evt_str is not None and evt_str in keep_evt_ids:
                    outfile.write("----- Begin chunk -----\n")
                    outfile.writelines(chunk_lines)
                    outfile.write("----- End chunk -----\n")

                chunk_lines = []
            else:
                if inside_chunk:
                    chunk_lines.append(line)
                else:
                    # still in the header region
                    header_lines.append(line)

    print(f"Filtered stream written to: {output_stream_path}")
