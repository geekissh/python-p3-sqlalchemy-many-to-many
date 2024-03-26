from sqlalchemy import create_engine, func, ForeignKey, Table, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define association table for many-to-many relationship between User and Game
game_user = Table(
    'game_users',
    Base.metadata,
    Column('game_id', ForeignKey('games.id'), primary_key=True),
    Column('user_id', ForeignKey('users.id'), primary_key=True)
)

class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    platform = Column(String)
    price = Column(Integer)

    # Establish many-to-many relationship with User
    users = relationship("User", secondary=game_user, back_populates="games")

    def __repr__(self):
        return f"Game(id={self.id}, title='{self.title}', platform='{self.platform}')"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Establish one-to-many relationship with Review
    reviews = relationship("Review", back_populates="user")

    # Establish many-to-many relationship with Game
    games = relationship("Game", secondary=game_user, back_populates="users")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}')"

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    # Establish many-to-one relationship with Game
    game = relationship("Game", back_populates="reviews")

    # Establish many-to-one relationship with User
    user = relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id}, score={self.score}, game_id={self.game_id})"
