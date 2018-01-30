from flask import Flask, render_template, request, escape
from search_for_letters import search4letters

app = Flask(__name__)


@app.route('/search4', methods=['POST'])
def do_search()->str:
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_tittle='Here are your results',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to search4letters on the web!')


@app.route('/viewlog')
def view_the_log() -> str:

    contents = []

    with open('vsearch.log') as log:
        for line in log:
            contents.append([])
            for item in line.split('|'):
                contents[-1].append(escape(item))

    titles = ('Form data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=contents)


def log_request(req: 'flask_request', res: str) -> None:

    with open('vsearch.log', 'a') as log_file:

        print(req.form, req.remote_addr, req.user_agent, res, sep='|', file=log_file)

# app.run(host='0.0.0.0')
if __name__ == '__main__':
    app.run(debug=True)