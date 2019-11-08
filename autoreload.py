from livereload import Server

from autoapp import app

server = Server(app)
server.watch("./stealthx/templates/", "make static")
server.watch("./assets/")
server.serve(port=8080, host="0.0.0.0")
