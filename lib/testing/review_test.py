from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from conftest import SQLITE_URL  # Assuming SQLITE_URL is defined in conftest.py
from models import Base, Game, Review  # Import your models and Base from models.py

class TestReview:
    @classmethod
    def setup_class(cls):
        # Create the engine
        cls.engine = create_engine(SQLITE_URL)
        # Create all tables in the database
        Base.metadata.create_all(cls.engine)
        # Create a session
        cls.Session = sessionmaker(bind=cls.engine)
        # Add test data
        cls.session = cls.Session()
        cls.skyrim = Game(
            title="The Elder Scrolls V: Skyrim",
            platform="PC",
            genre="Adventure",
            price=20
        )
        cls.session.add(cls.skyrim)
        cls.session.commit()
        cls.skyrim_review = Review(
            score=10,
            comment="Wow, what a game",
            game_id=cls.skyrim.id
        )
        cls.session.add(cls.skyrim_review)
        cls.session.commit()

    @classmethod
    def teardown_class(cls):
        # Close the session and remove the tables
        cls.session.close()
        Base.metadata.drop_all(cls.engine)

    def test_game_has_correct_attributes(self):
        assert hasattr(self.skyrim_review, "id")
        assert hasattr(self.skyrim_review, "score")
        assert hasattr(self.skyrim_review, "comment")
        assert hasattr(self.skyrim_review, "game_id")

    def test_knows_about_associated_game(self):
        assert self.skyrim_review.game == self.skyrim
