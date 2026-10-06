from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from lafs_mct.metrics import exact_removed_work_threshold, latency_break_even

def test_exact_reliability_threshold():
    assert abs(exact_removed_work_threshold(1e-4,1e-3)-0.0023981405239318354)<1e-15

def test_n16_mixed_threshold():
    assert abs(latency_break_even(115,67,91,89,1.0,0.2)-48.4)<1e-12
