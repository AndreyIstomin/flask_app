from flask import Flask, render_template, request, escape
from search_for_letters import search4letters
from DBcm import UseDatabase

app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'flask_app',
                          'password': '123456',
                          'database': 'vsearchlogDB',}


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

    with UseDatabase(app.config['dbconfig']) as cursor:

        _SQL = """select phrase, letters, ip, browser_string, results from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()

    titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html',
                           the_title='View log',
                           the_row_titles=titles,
                           the_data=contents,)


def log_request(req: 'flask_request', res: str) -> None:

    with UseDatabase(app.config['dbconfig']) as cursor:

        _SQL = """insert into log
                (phrase, letters, ip, browser_string, results)
                values
                (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res, ))

# deprecated
# def log_request_to_file(req: 'flask_request', res: str) -> None:
#
#     with open('vsearch.log', 'a') as log_file:
#
#         print(req.form, req.remote_addr, req.user_agent, res, sep='|', file=log_file)
#
#
# @app.route('/viewlog_file')
# def view_the_log_from_file() -> str:
#
#     contents = []
#
#     with open('vsearch.log') as log:
#         for line in log:
#             contents.append([])
#             for item in line.split('|'):
#                 contents[-1].append(escape(item))
#
#     titles = ('Form data', 'Remote_addr', 'User_agent', 'Results')
#     return render_template('viewlog.html',
#                            the_title='View log',
#                            the_row_titles=titles,
#                            the_data=contents)

# app.run(host='0.0.0.0')
if __name__ == '__main__':
    app.run(debug=True)