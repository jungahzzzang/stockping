from app import * # main에 선언된 모든 값을 가져온다.
from flask import Blueprint, jsonify, request, redirect
from pymongo import MongoClient
import datetime

app = Flask(__name__)

blueprint = Blueprint("board", __name__, template_folder="templates", static_folder="static", url_prefix="/")

with open(abs_path+'/app/settings/config.json', 'r') as f:
    config = json.load(f)
    db_info = config['DB']
    host='127.0.0.1'
    db_name = db_info['db_name']
    collection_name = db_info['board_collection']
        
    #몽고디비 연결   
    client = MongoClient(db_info['MONGO_URI'])
    db = client.db_name
    collection = db.collection_name

# 글 목록
@blueprint.route('/board/list')
def list():
    
    # articles = list(db.collection_name.find({},{'_id':False}).sort('pubDate', -1))
    # return jsonify({'result': 'success', 'articles': articles})
    
    return render_template('boardList.html')

# 글 쓰기
@blueprint.route('/board/write', methods=['POST'])
def write():
    
    article_title = request.form['title_input']
    article_content = request.form['content_input']
    now = datetime.datetime.now()
    article_create_at = now.today()
    article_modified_at = now.today()
    article_view = 0
    # article_user_id 
    
    db.collection_name.insert_one({'article_title': article_title, 'article_content': article_content, 'article_create_at': article_create_at,
                                   'article_modified_at': article_modified_at, 'article_view': article_view})
    
    return redirect('/board/list')

# 글 상세
@blueprint.route('/board/<article_id>', methods=['GET'])
def read(article_id):
    
    article = db.collection_name.find_one({'_id': article_id})
    
    # return render_template('boardDetail.html', article=article, user_id = user_id)
    return render_template('boardDetail.html', article=article)

# 글 수정
@blueprint.route('/board/<article_id>/modify', methods=['GET'])
def modify(article_id):
    
    article = db.collection_name.find_one({'_id': article_id})
    
    # return render_template('boardDetail.html', article=article, user_id = user_id)
    return render_template('boardDetail.html', article=article)

# 글 수정
@blueprint.route('/board/<article_id>/modify_process')
def modify_process(article_id):
    
    article_title = request.form['title_input']
    article_content = request.form['content_input']
    now = datetime.datetime.now()
    article_modified_at = now.today()
    
    db.collection_name.update_one({'_id':article_id}, {'$set': {'article_title' : article_title, 'article_content' : article_content,'article_modified_at' : article_modified_at}})
    
    return redirect('/board/list')

# 글 삭제
@blueprint.route('/board/<article_id>/delete', methods=['DELETE'])
def delete(article_id):
    
    db.collection_name.delete_one({'_id': article_id})

    return redirect('/board/list')