from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  


officers_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Model(HINDI)\Udhami_Yojna_Officers.csv')
queries_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Udhami_Yojna_Queries.csv')
faq_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Model(HINDI)\FAQ_Database_Normal.csv')


officers_df.columns = officers_df.columns.str.strip()
queries_df.columns = queries_df.columns.str.strip()
faq_df.columns = faq_df.columns.str.strip()


model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


faq_questions = faq_df['Question'].tolist()
faq_answers = faq_df['Answer'].tolist()
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

officer_descriptions = officers_df['Description'].tolist()
officer_embeddings = model.encode(officer_descriptions, convert_to_tensor=True)


def get_direct_answer(query_embedding, faq_embeddings, faq_answers, threshold=0.80):
    similarities = util.pytorch_cos_sim(query_embedding, faq_embeddings)
    best_match_idx = torch.argmax(similarities).item()
    similarity_score = similarities[0, best_match_idx].item()

    if similarity_score >= threshold:
        return faq_answers[best_match_idx], similarity_score
    return None, similarity_score


def assign_top_officer(query_embedding, officer_embeddings, officers_df):
    similarities = util.pytorch_cos_sim(query_embedding, officer_embeddings)
    best_match_idx = torch.argmax(similarities).item()
    assigned_officer = officers_df.iloc[best_match_idx]['Category']
    similarity_score = similarities[0, best_match_idx].item()
    return assigned_officer, similarity_score

@app.route('/process-query', methods=['POST'])
def process_query():
    user_query = request.json.get("query")
    query_embedding = model.encode([user_query], convert_to_tensor=True)

    
    answer, similarity_score = get_direct_answer(query_embedding, faq_embeddings, faq_answers)
    if answer:
        return jsonify({"type": "direct_answer", "response": answer, "score": similarity_score})

    
    assigned_officer, officer_similarity_score = assign_top_officer(query_embedding, officer_embeddings, officers_df)
    return jsonify({"type": "assigned_officer", "response": assigned_officer, "score": officer_similarity_score})


if __name__ == "__main__":
    app.run(debug=True)
