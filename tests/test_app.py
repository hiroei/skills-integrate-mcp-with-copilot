import importlib.util
import unittest
from pathlib import Path
from fastapi.testclient import TestClient


module_path = Path(__file__).resolve().parents[1] / 'src' / 'app.py'
spec = importlib.util.spec_from_file_location('school_app', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ActivityApiTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(module.app)

    def test_github_skills_activity_exists(self):
        response = self.client.get('/activities')
        self.assertEqual(response.status_code, 200)
        self.assertIn('GitHub Skills', response.json())

    def test_github_skills_signup_allows_enrollment(self):
        response = self.client.post('/activities/GitHub Skills/signup?email=student@mergington.edu')
        self.assertEqual(response.status_code, 200)
        self.assertIn('student@mergington.edu', module.activities['GitHub Skills']['participants'])


if __name__ == '__main__':
    unittest.main()
