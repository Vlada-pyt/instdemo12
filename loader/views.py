from json import JSONDecodeError

import logging

from flask import Flask, render_template, request, Blueprint

from loader.utils import save_picture
from functions import add_posts

loader_blueprint = Blueprint("loader_blueprint", __name__, template_folder="templates")


@loader_blueprint.route("/post")
def post_page():
    return render_template("post_form.html")


@loader_blueprint.route("/post", methods=["POST"])
def add_post():
    picture = request.files.get("picture")
    content = request.form.get("content")

    if not content or not picture:
        return "Нет файла или картинки"

    if picture.filename.split(".")[-1] not in["jpeg", "png"]:
        logging.info("Загруженный файл не картинка")
        return "Неверное расширение файла"
    try:
        picture_path = "/" + save_picture(picture)
    except FileNotFoundError:
        logging.error("Файл не найден")
        return "Файл не найден"
    except JSONDecodeError:
        return "Невалидный файл"
    post = add_posts({"pic": picture_path, "content": content})
    return render_template("post_uploaded.html", post=post)
