"""
main.py
========
End-to-end workflow automation for the NBA Productivity vs. Compensation project.
Runs all pipeline stages from data acquisition through analysis in one command.

Usage:
    python main.py              # Run full pipeline (uses cached raw data if available)
    python main.py --fetch      # Re-fetch raw data from APIs before running pipeline
    python main.py --verify     # Only verify SHA-256 checksums of existing data
"""

import subprocess
import sys
import os
import hashlib
import json
import argparse
from datetime import datetime

# ── Configuration ────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
DATA_RAW = os.path.join(PROJECT_ROOT, "data", "raw")
DATA_PROCESSED = os.path.join(PROJECT_ROOT, "data", "processed")
RESULTS_DIR = os.path.join(PROJECT_ROOT, "results")
CHECKSUM_FILE = os.path.join(PROJECT_ROOT, "checksums.json")

# Expected raw data files
RAW_FILES = [
    "player_stats_traditional.csv",
    "player_stats_advanced.csv",
    "player_salaries.csv",
    "team_standings.csv",
]

# Pipeline stages in execution order
FETCH_SCRIPTS = [
    ("Fetching player stats (nba_api)", "fetch_player_stats.py"),
    ("Fetching salary data (Basketball-Reference)", "fetch_salaries.py"),
    ("Fetching team standings (Basketball-Reference)", "fetch_team_standings.py"),
]

PIPELINE_SCRIPTS = [
    ("Cleaning raw data", "clean_data.py"),
    ("Integrating datasets (SQL joins)", "integrate_nba_data.py"),
    ("Running analysis and generating visualizations", "final_analysis.py"),
]


def compute_sha256(filepath):
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def generate_checksums():
    """Generate SHA-256 checksums for all data files and save to checksums.json."""
    checksums = {"generated_at": datetime.now().isoformat(), "files": {}}

    for directory in [DATA_RAW, DATA_PROCESSED, RESULTS_DIR]:
        if not os.path.exists(directory):
            continue
        for filename in sorted(os.listdir(directory)):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                rel_path = os.path.relpath(filepath, PROJECT_ROOT)
                checksums["files"][rel_path] = compute_sha256(filepath)

    with open(CHECKSUM_FILE, "w") as f:
        json.dump(checksums, f, indent=2)

    print(f"\n{'='*60}")
    print(f"SHA-256 checksums saved to: {CHECKSUM_FILE}")
    print(f"Total files checksummed: {len(checksums['files'])}")
    for path, sha in checksums["files"].items():
        print(f"  {sha[:16]}...  {path}")
    return checksums


def verify_checksums():
    """Verify existing files against stored checksums."""
    if not os.path.exists(CHECKSUM_FILE):
        print("ERROR: checksums.json not found. Run 'python main.py' first.")
        return False

    with open(CHECKSUM_FILE, "r") as f:
        stored = json.load(f)

    print(f"Verifying checksums (generated: {stored['generated_at']})...")
    all_ok = True
    for rel_path, expected_hash in stored["files"].items():
        filepath = os.path.join(PROJECT_ROOT, rel_path)
        if not os.path.exists(filepath):
            print(f"  MISSING: {rel_path}")
            all_ok = False
            continue
        actual_hash = compute_sha256(filepath)
        if actual_hash == expected_hash:
            print(f"  OK:      {rel_path}")
        else:
            print(f"  CHANGED: {rel_path}")
            print(f"           Expected: {expected_hash[:32]}...")
            print(f"           Actual:   {actual_hash[:32]}...")
            all_ok = False

    if all_ok:
        print("\nAll checksums verified successfully.")
    else:
        print("\nWARNING: Some files are missing or have changed.")
    return all_ok


def run_script(description, script_name):
    """Run a Python script and handle errors."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print(f"\n{'─'*60}")
    print(f"STAGE: {description}")
    print(f"  Script: scripts/{script_name}")
    print(f"{'─'*60}")

    result = subprocess.run(
        [sys.executable, script_path],
        cwd=PROJECT_ROOT,
        capture_output=False,
    )

    if result.returncode != 0:
        print(f"\n  ERROR: {script_name} exited with code {result.returncode}")
        sys.exit(1)

    print(f"  Completed: {description}")


def check_raw_data_exists():
    """Check if all raw data files are present."""
    missing = []
    for filename in RAW_FILES:
        if not os.path.exists(os.path.join(DATA_RAW, filename)):
            missing.append(filename)
    return missing


def main():
    parser = argparse.ArgumentParser(
        description="NBA Productivity vs. Compensation - Workflow Automation"
    )
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Re-fetch raw data from APIs (requires internet connection)",
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Only verify SHA-256 checksums of existing data files",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("NBA Productivity vs. Compensation Analysis")
    print("End-to-End Workflow Automation")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Verify-only mode
    if args.verify:
        verify_checksums()
        return

    # Ensure output directories exist
    os.makedirs(DATA_RAW, exist_ok=True)
    os.makedirs(DATA_PROCESSED, exist_ok=True)
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # ── Stage 1: Data Acquisition ────────────────────────────────
    if args.fetch:
        print("\n[STAGE 1/4] DATA ACQUISITION (--fetch mode)")
        for desc, script in FETCH_SCRIPTS:
            run_script(desc, script)
    else:
        missing = check_raw_data_exists()
        if missing:
            print(f"\nERROR: Missing raw data files: {missing}")
            print("Run with --fetch to download from APIs, or add files to data/raw/")
            sys.exit(1)
        print("\n[STAGE 1/4] DATA ACQUISITION")
        print("  Using existing raw data in data/raw/ (run with --fetch to re-download)")

    # ── Stage 2: Data Cleaning ───────────────────────────────────
    print("\n[STAGE 2/4] DATA CLEANING")
    run_script("Cleaning raw data", "clean_data.py")

    # ── Stage 3: Data Integration ────────────────────────────────
    print("\n[STAGE 3/4] DATA INTEGRATION")
    run_script("Integrating datasets (SQL joins)", "integrate_nba_data.py")

    # ── Stage 4: Analysis & Visualization ────────────────────────
    print("\n[STAGE 4/4] ANALYSIS & VISUALIZATION")
    run_script("Running analysis and generating visualizations", "final_analysis.py")

    # ── Generate SHA-256 Checksums ───────────────────────────────
    generate_checksums()

    # ── Summary ──────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print("WORKFLOW COMPLETE")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    print("Outputs:")
    print(f"  Cleaned data:      {DATA_PROCESSED}/")
    print(f"  SQLite database:   data/processed/nba_project.db")
    print(f"  Integrated CSV:    data/processed/integrated_nba_data.csv")
    print(f"  Visualizations:    {RESULTS_DIR}/")
    print(f"  Checksums:         {CHECKSUM_FILE}")
    print(f"\nTo verify data integrity: python main.py --verify")


if __name__ == "__main__":
    main()
