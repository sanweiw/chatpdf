from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import shutil, os
from flask_cors import CORS
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from utils import allowed_file, file_hash
from vector_db import MyVectorDBConnector
from chat_bot import RAG_Bot
from openai_utils import get_embeddings, get_completion
from pdf_processing import extract_text_from_pdf

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['initialized'] = False
vector_db = None
bot = None

# Routes and other functions remain mostly unchanged, but now import and use the modularized components.
@app.route('/upload', methods=['POST'])
def upload_file():
    print("enter upload_file")
    # 检查是否有文件在请求中
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    # 如果用户没有选择文件，浏览器也会提交一个空的文件名
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):

        # 使用临时文件计算哈希值
        with NamedTemporaryFile(delete=False) as tmp_file:
            file.save(tmp_file)
            tmp_file.seek(0)  # 回到文件开头，以便重新读取内容进行哈希计算
            file_hash_value = file_hash(tmp_file)

        hash_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'hashes.txt')
        if os.path.exists(hash_file_path):
            with open(hash_file_path, 'r') as hash_file:
                if file_hash_value in hash_file.read():
                    os.remove(tmp_file.name)  # 删除临时文件
                    return jsonify({'message': 'File already exists'}), 200

        # 文件是新的，移动到最终目录
        final_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        # os.rename(tmp_file.name, final_path)
        shutil.move(tmp_file.name, final_path)  # 使用shutil.move代替os.rename

        with open(hash_file_path, 'a') as hash_file:
            hash_file.write(file_hash_value + '\n')

        # 在这里调用extract_text_from_pdf函数处理上传的PDF文件
        paragraphs = extract_text_from_pdf(final_path, min_line_length=10)

        # 向向量数据库中添加文档
        vector_db.add_documents(paragraphs)

        return jsonify({'message': 'File saved'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

    
@app.route('/process-input', methods=['POST'])
def process_input():
    global bot
    # 获取 JSON 数据
    data = request.json
    input_text = data.get('input_text')
    # results = vector_db.search(input_text, top_n=2) 

    # for para in results['documents'][0]:
    #     print(para+"\n")
    print(input_text)
    response = bot.chat(input_text)
    print(response)
    return jsonify({'message': response}), 200


# Ensure UPLOAD_FOLDER exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def process_pdf_file(filename):
    """Extract text from a PDF file and add it to the vector database."""
    print(f"Processing {filename}")
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    paragraphs = extract_text_from_pdf(file_path, min_line_length=10)
    vector_db.add_documents(paragraphs)

def add_documents_to_vector_db():
    """Add documents from the UPLOAD_FOLDER to the vector database."""
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.pdf'):
            try:
                process_pdf_file(filename)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    print("All documents have been added to the vector database.")

# @app.before_first_request
@app.before_request
def initialize_vector_db():
    """Initialize the vector database and RAG bot before the first request."""
    global vector_db, bot
    if not app.config.get('initialized', False):
        print('Initializing vector database...')
        vector_db = MyVectorDBConnector("demo", get_embeddings)
        add_documents_to_vector_db()
        bot = RAG_Bot(vector_db, llm_api=get_completion)
        app.config['initialized'] = True

if __name__ == '__main__':
    app.run(debug=True)