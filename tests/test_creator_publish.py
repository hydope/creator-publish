"""Tests: dry_run for every adapter (no network, no creds) + scheduler."""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# isolate the queue db before importing schedule
_tmp = tempfile.mkdtemp(prefix="cp-test-")
os.environ["CREATOR_PUBLISH_HOME"] = _tmp

from creator_publish.publish import ADAPTERS, publish  # noqa: E402
from creator_publish.schedule import (  # noqa: E402
    cancel, enqueue, list_jobs, parse_when,
)


class PublishTest(unittest.TestCase):
    def test_all_adapters_dry_run(self):
        video = Path(__file__)  # any existing file; size only
        for platform in ADAPTERS:
            with self.subTest(platform=platform):
                try:
                    res = publish(platform, video, title="t", description="d",
                                  hashtags=["#pov"], dry_run=True)
                except RuntimeError as e:
                    # adapters that need setup even for dry_run must say so
                    # clearly — but our contract is dry_run never needs creds
                    self.fail(f"{platform} dry_run raised: {e}")
                self.assertTrue(res.get("dry_run"), platform)
                self.assertEqual(res["platform"], platform)

    def test_unknown_platform(self):
        with self.assertRaises(ValueError):
            publish("myspace", Path(__file__), "t", "d", [],
                    dry_run=True)


class ScheduleTest(unittest.TestCase):
    def test_parse_when(self):
        dt = parse_when("Friday 6pm", "America/New_York")
        self.assertEqual(dt.strftime("%A"), "Friday")
        self.assertEqual(dt.hour, 18)

    def test_queue_round_trip(self):
        jid = enqueue(parse_when("tomorrow 9am", "America/New_York"),
                      "publish", {"platform": "youtube", "video": "x.mp4"})
        jobs = list_jobs("queued")
        self.assertTrue(any(j["id"] == jid for j in jobs))
        self.assertTrue(cancel(jid))
        self.assertFalse(any(j["id"] == jid for j in list_jobs("queued")))


if __name__ == "__main__":
    unittest.main()
