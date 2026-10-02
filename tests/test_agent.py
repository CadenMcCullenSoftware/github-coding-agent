import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "agent.py"
spec = importlib.util.spec_from_file_location("coding_agent", MODULE_PATH)
agent = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(agent)


class AgentSafetyTests(unittest.TestCase):
    def test_patch_paths_accept_ordinary_source(self):
        patch = "diff --git a/src/app.py b/src/app.py\n--- a/src/app.py\n+++ b/src/app.py\n@@ -1 +1 @@\n-old\n+new\n"
        self.assertEqual(agent.patch_paths(patch), {"src/app.py"})

    def test_patch_paths_reject_workflow_changes(self):
        patch = "diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml\n--- a/.github/workflows/ci.yml\n+++ b/.github/workflows/ci.yml\n@@ -1 +1 @@\n-old\n+new\n"
        with self.assertRaises(agent.AgentError):
            agent.patch_paths(patch)

    def test_patch_paths_reject_parent_traversal(self):
        patch = "diff --git a/../outside.py b/../outside.py\n--- a/../outside.py\n+++ b/../outside.py\n@@ -1 +1 @@\n-old\n+new\n"
        with self.assertRaises(agent.AgentError):
            agent.patch_paths(patch)

    def test_patch_paths_reject_secret_files(self):
        patch = "diff --git a/config/api_key.txt b/config/api_key.txt\n--- a/config/api_key.txt\n+++ b/config/api_key.txt\n@@ -1 +1 @@\n-old\n+new\n"
        with self.assertRaises(agent.AgentError):
            agent.patch_paths(patch)

    def test_trusted_task_requires_trusted_author(self):
        event = {
            "comment": {"author_association": "CONTRIBUTOR", "body": "/agent change code"},
            "issue": {"number": 12},
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            json.dump(event, handle)
            handle.flush()
            with self.assertRaises(agent.AgentError):
                agent.trusted_task(handle.name)

    def test_trusted_task_extracts_command(self):
        event = {
            "comment": {"author_association": "MEMBER", "body": "/agent Add a test"},
            "issue": {"number": 12},
        }
        with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
            json.dump(event, handle)
            handle.flush()
            self.assertEqual(agent.trusted_task(handle.name), ("Add a test", 12))


if __name__ == "__main__":
    unittest.main()
