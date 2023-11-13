from pathlib import Path

from flask.helpers import get_root_path
from werkzeug.datastructures import FileStorage

from apps.detector.models import UserImage


# Not logged in
def test_index(client):
    rv = client.get("/")
    assert "Login" in rv.data.decode()
    assert "Upload new image" in rv.data.decode()


# logged in
def signup(client, username, email, password):
    """sign up."""
    data = dict(username=username, email=email, password=password)
    return client.post("/auth/signup", data=data, follow_redirects=True)


def test_index_signup(client):
    """exec. sign up"""
    rv = signup(client, "admin", "flaskbook@example.com", "testpassword")
    print(rv)
    assert "admin" in rv.data.decode()

    rv = client.get("/")
    assert "Logout" in rv.data.decode()
    assert "Upload new image" in rv.data.decode()


def test_upload_no_auth(client):
    """Image upload screen test when not logged in"""
    rv = client.get("/upload", follow_redirects=True)
    assert "Upload" not in rv.data.decode()
    assert "Email address" in rv.data.decode()
    assert "Password" in rv.data.decode()


def test_upload_signup_get(client):
    """Image upload screen test at login"""
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    rv = client.get()
    assert "Upload" in rv.data.decode()


def upload_image(client, image_path):
    """Upload image"""
    image = Path(get_root_path("tests"), image_path)

    test_file = (
        FileStorage(
            stream=open(image, "rb"),
            filename=Path(image_path).name,
            content_type="multipart/from-data",
        ),
    )

    data = dict(
        image=test_file,
    )

    return client.post("/upload", data=data, follow_redirects=True)


def test_upload_signup_post_validate(client):
    """Image upload successful test"""
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    rv = upload_image(client, "detector/testdata/test_invalid_file.txt")
    assert "Unsupported image format." in rv.data.decode()


def test_upload_signup_post(client):
    """Image upload successful test"""
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    rv = upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()


def tets_detect_no_user_image(client):
    """Validation error test after pressing the detection button"""
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    # specifying a non-existent ID
    rv = client.post("/detect/notexistid", follow_redirects=True)
    assert "Target image does not exist." in rv.data.decode()


def test_detect(client):
    """Object detection success test"""
    # signup
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    # Upload image
    upload_image(client, "detector/testdata/test_valid_image.jpg")
    user_image = UserImage.query.first()

    # detect execute
    rv = client.post(f"/detect/{user_image.id}", follow_redirects=True)
    user_image = UserImage.query.first()
    assert user_image.image_path in rv.data.decode()
    assert "cat" in rv.data.decode()


def test_delete(client):
    """Image deletion test"""
    signup(client, "admin", "flaskbook@example.com", "testpassword")
    upload_image(client, "detector/testdata/test_valid_image.jpg")

    user_image = UserImage.query.first()
    image_path = user_image.image_path
    rv = client.post(f"/images/delete/{user_image.id}", follow_redirects=True)
    assert image_path not in rv.data.decode()


def test_custom_error(client):
    """custom error test"""
    rv = client.get("/notfound")
    assert "404 Not Found" in rv.data.decode()
