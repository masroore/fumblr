# Copyright 2023 Dr. Masroor Ehsan

import os
import random
import string

import furl
import requests
from werkzeug.utils import secure_filename

from ..default_settings import UPLOAD_FOLDER


def _result(path: str) -> dict:
    path = path.replace("\\", "/")
    data = dict(
        id="".join(random.choices(string.ascii_lowercase + string.digits, k=8)),
        deletehash="".join(
            random.choices(string.ascii_lowercase + string.digits, k=16)
        ),
        link=f"/{path}",
    )
    return data


def upload(file) -> dict:
    filename = secure_filename(file.filename)
    link = os.path.join(UPLOAD_FOLDER, filename)
    file.save(os.path.abspath(link))

    return _result(link)


def upload_from_url(url: str) -> dict:
    resp = requests.get(url)
    fname = os.path.basename(str(furl.furl(url).path))
    filename = secure_filename(fname)
    link = os.path.join(UPLOAD_FOLDER, filename)
    with open(filename, "wb") as fp:
        fp.write(resp.content)

    return _result(link)
