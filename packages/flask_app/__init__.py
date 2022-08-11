import os
import sys


from flask import Flask, render_template
from packages.stats_collector.stats_provider import StatsProvider

# from stats_collector.stats_provider import StatsProvider, MatchStats


def create_app(match_data_folder_path, test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    app.config["MATCH_DATA_FOLDER_PATH"] = match_data_folder_path
    app.stats_provider: StatsProvider = StatsProvider(match_data_folder_path)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def index():
        match_ids = app.stats_provider.get_match_ids()
        ctx = {}
        ctx.update({"match_ids": match_ids})
        return render_template("index.html", **ctx)

    @app.route("/match/<match_id>")
    def match(match_id):
        match_data = app.stats_provider.get_match_by_id(match_id)
        own_team = match_data.get_self_team()
        other_teams = match_data.get_other_teams()
        print(other_teams)
        ctx = {"own_team": own_team, "other_teams": other_teams}
        return render_template("match.html", **ctx)

    return app


if __name__ == "__main__":
    MATCHES_DATA_PATH = "..\\data\\matches\\"
    app = create_app(MATCHES_DATA_PATH, test_config=None)
    app.run(host="127.0.0.1", port=8000, debug=True)
