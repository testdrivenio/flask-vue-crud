# Developing a Single Page App with Flask and Vue.js

### Want to learn how to build this?

Check out the [tutorial](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs).

## Want to use this project?

1. Fork/Clone

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ flask run --port=5001 --debug
    ```

    Navigate to [http://localhost:5001](http://localhost:5001)

1. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
    ```

    Navigate to [http://localhost:5173](http://localhost:5173)
