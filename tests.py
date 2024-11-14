import os

os.environ['DATABASE_URI'] = 'sqlite:///'

from datetime import datetime, timezone, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        user = User(username="Mohan", email="mohan@blog.in")
        user.set_password("Mohan@123")
        self.assertFalse(user.check_password('dog'))
        self.assertTrue(user.check_password('Mohan@123'))

    def test_avatar(self):
        user = User(username="Neema", email="neema@blog.in")
        self.assertEqual(user.avatar(128), "https://www.gravatar.com/avatar/8c360c32f9cf6a051b3456872e425f69?d=wavatar&size=128")

    def test_follow(self):
        user1 = User(username="Bolt", email="bolt@blog.in")
        user2 = User(username="Doug", email="doug@blog.in")
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        following = db.session.scalars(user1.following.select()).all()
        followers = db.session.scalars(user2.followers.select()).all()

        self.assertEqual(following, [])
        self.assertEqual(followers, [])

        user1.follow(user2)
        db.session.commit()
        self.assertTrue(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 1)
        self.assertEqual(user2.followers_count(), 1)

        user1_following = db.session.scalars(user1.following.select()).all()
        user2_followers = db.session.scalars(user2.followers.select()).all()
        self.assertEqual(user1_following[0].username, 'Doug')
        self.assertEqual(user2_followers[0].username, 'Bolt')

        user1.unfollow(user2)
        db.session.commit()
        self.assertFalse(user1.is_following(user2))
        self.assertEqual(user1.following_count(), 0)
        self.assertEqual(user2.followers_count(), 0)

    def test_follow_posts(self):
        # Create 4 users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # Create 4 posts
        now = datetime.now(timezone.utc)
        p1 = Post(body="post from john", author=u1, timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2, timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Follower setup
        u1.follow(u2) # John follows Susan
        u1.follow(u4) # John follows David
        u2.follow(u3) # Susan follows Mary
        u3.follow(u4) # Mary follows David
        db.session.commit()

        # Check the following posts of each user
        f1 = db.session.scalars(u1.following_posts()).all()
        f2 = db.session.scalars(u2.following_posts()).all()
        f3 = db.session.scalars(u3.following_posts()).all()
        f4 = db.session.scalars(u4.following_posts()).all()

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == "__main__":
    unittest.main(verbosity=2)