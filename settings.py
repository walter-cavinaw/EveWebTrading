import os.path
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("mysql_host", default="localhost:3306", help="eve database host")
define("mysql_database", default="eve", help="database/schema name: eve")
define("mysql_user", default="eve_server", help="eve server login id")
define("mysql_password", default="evetrading2014", help="eve server password")

PRODUCTION = "PRODUCTION"
DEV = "DEV"
STAGING = "STAGING"

if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
else:
    DEPLOYMENT = DEV

if DEPLOYMENT == PRODUCTION:
    options.mysql_host = os.environ['CLEARDB_DATABASE_URL']
    options.mysql_user = os.environ['CLEARDB_USER']
    options.mysql_password = os.environ['CLEARDB_PWD']
    options.mysql_database = os.environ['CLEARDB_DB']


settings = dict()
settings['cookie_secret'] = "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"
settings['login_url'] = "auth/login"
settings['template_path'] = os.path.join(os.path.dirname(__file__), "templates")
settings['static_path'] = os.path.join(os.path.dirname(__file__), "static")

