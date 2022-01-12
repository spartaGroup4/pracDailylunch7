from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API 역할을 하는 부분
@app.route('/api/comments', methods=['POST'])
def write_comment():
    # title_receive로 클라이언트가 준 title 가져오기
    nick_receive = request.form['nick_give']
    comment_receive = request.form['comment_give']

    # DB에 삽입할 review 만들기
    doc = {
        'nick' : nick_receive,
        'comment' : comment_receive 
    }
    # reviews에 review 저장하기
    db.dailylunch.insert_one(doc)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'msg': '댓글이 성공적으로 작성되었습니다.'})


@app.route('/api/comments', methods=['GET'])
def read_comment():
    # 1. DB에서 리0뷰 정보 모두 가져오기
    lunches = list(db.dailylunch.find({}, {'_id': False}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'all_lunches': lunches})

@app.route('/api/comment_delete', methods=['POST'])
def delete_comment():
    comment_receive = request.form['comment_give']
    db.dailylunch.delete_one({'comment': comment_receive})
    return jsonify({'msg': '삭제 완료!'})

@app.route('/api/menu', methods=['POST'])
def like_menu():
    title_receive = request.form['title_give']

    target_title = db.dailylunch.find_one({'title': title_receive})
    current_like = target_title['like']
    # target_like중에서 like만 가져오고싶다

    new_like = current_like + 1

    db.dailylunch.update_one({'title': title_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)