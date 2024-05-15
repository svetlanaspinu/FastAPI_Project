# this file containes the testcase for votes file
# 17h 25'
import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

# tests a vote tah have been already liked by the same user
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    res = authorized_client.posts("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


# test for deleting a vote
def test_delete_vote(client, test_posts, test_vote):
    res = authorized_client.posts("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

# testing that an user that is unauthenticatdd cant vote
def test_vote_unauthorized_user(authorized_client, test_posts):
    res = client.posts("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401