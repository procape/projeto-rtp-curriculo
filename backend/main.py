import os
from server import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv("BACKEND_PORT", 5000))
    debug = os.getenv("DEBUG", "False") == "True"
    app.run(host='0.0.0.0', port=port, debug=debug)
