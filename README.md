# Codachrome

Give us midi and we give you midi back! Never play alone

## Setup for local development

  1. First make sure you have Python 3 installed by running `python --version` in your terminal. If it doesn't show `3.0` or higher, then install Python 3 with these instructions: https://docs.python-guide.org/starting/installation/

  1. Clone this repo! See: https://help.github.com/articles/cloning-a-repository/

  1. In your terminal, go into the newly-created folder for this repo with `cd codachrome`.

   > To verify that you're in the correct folder, you can use the command `pwd` (print working directory)
  
  1. Create a virtual environment with this command: `python3 -m venv venv` on Mac, or `py -3 -m venv venv` on Windows.

   > Note: This lets you use different versions of Python and Python modules for each of your Python projects separately, so they don't conflict with each other.

  1. Activate the virtual environment by running this terminal command while you're inside the `codachrome` folder: `source venv/bin/activate` on Mac, or `venv\Scripts\activate` on Windows. You'll know it worked if you now see `(venv)` appear before your shell prompt.

   > To exit out of the current virtual environment when you're switching between projects, just run `deactivate`.

  1. Install the project dependencies by running this terminal command: `pip install -r requirements.txt`

  1. Finally, to start a local server and run the Codachrome app, run `flask run` in terminal.

  1. You'll see something like `Running on http://127.0.0.1:5000/` appear in your terminal. Navigate to that URL in your web browser to see the app!
  
  > Or you can use the URL `localhost:5000` as a shortcut.


