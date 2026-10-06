from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from lafs_mct.numpy_verify import verify_exact_ccx_decomposition

def test_exact_ccx_reference():
    assert verify_exact_ccx_decomposition() < 1e-12
