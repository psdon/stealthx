# -*- coding: utf-8 -*-
"""Create an application instance."""
from stealthx.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, True)