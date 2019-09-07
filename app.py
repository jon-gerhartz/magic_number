from flask import Flask, render_template
from run import runner


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret-ass-key"


@app.route('/', methods =['GET'])
def index():
	return render_template('index.html')


@app.route('/magic', methods =['GET'])
def magic():
	data = runner()
	return render_template('magic.html', tables=data)#[data.to_html(index=False, bold_rows=True)])


@app.route('/playoffs', methods =['GET'])
def playoffs():
	return render_template('playoffs.html')

if __name__ == "__main__":
    app.run(debug=True)