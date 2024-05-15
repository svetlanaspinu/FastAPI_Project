# this file holds the testcase when it comes creating, riding, updating and deleting posts.
# in video e la 16h 50'
import pytest



def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200 

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


# retrieve a valid post
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id # e post.Post deaorece in schema la BaseModel Post: Post

# creating a Post test.
@pytest.mark.parametrize("title, content, publised", [
    ("this is a title for testing purpose", "the content is for testing case", True),
    ("this is a title for testing purpose nr 2", "the content is for testing case nr 2", False),
    ("this is a title for testing purpose nr 3", "the content is for testing case nr 3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    assert res.status_code == 201

# to test if we are not logged-in 
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "this is the title", "content": "this is the content"}
    )
    assert res.status_code == 401


# test an unauthorized user trying to delete a post
def test_unautohorized_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# test a valid deletion
def test_delete_post_success(authorized_client, test_user, test_posts):
     res = authorized_client.delete(f"/posts/{test_posts[0].id}")
     assert res.status_code == 204

# deleting a non existing posts - that dosent exist in the database
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
     res = authorized_client.delete(f"/posts/800800")
     assert res.status_code == 404

# test update post
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title":"update title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    update_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update_post.title == data['title']
    assert update_post.content == data['content']


def test_unautohorized_update_Post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    