import os

from test_project import create_app


app = create_app()


def local_server():
    os.system("flask run -p 5555 --reload")


def local_db_down():
    os.system("docker-compose -f docker-compose.yml down")


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
