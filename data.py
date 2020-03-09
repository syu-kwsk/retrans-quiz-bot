import json

from bot.models import Quiz, User, db, init
i = 0
with open('quiz.json') as fin:
    for line in fin:
        if i < 1000:
            data = json.loads(line)
            quiz = Quiz(question=data['question'], answer=data['answer'])
            db.session.add(quiz)
            db.session.commit()
            i += 1

        else:
            data = json.loads(line)
            continue

'''
i = 0
datas = []
with open('quiz.json') as fin:
    for line in fin:
        if i < 1000:
            data = json.loads(line)
            with open('quiz_sub.json', mode="a") as f:
                json.dump({"question":data['question'], "answer" : data['answer']}, f, ensure_ascii=False)
                print('', file=f)
            i += 1

        else:
            data = json.loads(line)
            continue

'''
