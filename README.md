# EAS 510 - Assignment 1: Digital Forensics Apprentice

A rule-based expert system that matches modified images back to their originals.

This is the **starter repository** for Project 1. Two repositories matter:

| Repository | Role |
|------------|------|
| `delveccj/EAS510_Assignment1_starter` (this repo) | Your **code** lives here. You will fork it, work in your fork, and push your final submission here. |
| `delveccj/EAS510_Assignment1` | The **dataset** (read-only). Clone it for the images; never commit it to your fork. |

## Setup on your Codio box

```bash
# 1. Fork this repo on GitHub, then in your box:
git clone https://github.com/YOUR-USERNAME/EAS510_Assignment1_starter.git
cd EAS510_Assignment1_starter

# 2. Clone the read-only dataset as a sibling folder (images live there):
cd ~/workspace
git clone https://github.com/delveccj/EAS510_Assignment1.git

# 3. Install dependencies:
cd ~/workspace/EAS510_Assignment1_starter
python3 -m pip install -r requirements.txt

# 4. Point this box at YOUR fork (run once):
./setup_git.sh
```

## Repository layout

```
forensics_detective.py   SimpleDetector: register targets + find_best_match
rules.py                 Rule functions (Rule 1: Metadata, Rule 2: Histogram, Rule 3: Template)
test_system.py           Runs the detector over the data folders and writes results_*.txt
scripts/check_output_format.py   Validates a results file against the required format
setup_git.sh, submit.sh  One-time setup + commit/push helper ("backup button")
```

## The task in one paragraph

Implement three interpretable rules (metadata, color histogram, template matching)
that combine into a 0-100 confidence score. Run your system on `modified_images/`
and `random/` and save the full output as `results_v1.txt`. In Phase 2, run on
`hard/`, diagnose a systematic failure, add a **Rule 4**, and save
`results_v1_hard.txt` and `results_v2.txt`. Full instructions are in the Codio guide
and in the assignment PDF in UBLearns.

## Running

```bash
# Phase 1 (easy + random) -> results_v1.txt
python3 test_system.py --modified --random --output results_v1.txt

# Phase 1 on hard cases -> results_v1_hard.txt
python3 test_system.py --hard --output results_v1_hard.txt

# Phase 2 (everything) -> results_v2.txt
python3 test_system.py --modified --hard --random --output results_v2.txt

# Validate any results file against the required format:
python3 scripts/check_output_format.py results_v1.txt
```

The data folders are resolved from a sibling clone of `EAS510_Assignment1`.
If your data is elsewhere, pass `--data-dir /path/to/EAS510_Assignment1`.

## Output format (do not alter)

```
Processing: modified_image_01.jpg
Rule 1 (Metadata): FIRED - Size ratio 0.85 -> 20/30 points
Rule 2 (Histogram): FIRED - Correlation 0.92 -> 25/30 points
Rule 3 (Template): FIRED - Match score 0.76 -> 30/40 points
Final Score: 75/100 -> MATCH to original_03.jpg
```

## Backup doctrine

Your Codio box can be reset at any time. **Your fork on GitHub is the only safe
copy.** After every milestone run `./submit.sh "describe what you did"`. A box
restart never touches GitHub.

## License

Apache 2.0. See `LICENSE`.


## Observed weakness in V1: what failed and why
- In my V1 hard-case results, cropping was the biggest weakness.
- v1 (off-center crop + compression): 0 out of 10 matched.
- v2 (crop + brightness + compression): 0 out of 10 matched.
- v6 (crop + resize): 5 out of 10 matched.
- Resize by itself was also weaker: v3 matched 4 out of 10.


## Design decision for V2: what Rule 4 is and why you chose it
- I added Rule 4 using Canny edge detection.
- I chose it because the main V1 weakness was cropped images.
- The rule converts both images to grayscale and finds edges using cv2.Canny.
- It then compares the edge maps using template matching.
- The idea is to compare image structure instead of depending only on color or file size.
- I used the 25/25/40/10 point split so all four rules still total 100.


## Effect of the change: accuracy before/after on easy vs hard
- V1 hard result: 29 matched and 31 rejected out of 60 hard images.
- V2 processed all 135 required images and produced 56 matches and 79 rejections.
- The format checker passed: PASS: results_v2.txt (135 images).


## Trade-offs: what new costs or risks did Rule 4 introduce
- Rule 4 adds more image processing because Canny edge detection and template matching must run for every comparison.
- This made V2 slower than V1.
- Edge matching can still be weak when an image is resized, cropped heavily, or changed enough that the edges do not align.
- Adding Rule 4 also required reducing Rule 1 and Rule 2 from 30 points to 25 points each so the total remained 100.
