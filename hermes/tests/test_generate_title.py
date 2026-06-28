import unittest

from hermes.tasks.generate_title import parse_titles, run


class FakeGateway:
    def __init__(self, content):
        self.content = content

    def generate_text(self, messages, **kwargs):
        return self.content


class ParseTitlesTests(unittest.TestCase):
    def test_json_array(self):
        self.assertEqual(parse_titles('["A", "B"]'), ["A", "B"])

    def test_json_in_code_fence(self):
        self.assertEqual(parse_titles('```json\n["A", "B"]\n```'), ["A", "B"])

    def test_numbered_list(self):
        self.assertEqual(parse_titles("1. First\n2) Second\n- Third"), ["First", "Second", "Third"])

    def test_keeps_leading_number_in_title(self):
        # "5 Cara ..." must not lose its leading number.
        self.assertEqual(parse_titles("5 Cara Sholat Tahajud"), ["5 Cara Sholat Tahajud"])


class RunTests(unittest.TestCase):
    def test_run_truncates_to_requested(self):
        gw = FakeGateway('["A", "B", "C"]')
        out = run({"keyword": "k", "n_titles": 2, "project": {}}, gw)
        self.assertEqual(out["titles"], ["A", "B"])
        self.assertEqual(out["returned"], 2)


if __name__ == "__main__":
    unittest.main()
