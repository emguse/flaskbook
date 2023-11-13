import os
import shutil

import pytest

from apps.app import create_app, db
from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


@pytest.fixture
def app_data():
    return 3


@pytest.fixture
def fixture_app():
    # setup
    app = create_app("testing")
    app.secret_key = "nvcGG56FLS3CzkRVh0d5oVIWDF7e6MNF"

    # define useing databese
    app.app_context().push()

    # create the test database table
    with app.app_context():
        db.create_all()

    # create the test image upload directory
    os.mkdir(app.config["UPLOAD_FOLDER"])

    yield app

    # cleanup
    # delete user table
    User.query.delete()
    # delete userimage record
    UserImage.query.delete()
    # delete the user image tags record
    UserImageTag.query.delete()
    # delete the test image upload directory
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


# fixture function for Flask test client
@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
