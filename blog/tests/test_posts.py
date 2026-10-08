import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from blog.models import Category, Like, Post,Comment

from blog.models import Category


@pytest.mark.django_db
def test_create_post():
    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "My First API Post",
        "slug": "my-first-api-post",
        "content": "This post was created using an automated test.",
        "category_id": category.id,
    }

    response = client.post("/posts/", data)

    assert response.status_code == 201, response.data

    post = Post.objects.get(slug="my-first-api-post")

    assert post.title == "My First API Post"
    assert post.author == user
    assert post.category == category



@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_post():
    client = APIClient()

    data = {
        "title": "Unauthorized Post",
        "slug": "unauthorized-post",
        "content": "This should not be created.",
    }

    response = client.post("/posts/", data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_user_cannot_edit_another_users_post():
    user_a = User.objects.create_user(
        username="user_a",
        password="password123"
    )

    user_b = User.objects.create_user(
        username="user_b",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user_a,
        title="Original Post",
        slug="original-post",
        content="Original content",
        category=category
    )

    client = APIClient()

    # Authenticate as User B
    client.force_authenticate(user=user_b)

    data = {
        "title": "Hacked Post",
        "slug": "original-post",
        "content": "User B changed this post.",
        "category_id": category.id,
    }

    response = client.put(
        f"/posts/{post.id}/",
        data
    )

    assert response.status_code == 403
@pytest.mark.django_db
def test_author_can_edit_own_post():
    user = User.objects.create_user(
        username="author",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Original Post",
        slug="original-post",
        content="Original content",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Updated Post",
        "slug": "updated-post",
        "content": "Updated content",
        "category_id": category.id,
    }

    response = client.put(
        f"/posts/{post.id}/",
        data
    )

    assert response.status_code == 200

    post.refresh_from_db()

    assert post.title == "Updated Post"
    assert post.content == "Updated content"
@pytest.mark.django_db
def test_user_cannot_delete_another_users_post():
    user_a = User.objects.create_user(
        username="user_a",
        password="password123"
    )

    user_b = User.objects.create_user(
        username="user_b",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user_a,
        title="Original Post",
        slug="original-post",
        content="Original content",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user_b)

    response = client.delete(
        f"/posts/{post.id}/"
    )

    assert response.status_code == 403

    assert Post.objects.filter(id=post.id).exists()
@pytest.mark.django_db
def test_author_can_delete_own_post():
    user = User.objects.create_user(
        username="author",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post To Delete",
        slug="post-to-delete",
        content="This post will be deleted.",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(
        f"/posts/{post.id}/"
    )

    assert response.status_code == 204

    assert not Post.objects.filter(id=post.id).exists()
@pytest.mark.django_db
def test_post_title_must_be_at_least_5_characters():
    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Hi",
        "slug": "short-title",
        "content": "This post has enough content.",
        "category_id": category.id,
    }

    response = client.post("/posts/", data)

    assert response.status_code == 400
    assert "title" in response.data

@pytest.mark.django_db
def test_published_post_requires_content():
    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Published Post",
        "slug": "published-post",
        "content": "",
        "published": True,
        "category_id": category.id,
    }

    response = client.post("/posts/", data)

    assert response.status_code == 400
    assert "content" in response.data
@pytest.mark.django_db
def test_post_response_contains_nested_author_and_category():
    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "title": "Nested Serializer Test",
        "slug": "nested-serializer-test",
        "content": "Testing nested serializer responses.",
        "category_id": category.id,
    }

    response = client.post("/posts/", data)

    assert response.status_code == 201

    # Check the nested author
    assert response.data["author"]["username"] == "testuser"

    # Check the nested category
    assert response.data["category"]["name"] == "Technology"
    assert response.data["category"]["slug"] == "technology"
@pytest.mark.django_db
def test_post_response_contains_comments():
    user = User.objects.create_user(
        username="testuser",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post With Comment",
        slug="post-with-comment",
        content="This post has a comment.",
        category=category
    )

    Comment.objects.create(
        post=post,
        author=user,
        body="This is a test comment."
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f"/posts/{post.id}/")

    assert response.status_code == 200

    assert len(response.data["comments"]) == 1
    assert response.data["comments"][0]["body"] == "This is a test comment."
@pytest.mark.django_db
def test_authenticated_user_can_create_comment():
    user = User.objects.create_user(
        username="commenter",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "post": post.id,
        "body": "This is my first API comment."
    }

    response = client.post("/comments/", data)

    assert response.status_code == 201

    comment = Comment.objects.get(
        body="This is my first API comment."
    )

    assert comment.post == post
    assert comment.author == user
@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_comment():
    user = User.objects.create_user(
        username="comment_author",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    client = APIClient()

    data = {
        "post": post.id,
        "body": "This is an anonymous comment."
    }

    response = client.post("/comments/", data)

    assert response.status_code == 403

    assert not Comment.objects.filter(
        body="This is an anonymous comment."
    ).exists()
@pytest.mark.django_db
def test_user_cannot_edit_another_users_comment():
    user1 = User.objects.create_user(
        username="comment_author",
        password="password123"
    )

    user2 = User.objects.create_user(
        username="other_user",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user1,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    comment = Comment.objects.create(
        post=post,
        author=user1,
        body="Original comment"
    )

    client = APIClient()
    client.force_authenticate(user=user2)

    data = {
        "post": post.id,
        "body": "I changed this comment."
    }

    response = client.put(
        f"/comments/{comment.id}/",
        data
    )

    assert response.status_code == 403

    comment.refresh_from_db()

    assert comment.body == "Original comment"
@pytest.mark.django_db
def test_comment_author_can_edit_own_comment():
    user = User.objects.create_user(
        username="comment_author",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    comment = Comment.objects.create(
        post=post,
        author=user,
        body="Original comment"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "post": post.id,
        "body": "Updated comment"
    }

    response = client.put(
        f"/comments/{comment.id}/",
        data
    )

    assert response.status_code == 200

    comment.refresh_from_db()

    assert comment.body == "Updated comment"
    assert comment.author == user

@pytest.mark.django_db
def test_user_cannot_delete_another_users_comment():
    user1 = User.objects.create_user(
        username="comment_author",
        password="password123"
    )

    user2 = User.objects.create_user(
        username="other_user",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user1,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    comment = Comment.objects.create(
        post=post,
        author=user1,
        body="Original comment"
    )

    client = APIClient()
    client.force_authenticate(user=user2)

    response = client.delete(
        f"/comments/{comment.id}/"
    )

    assert response.status_code == 403

    assert Comment.objects.filter(
        id=comment.id
    ).exists()
@pytest.mark.django_db
def test_comment_author_can_delete_own_comment():
    user = User.objects.create_user(
        username="comment_author",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    comment = Comment.objects.create(
        post=post,
        author=user,
        body="Comment to delete"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete(
        f"/comments/{comment.id}/"
    )

    assert response.status_code == 204

    assert not Comment.objects.filter(
        id=comment.id
    ).exists()
@pytest.mark.django_db
def test_comment_body_must_be_at_least_3_characters():
    user = User.objects.create_user(
        username="commenter",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post For Comment",
        slug="post-for-comment",
        content="This post will receive a comment.",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "post": post.id,
        "body": "Hi"
    }

    response = client.post("/comments/", data)

    assert response.status_code == 400

    assert "body" in response.data

    assert not Comment.objects.filter(
        body="Hi"
    ).exists()

@pytest.mark.django_db
def test_authenticated_user_can_like_post():
    user = User.objects.create_user(
        username="liker",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post To Like",
        slug="post-to-like",
        content="This post will be liked.",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "post": post.id
    }

    response = client.post("/likes/", data)
    

    assert response.status_code == 201, response.data

    assert Like.objects.filter(
        post=post,
        user=user
    ).exists()
@pytest.mark.django_db
def test_unauthenticated_user_cannot_like_post():
    user = User.objects.create_user(
        username="postauthor",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post To Like",
        slug="post-to-like",
        content="This post will be liked.",
        category=category
    )

    client = APIClient()

    data = {
        "post": post.id
    }

    response = client.post("/likes/", data)

    assert response.status_code in [401, 403]

    assert not Like.objects.filter(
        post=post
    ).exists()

@pytest.mark.django_db
def test_user_cannot_like_same_post_twice():
    user = User.objects.create_user(
        username="liker",
        password="password123"
    )

    category = Category.objects.create(
        name="Technology",
        slug="technology"
    )

    post = Post.objects.create(
        author=user,
        title="Post To Like",
        slug="post-to-like",
        content="This post will be liked.",
        category=category
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
        "post": post.id
    }

    # First like
    first_response = client.post("/likes/", data)

    assert first_response.status_code == 201

    # Second like
    second_response = client.post("/likes/", data)

    assert second_response.status_code in [400, 409]

    # Make sure only one Like exists
    assert Like.objects.filter(
        post=post,
        user=user
    ).count() == 1