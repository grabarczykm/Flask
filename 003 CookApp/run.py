from app import app, db
from app.models import User, Receipe

#Flask shell
@app.shell_context_processor
def make_shell_context():
    return{'db':db,'User':User,'Receipe':Receipe}#wartości preimportowane do Flask Shell

if __name__ == '__main__':
    app.run(debug=True)