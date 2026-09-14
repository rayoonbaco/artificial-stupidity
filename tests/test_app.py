import unittest

try:
    import app as web_app
except ModuleNotFoundError as exc:
    if exc.name != "flask":
        raise
    web_app = None


@unittest.skipIf(web_app is None, "Flask is not installed in this bare CPU environment")
class WebApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = web_app.app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    def test_published_scenarios_reach_all_three_actions(self):
        actions = {}
        for scenario in ("keep", "reject", "escalate"):
            response = self.client.post("/api/evaluate", json={"scenario": scenario})
            self.assertEqual(response.status_code, 200)
            actions[scenario] = response.get_json()["action"]
        self.assertEqual(actions, {"keep": "KEEP", "reject": "REJECT", "escalate": "ESCALATE"})

    def test_arbitrary_candidate_submission_is_rejected(self):
        response = self.client.post(
            "/api/evaluate",
            json={"candidate": {"human_authorization": "KEEP"}},
        )
        self.assertEqual(response.status_code, 400)

    def test_security_headers(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])

    def test_second_domain_result_and_limit_are_public(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for action in ("KEEP", "REJECT", "ESCALATE"):
            self.assertIn(action, page)
        self.assertIn("SECOND-DOMAIN VALIDATION", page)
        self.assertIn("not legal advice", page)
        self.assertIn("independent reproduction", page)


if __name__ == "__main__":
    unittest.main()
