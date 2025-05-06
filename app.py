from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import json
import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.urandom(24)  


if not os.path.exists('static'):
    os.makedirs('static')
if not os.path.exists('static/css'):
    os.makedirs('static/css')
if not os.path.exists('templates'):
    os.makedirs('templates')

QUIZ_DATA = {
    1: {
        'id': 1,
        'title': "General Knowledge Quiz",
        'description': "Test your general knowledge with this quiz covering various topics.",
        'time_limit': 900, 
        'questions': [
            {
                'id': 1,
                'text': "What is the largest planet in our solar system?",
                'options': ["Earth", "Jupiter", "Saturn", "Mars"],
                'correct_answer': 1, 
                'explanation': "Jupiter is the largest planet in our solar system, with a diameter of about 86,881 miles (139,820 km)."
            },
            {
                'id': 2,
                'text': "Which country has the largest population in the world?",
                'options': ["United States", "Russia", "India", "China"],
                'correct_answer': 3,  
                'explanation': "China has the largest population with over 1.4 billion people, followed closely by India."
            },
            {
                'id': 3,
                'text': "Who wrote 'Romeo and Juliet'?",
                'options': ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                'correct_answer': 1, 
                'explanation': "William Shakespeare wrote 'Romeo and Juliet' around 1594-1595."
            },
            {
                'id': 4,
                'text': "What is the chemical symbol for gold?",
                'options': ["Go", "Gl", "Au", "Ag"],
                'correct_answer': 2,  
                'explanation': "The chemical symbol for gold is 'Au', which comes from the Latin word 'aurum'."
            },
            {
                'id': 5,
                'text': "Which of these is not a primary color?",
                'options': ["Red", "Blue", "Green", "Yellow"],
                'correct_answer': 3, 
                'explanation': "In additive color mixing (light), the primary colors are red, green, and blue. In subtractive color mixing (pigments), they are cyan, magenta, and yellow."
            },
            {
                'id': 6,
                'text': "What is the capital of Japan?",
                'options': ["Beijing", "Seoul", "Tokyo", "Bangkok"],
                'correct_answer': 2, 
                'explanation': "Tokyo is the capital and largest city of Japan."
            },
            {
                'id': 7,
                'text': "Which planet is known as the 'Red Planet'?",
                'options': ["Venus", "Mars", "Jupiter", "Mercury"],
                'correct_answer': 1,  
                'explanation': "Mars is known as the 'Red Planet' due to its reddish appearance caused by iron oxide (rust) on its surface."
            },
            {
                'id': 8,
                'text': "What is the largest ocean on Earth?",
                'options': ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
                'correct_answer': 3, 
                'explanation': "The Pacific Ocean is the largest and deepest ocean on Earth, covering about one-third of the Earth's surface."
            },
            {
                'id': 9,
                'text': "Who painted the Mona Lisa?",
                'options': ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"],
                'correct_answer': 2, 
                'explanation': "The Mona Lisa was painted by Leonardo da Vinci between 1503 and 1519."
            },
            {
                'id': 10,
                'text': "Which element has the chemical symbol 'O'?",
                'options': ["Osmium", "Oxygen", "Oganesson", "Orpiment"],
                'correct_answer': 1, 
                'explanation': "The chemical symbol 'O' represents Oxygen, an essential element for life on Earth."
            }
        ]
    },
    2: {
        'id': 2,
        'title': "Technical Knowledge Quiz",
        'description': "Test your technical knowledge with questions about programming, web development, and more.",
        'time_limit': 900,  
        'questions': [
            {
                'id': 1,
                'text': "What does HTML stand for?",
                'options': ["Hyper Text Markup Language", "High Tech Multi Language", "Hyper Transfer Markup Language", "Hyper Text Multiple Language"],
                'correct_answer': 0, 
                'explanation': "HTML stands for Hyper Text Markup Language, which is the standard markup language for creating web pages."
            },
            {
                'id': 2,
                'text': "Which of the following is not a programming language?",
                'options': ["Java", "Python", "HTTP", "C++"],
                'correct_answer': 2,  
                'explanation': "HTTP (Hypertext Transfer Protocol) is a protocol for transmitting data over the internet, not a programming language."
            },
            {
                'id': 3,
                'text': "What is the purpose of CSS in web development?",
                'options': ["To define the structure of a webpage", "To style and layout webpage content", "To handle server-side processing", "To manage databases"],
                'correct_answer': 1, 
                'explanation': "CSS (Cascading Style Sheets) is used to control the presentation and layout of web pages."
            },
            {
                'id': 4,
                'text': "Which of these is not a JavaScript framework or library?",
                'options': ["React", "Angular", "Django", "Vue"],
                'correct_answer': 2,  
                'explanation': "Django is a Python web framework, not a JavaScript framework or library."
            },
            {
                'id': 5,
                'text': "What does API stand for?",
                'options': ["Application Programming Interface", "Automated Program Integration", "Application Protocol Interface", "Advanced Programming Integration"],
                'correct_answer': 0,  
                'explanation': "API stands for Application Programming Interface, which defines interactions between multiple software applications."
            },
            {
                'id': 6,
                'text': "Which of the following is a NoSQL database?",
                'options': ["MySQL", "PostgreSQL", "MongoDB", "Oracle"],
                'correct_answer': 2, 
                'explanation': "MongoDB is a popular NoSQL database that uses a document-oriented data model."
            },
            {
                'id': 7,
                'text': "What is the purpose of the 'git' technology?",
                'options': ["Web hosting", "Version control", "Database management", "Frontend framework"],
                'correct_answer': 1, 
                'explanation': "Git is a distributed version control system for tracking changes in source code during software development."
            },
            {
                'id': 8,
                'text': "Which protocol is used for secure data transfer on the web?",
                'options': ["HTTP", "FTP", "HTTPS", "SMTP"],
                'correct_answer': 2,  
                'explanation': "HTTPS (Hypertext Transfer Protocol Secure) is used for secure communication over a computer network."
            },
            {
                'id': 9,
                'text': "What does SQL stand for?",
                'options': ["Structured Query Language", "Simple Query Language", "Standard Query Language", "Sequential Query Language"],
                'correct_answer': 0, 
                'explanation': "SQL stands for Structured Query Language, used for managing and manipulating relational databases."
            },
            {
                'id': 10,
                'text': "Which of these is an example of a cloud computing service?",
                'options': ["Windows 10", "Adobe Photoshop", "Amazon Web Services (AWS)", "Microsoft Word"],
                'correct_answer': 2, 
                'explanation': "Amazon Web Services (AWS) is a comprehensive cloud computing platform offering over 200 services globally."
            }
        ]
    }
}


ACTIVE_SESSIONS = {}
QUIZ_RESULTS = []
USERS = {}  
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if username in USERS:
        return "Username already exists. Go back and try again."
    
    USERS[username] = generate_password_hash(password)
    session['user'] = username
    return redirect(url_for('index'))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user_hash = USERS.get(username)
    if user_hash and check_password_hash(user_hash, password):
        session['user'] = username
        return redirect(url_for('index'))
    return "Invalid credentials. Please try again."


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))



@app.route('/')
def index():
    return render_template('index.html', quizzes=[
        {'id': 1, 'title': 'General Knowledge Quiz', 'description': 'Test your general knowledge with this quiz covering various topics.'},
        {'id': 2, 'title': 'Technical Knowledge Quiz', 'description': 'Test your technical knowledge with questions about programming, web development, and more.'}
    ])


@app.route('/quiz/<int:quiz_id>/start', methods=['GET', 'POST'])
def start_quiz(quiz_id):
    if request.method == 'POST':
      
        session_id = str(uuid.uuid4())
        session['quiz_session'] = session_id
        
        quiz = QUIZ_DATA.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
    
        ACTIVE_SESSIONS[session_id] = {
            'quiz_id': quiz_id,
            'start_time': datetime.now(),
            'user_answers': {},
            'time_limit': quiz.get('time_limit', 900)
        }
        
        return jsonify({
            'session_id': session_id,
            'redirect': url_for('quiz_page', quiz_id=quiz_id)
        })

    return redirect(url_for('index'))


@app.route('/quiz/<int:quiz_id>')
def quiz_page(quiz_id):
    quiz = QUIZ_DATA.get(quiz_id)
    if not quiz:
        return redirect(url_for('index'))
    
    session_id = session.get('quiz_session')
    
  
    if not session_id or session_id not in ACTIVE_SESSIONS:
        return redirect(url_for('index'))
    
    session_data = ACTIVE_SESSIONS[session_id]
    
   
    if session_data['quiz_id'] != quiz_id:
        return redirect(url_for('index'))

    safe_quiz = {
        'id': quiz['id'],
        'title': quiz['title'],
        'description': quiz['description'],
        'time_limit': quiz['time_limit'],
        'questions': []
    }
    
    for q in quiz['questions']:
        safe_quiz['questions'].append({
            'id': q['id'],
            'text': q['text'],
            'options': q['options']
        })
    
    return render_template('quiz.html', quiz=safe_quiz, session_id=session_id)


@app.route('/api/quiz/session/<session_id>/save-answer', methods=['POST'])
def save_answer(session_id):
    if session_id not in ACTIVE_SESSIONS:
        return jsonify({'error': 'Invalid session'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    question_id = data.get('question_id')
    answer_index = data.get('answer_index')
    
    if question_id is None or answer_index is None:
        return jsonify({'error': 'Invalid data'}), 400
    

    ACTIVE_SESSIONS[session_id]['user_answers'][str(question_id)] = answer_index
    
    return jsonify({'success': True})


@app.route('/api/quiz/session/<session_id>/submit', methods=['POST'])
def submit_quiz(session_id):
    if session_id not in ACTIVE_SESSIONS:
        return jsonify({'error': 'Invalid session'}), 400
    
    session_data = ACTIVE_SESSIONS[session_id]
    quiz_id = session_data['quiz_id']
    quiz = QUIZ_DATA.get(quiz_id)
    
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    

    user_answers = session_data['user_answers']
    score = 0
    results = []
    
    for question in quiz['questions']:
        q_id = str(question['id'])
        user_answer = user_answers.get(q_id)
        
        is_correct = user_answer == question['correct_answer'] if user_answer is not None else False
        if is_correct:
            score += 1
        
        results.append({
            'question_id': question['id'],
            'text': question['text'],
            'options': question['options'],
            'user_answer': user_answer,
            'correct_answer': question['correct_answer'],
            'explanation': question['explanation'],
            'is_correct': is_correct
        })
    

    time_taken = (datetime.now() - session_data['start_time']).total_seconds()
    if time_taken > session_data['time_limit']:
        time_taken = session_data['time_limit']
    
  
    result_data = {
        'session_id': session_id,
        'quiz_id': quiz_id,
        'quiz_title': quiz['title'],
        'score': score,
        'max_score': len(quiz['questions']),
        'time_taken': time_taken,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    QUIZ_RESULTS.append(result_data)
    

    if session_id in ACTIVE_SESSIONS:
        del ACTIVE_SESSIONS[session_id]
    
 
    return jsonify({
        'score': score,
        'max_score': len(quiz['questions']),
        'percentage': round((score / len(quiz['questions']) * 100), 1),
        'time_taken': time_taken,
        'results': results
    })


@app.route('/quiz/results/<session_id>')
def results_page(session_id):
  
    result = next((r for r in QUIZ_RESULTS if r['session_id'] == session_id), None)
    
    if not result:
        return redirect(url_for('index'))
    
    return render_template('results.html', result=result)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)