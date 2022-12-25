import os

from app import create_app


def run_app():
    return create_app()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True,
            threaded=True,
            host=os.getenv('SERVER_HOST'),
            port=os.getenv('SERVER_PORT')
    )

