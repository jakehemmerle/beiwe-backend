import jinja2, traceback
from flask import Flask, render_template, redirect, abort
from pages import admin_pages, mobile_pages, survey_designer, system_admin_pages
from api import mobile_api, survey_api, admin_api, data_access_api
from libs.admin_authentication import is_logged_in
from libs.logging import log_error
from libs.security import set_secret_key


def subdomain(directory):
    app = Flask(__name__, static_folder=directory + "/static")
    set_secret_key(app)
    loader = [app.jinja_loader, jinja2.FileSystemLoader(directory + "/templates")]
    app.jinja_loader = jinja2.ChoiceLoader(loader)
    return app


# Register pages here
app = subdomain("frontend")
app.register_blueprint(mobile_api.mobile_api)
app.register_blueprint(admin_pages.admin_pages)
app.register_blueprint(mobile_pages.mobile_pages)
app.register_blueprint(system_admin_pages.system_admin_pages)
app.register_blueprint(survey_designer.survey_designer)
app.register_blueprint(admin_api.admin_api)
app.register_blueprint(survey_api.survey_api)
app.register_blueprint(data_access_api.data_access_api)

@app.route("/<page>.html")
def strip_dot_html(page):
    #strips away the dot html from pages
    return redirect("/%s" % page)


# Points our custom 404 page (in /frontend/templates) to display on a 404 error.
# (note, function name is irrelevant, it is the
@app.errorhandler(404)
def e404(e):
    return render_template("404.html",is_logged_in=is_logged_in())


# Defines additional behavior for HTML 500 errors, in this case logs a stacktrace.
@app.errorhandler(500)
def e500_text(e):
    try:
        stacktrace = traceback.format_exc()
        print(stacktrace)
    except Exception as e:
        log_error(e)
    return abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
