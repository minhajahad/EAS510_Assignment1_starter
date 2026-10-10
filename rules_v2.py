"""EAS 510 - Project 1 - Phase 2: the V2 rule set.

Rules 1-3 are kept exactly as in `rules.py`. Your job is to ADD Rule 4 that
targets the systematic weakness you diagnosed from results_v1_hard.txt.

Constraint: the rules' `out_of` weights must still sum to 100 so the Final
Score stays on a /100 scale (the format validator enforces "Final Score:
<s>/100" equals the sum of the block's rule scores).

Example split that keeps the original spirit: Rules 1-3 -> 25/25/40 and
Rule 4 -> 10 (or trim the losers more aggressively).
"""

import rules
import cv2
import numpy as np

#: Import the original rules and append your new one.
RULES = ("rule1_metadata_v2", "rule2_histogram_v2", "rule3_template", "rule4_edges")

def rule1_metadata_v2(target, input_path):
    out = rules.rule1_metadata(target, input_path)

    out["out_of"] = 25

    if out["fired"]:
        out["score"] = int(round(25 * out["metric"]))

    return out


def rule2_histogram_v2(target, input_path):
    out = rules.rule2_histogram(target, input_path)

    out["out_of"] = 25

    if out["fired"]:
        out["score"] = int(round(25 * out["metric"]))

    return out


def rule4_edges(target, input_path):
    """Compare Canny edge maps to help with cropped images."""

    out = {
        "rule": 4,
        "name": "Edges",
        "fired": False,
        "score": 0,
        "out_of": 10,
        "note": "Edge match 0.00",
        "metric": 0.0,
    }

    try:
        src = cv2.imread(target["path"], cv2.IMREAD_GRAYSCALE)
        inp = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)

        if src is None or inp is None:
            return out

        src_edges = cv2.Canny(src, 100, 200)
        inp_edges = cv2.Canny(inp, 100, 200)

        if (inp_edges.shape[0] > src_edges.shape[0] or
                inp_edges.shape[1] > src_edges.shape[1]):

            scale = min(
                src_edges.shape[1] / inp_edges.shape[1],
                src_edges.shape[0] / inp_edges.shape[0]
            )

            new_w = max(1, int(inp_edges.shape[1] * scale))
            new_h = max(1, int(inp_edges.shape[0] * scale))

            inp_edges = cv2.resize(inp_edges, (new_w, new_h))

        result = cv2.matchTemplate(
            src_edges,
            inp_edges,
            cv2.TM_CCOEFF_NORMED
        )

        metric = float(result.max())

        out["metric"] = round(max(0.0, min(1.0, metric)), 3)
        out["note"] = f"Edge match {out['metric']:.2f}"

        if out["metric"] >= 0.4:
            out["fired"] = True
            out["score"] = int(round(out["out_of"] * out["metric"]))

    except Exception:
        pass

    return out
