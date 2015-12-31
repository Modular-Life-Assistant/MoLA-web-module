from flask import Flask, render_template

from core import DataFileManager
from core.settings import SECRET_KEY
from helpers.modules.BaseModule import BaseModule


class Module(BaseModule):
    flask = Flask(__name__)
    app_list = []

    def add_blueprint(self, blueprint, icon='', **options):
        self.flask.register_blueprint(blueprint, **options)
        self.app_list.append({
            'css_class': 'ui-btn-icon-left ui-icon-%s' % icon if icon else '',
            'name': blueprint.name,
            'url': blueprint.url_prefix,
        })

    def init(self):
        # url mapping
        self.flask.add_url_rule('/', 'index', view_func=self._index)
        self.flask.add_url_rule('/home', 'home', view_func=self._home)

        # set vars
        self.flask.secret_key = SECRET_KEY

    def run(self):
        config = DataFileManager.load(self.name, 'config', {
            'host' : '0.0.0.0',
            'debug': False,
        })
        config['threaded'] = True  # for multiple pages simultaneously
        self.flask.run(**config)

    def _home(self):
        return render_template('home.html', apps=self.app_list)

    def _index(self):
        return render_template('index.html', apps=self.app_list,
                               content_url='/home')
