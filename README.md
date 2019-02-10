## The Bias Portfolio ##

This app is a web-based dashboard which analyses the input and output of an algorithm to identify where undesirable biases are present.
Often, protected classes (such as gender) are encoded in a set of unprotected variables, therefore a naive algorithm is able to discriminate against (e.g.) gender without using access to the protected class in the first place.

Simple 'fairness' methods do not identify these relationships and are therefore unable to address key issues in the measurement methodology. This multivariate analysis highlights variables which are highly correlated with protected classes.

#### Resources ####
https://dash.plot.ly/

#### Installation ####
Clone the project and navigate to the folder.
`git clone https://github.com/rosscg/ai-recruitment-bias`
`cd ai-recruitment-bias`

Create and activate virtual environment (Mac).
`python3 -m venv venv`
`source venv/bin/activate`

Create and activate virtual environment (Windows Anaconda).
`conda update conda`
`conda create -n venv python=3.6 anaconda`
`source activate venv`

Install dependencies with the command:
`pip install -r requirements.txt `

Run the app with the command:
`python app.py`

Visit [http:127.0.0.1:8050/](http:127.0.0.1:8050/) in your web browser

#### Viewing Notebook ####
Run:
`jupyter notebook analysis/notebook.ipynb`
