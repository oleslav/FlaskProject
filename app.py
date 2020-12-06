from config import *

from controllers.note_controller import *
from controllers.user_controller import *
db.create_all()

@app.route('/')
def index():
    return 'Hello world'


if __name__ == '__main__':
    app.run()
