from apps import *
from decouple import config
from apps.config import config_dict

DEBUG = config('DEBUG', default=False, cast=bool)
get_config_mode = 'Debug' if DEBUG else 'Production'
app_config = config_dict[get_config_mode.capitalize()]
app = create_app(app_config)

if __name__ == "__main__":
    app.run(debug=True)