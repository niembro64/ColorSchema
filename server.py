# Eric's Version

from flask_app import app
from flask_app.controllers import user_controller
from flask_app.controllers import schema_controller




if __name__ == "__main__":
    app.run(debug=True)
#    app.run(debug=True, port=5000)

# redbelted