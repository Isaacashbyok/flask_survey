from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY']='thisisasecretkey'
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    return render_template('home.html', survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route('/answer', methods=['POST'])
def handle_question():
    
    choice = request.form['answer']
    
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if (len(responses) == len(survey.questions)) : 
        return redirect('/completed')
    else : 
        return redirect(f'/questions/{len(responses)}')
    

@app.route('/questions/<int:id>')
def show_question(id) : 
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None) : 
        return redirect('/')
    
    if (len(responses) == len(survey.questions)) : 
        
        return redirect('/completed')
    
    if (len(responses) != id) : 
        
        flash(f'Invalid question id: {id}')
        return redirect(f'/questions/{len(responses)}')
    
    question = survey.questions[id]
    return render_template('questions.html', question=question, question_num=id)

@app.route('/completed')
def completed() : 
    
    return render_template('completed.html')