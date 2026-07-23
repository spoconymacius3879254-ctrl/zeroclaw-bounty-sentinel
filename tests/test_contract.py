import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "skills" / "bounty-sentinel" / "SKILL.md").read_text()
SOP = (ROOT / "sops" / "bounty-digest" / "SOP.md").read_text()


class ContractTests(unittest.TestCase):
    def test_only_allowlisted_https_hosts_are_in_skill(self):
        hosts = set(re.findall(r"https://([^/`\s]+)", SKILL))
        self.assertEqual(hosts, {"api.github.com", "api.devnet.solana.com"})

    def test_skill_declares_no_custody_boundary(self):
        for phrase in ("T0 read-only", "Never call shell", "Never request or reveal a seed phrase"):
            self.assertIn(phrase, SKILL)

    def test_sop_narrows_every_step_to_http(self):
        self.assertEqual(SOP.count("- allow-tools: http_request"), 2)
        self.assertNotIn("shell", SOP.lower())

    def test_public_solana_address_is_stable(self):
        self.assertIn("Edk1vBTRxCeqxYmytWJcBYCxBxHsh4jXFNrVChdyLxc", SKILL)
        self.assertIn("2.3 Devnet SOL", SKILL)


if __name__ == "__main__":
    unittest.main()
