import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from main import app

class TestRepositoryEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('httpx.Client.get')
    def test_get_repository(self, mock_get):
        mock_response = {
            "full_name": "openai/gpt-3",
            "description": "GPT-3: Language Models are Few-Shot Learners",
            "clone_url": "https://github.com/openai/gpt-3.git",
            "stars": "15424",
            "created_at": "2020-05-18T08:03:50Z"
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response

        response = self.client.get("/repositories/openai/gpt-3")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), mock_response)
    
    @patch('httpx.Client.get')
    def test_get_repository_not_found(self, mock_get):
        # Configure the mock to simulate a 'not found' error from GitHub
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"detail": "Repository not found"}

        response = self.client.get("/repositories/openai/nonexistent-repo")
        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"], "Repository not found")
    
    @patch('main.get_repository_from_db')
    def test_get_repository_from_cache(self, mock_db):
        mock_db_response = {
            "full_name": "openai/gpt-3",
            "description": "Cached Description",
            "clone_url": "https://github.com/openai/gpt-3.git",
            "stars": "15000",
            "created_at": "2020-05-18T08:03:50Z"
        }
        mock_db.return_value = mock_db_response

        response = self.client.get("/repositories/openai/gpt-3")
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), mock_db_response)

if __name__ == '__main__':
    unittest.main()
