import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from summarize_results import latest_per_run  # noqa: E402


class LatestPerRun(unittest.TestCase):
    def test_rerun_replaces_earlier_row(self):
        k = dict(scenario='s', profile='p', hours='9 10', demand='0.6', controller='fixed')
        rows = [k | {'seed': '0', 'delay_s': '1'}, k | {'seed': '1', 'delay_s': '2'},
                k | {'seed': '0', 'delay_s': '9'}]
        kept, dropped = latest_per_run(rows)
        self.assertEqual(dropped, 1)
        self.assertEqual(sorted(r['delay_s'] for r in kept), ['2', '9'])


if __name__ == '__main__':
    unittest.main()
