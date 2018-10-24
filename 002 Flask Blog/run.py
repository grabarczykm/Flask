from app2 import create_app #app2 to nazwa folderu, import zachodzi z pliku __init__

app = create_app()

if __name__ == '__main__':
    app.run(debug = True)