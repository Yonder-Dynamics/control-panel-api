import connexion

def ping():
    return "PONG!"

app = connexion.FlaskApp(__name__, specification_dir='/api/')
app.add_api("swagger.yaml")
app.run(port=8080)