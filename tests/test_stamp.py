import subprocess


def test_stamp_iso():
    out = subprocess.check_output(["python3", "dct.py", "stamp", "--iso"], text=True).strip()
    assert "T" in out

