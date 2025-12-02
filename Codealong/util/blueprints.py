import routes

def register_blueprint(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.orgs)
    app.register_blueprint(routes.search)
    app.register_blueprint(routes.users)