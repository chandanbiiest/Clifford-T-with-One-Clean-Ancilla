from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from lafs_mct.numpy_verify import verify_measurement_release

def test_branch_maps_are_exact():
    result=verify_measurement_release()
    assert result["max_error"]<1e-12
    assert result["branch_probability_0"]==0.5
    assert result["branch_probability_1"]==0.5
