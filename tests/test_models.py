import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Repository

class TestRepositoryModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up an in-memory database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        # Create a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback changes after each test
        self.session.rollback()
        self.session.close()

    def test_create_repository(self):
        # Create a new repository instance
        new_repo = Repository(
            full_name="openai/gpt-3",
            description="GPT-3: Language Models are Few-Shot Learners",
            clone_url="https://github.com/openai/gpt-3.git",
            stars=15424,
            created_at="2020-05-18T08:03:50Z"
        )
        self.session.add(new_repo)
        self.session.commit()

        # Retrieve the repository from the database
        retrieved_repo = self.session.query(Repository).filter_by(full_name="openai/gpt-3").first()
        self.assertIsNotNone(retrieved_repo)
        self.assertEqual(retrieved_repo.full_name, "openai/gpt-3")
        self.assertEqual(retrieved_repo.description, "GPT-3: Language Models are Few-Shot Learners")
        self.assertEqual(retrieved_repo.clone_url, "https://github.com/openai/gpt-3.git")
        self.assertEqual(retrieved_repo.stars, "15424")

if __name__ == '__main__':
    unittest.main()