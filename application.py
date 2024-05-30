from flask import Flask, request, jsonify
import pymysql


app = Flask(__name__)

db_config = {
    'host' : 'localhost',
    'user' : 'root',
    'password' : 'Ou812@My3801',
    'database' : 'tests'
}

db_conn = pymysql.connect(**db_config)
cursor = db_conn.cursor()

@app.route('/exam', methods=['GET'])
def health_check():
    return jsonify({'Health_Check': 'Health Check Successful!'})

@app.route('/exam/question/add', methods=['POST'])
def add_question():
    try:
        data = request.get_json()
        exam_id = data.get('exam_id')
        exam_name = data.get('exam_name')
        question_id = data.get('question_id')
        question = data.get('question')
        scenario = data.get('scenario')
        choice_1 = data.get('choice_1')
        choice_2 = data.get('choice_1')
        choice_3 = data.get('choice_1')
        choice_4 = data.get('choice_1')
        choice_5 = data.get('choice_1')
        answer = data.get('answer')
        why = data.get('why')

        sql = 'INSERT INTO exams (ExamID, ExamName, QuestionID, Question, Scenario, Choice_1, Choice_2, Choice_3, Choice_4, Choice_5, Answer, Why) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        tup = (exam_id, exam_name, question_id, question, scenario, choice_1, choice_2, choice_3, choice_4, choice_5, answer, why)
        cursor.execute(sql, tup)
        db_conn.commit()

        return jsonify({'message': 'New question successfully entered into database'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/exam/user_info/answer', methods=['POST'])
def record_answer():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        exam_id = data.get('exam_id')
        question_id = data.get('question_id')
        answer_given = data.get('answer_given')
    
        sql = 'INSERT INTO test_results (UserID, ExamID, QuestionID, AnswerGiven) VALUES (%s, %s, %s, %s)'
        tup = (user_id, exam_id, question_id, answer_given)
        cursor.execute(sql, tup)
        db_conn.commit()
        return jsonify({'message': 'New user answer successfully entered into database'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
@app.route('/exam/user_info/add', methods=['POST'])
def user_info_add():
    try:
        data = request.get_json()
        user_name = data.get('user_name')
        email_address = data.get('email_address')

        sql = 'INSERT INTO users (UserName, EmailAddress) VALUES (%s, %s)'
        tup = (user_name, email_address)
        cursor.execute(sql, tup)
        db_conn.commit()
        return jsonify({'message': 'New User was successfully entered into database'})
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/exam/test_info/add', methods=['POST'])
def test_info_add():
    try:
        data = request.get_json()
        exam_name = data.get('exam_name')
        exam_cost = data.get('exam_cost')
        pass_percentage = data.get('pass_percentage')
        info_address = data.get('info_address')
        
        sql = 'INSERT INTO test_info (ExamName, ExamCost, PassPercentage, InfoAddress) VALUES (%s, %s, %s, %s)'
        tup = (exam_name, exam_cost, pass_percentage, info_address)
        cursor.execute(sql, tup)
        db_conn.commit()
        return jsonify({'message': 'New test info was successfully entered into database'})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/exam/list/<category>', methods=['GET', 'POST'])
def get_list_of_exams(category):
    try:
        sql = "SELECT ID, ExamName, ExamCost, PassPercentage, InfoAddress, Category, SubCategory, Active FROM test_info WHERE Category='"+ category +"'"
        cursor.execute(sql)
        results = [{'ExamID': ID, 'ExamName': ExamName, 'ExamCost': ExamCost, 'PassPercentage': PassPercentage, 'InfoAddress': InfoAddress, 'Category': Category, 'SubCategory': SubCategory, 'Active': Active} for ID, ExamName, ExamCost, PassPercentage, InfoAddress, Category, SubCategory, Active in cursor.fetchall()]
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/exam/question', methods=['GET'])
def get_question():
    try:
        data = request.get_json()
        exam_id = data.get('exam_id')
        question_id = data.get('question_id')

        sql = 'SELECT QuestionID, Question, Scenario, Choice_1, Choice_2, Choice_3, Choice_4, Choice_5 FROM exams WHERE ExamID={} AND QuestionID={}'.format(exam_id, question_id)
        cursor.execute(sql)
        result = [{'QuestionID': QuestionID, 'Question': Question, 'Scenario': Scenario, 'Choice_1': Choice_1, 'Choice_2': Choice_2, 'Choice_3': Choice_3, 'Choice_4': Choice_4, 'Choice_5': Choice_5} for QuestionID, Question, Scenario, Choice_1, Choice_2, Choice_3, Choice_4, Choice_5 in cursor.fetchall()]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error' : str(e)})
    
@app.route('/exam/question/amount', methods=['GET'])
def get_question_amount():
    try:
        data = request.get_json()
        exam_id = data.get('exam_id')

        sql = 'SELECT count(ExamID) AS NumberOfQuestions FROM exams WHERE ExamID={}'.format(exam_id)
        cursor.execute(sql)
        NumberOfQuestions = cursor.fetchone()[0]
        result = {'NumberOfQuestion': NumberOfQuestions}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)

