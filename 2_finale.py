import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch


officers_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Model(HINDI)\Udhami_Yojna_Officers.csv')
queries_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Udhami_Yojna_Queries.csv')
faq_df = pd.read_csv(r'C:\Users\HP\Desktop\Projects 2k24\NS Apps- Wooorkkk\YOJNA_Query_classification\MODEL\Model(HINDI)\FAQ_Database_Normal.csv')  # Predefined questions/answers


officers_df.columns = officers_df.columns.str.strip()
queries_df.columns = queries_df.columns.str.strip()
faq_df.columns = faq_df.columns.str.strip()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

faq_questions = faq_df['Question'].tolist()
faq_answers = faq_df['Answer'].tolist()
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

officer_descriptions = officers_df['Description'].tolist()
officer_embeddings = model.encode(officer_descriptions, convert_to_tensor=True)

def get_direct_answer(query_embedding, faq_embeddings, faq_answers, threshold=0.75):
    similarities = util.pytorch_cos_sim(query_embedding, faq_embeddings)
    best_match_idx = torch.argmax(similarities).item()
    similarity_score = similarities[0, best_match_idx].item()
    return faq_answers[best_match_idx] if similarity_score >= threshold else None, similarity_score

def assign_top_officer(query_embedding, officer_embeddings, officers_df):
    similarities = util.pytorch_cos_sim(query_embedding, officer_embeddings)
    best_match_idx = torch.argmax(similarities).item()
    assigned_officer = officers_df.iloc[best_match_idx]['Category']
    similarity_score = similarities[0, best_match_idx].item()
    return assigned_officer, similarity_score


def process_query(user_query, model, faq_embeddings, officer_embeddings, faq_answers, officers_df):
    query_embedding = model.encode([user_query], convert_to_tensor=True)

    
    answer, faq_similarity = get_direct_answer(query_embedding, faq_embeddings, faq_answers)

    
    assigned_officer, officer_similarity = assign_top_officer(query_embedding, officer_embeddings, officers_df)

    if answer:
        return (f"Direct Answer: {answer} (FAQ Similarity Score: {faq_similarity:.4f})\n"
                f"Officer Assignment (for reference): {assigned_officer} (Officer Similarity Score: {officer_similarity:.4f})")
    else:
        return (f"No direct FAQ match found.\n"
                f"Assigned Officer: {assigned_officer} (Officer Similarity Score: {officer_similarity:.4f})")


while True:
    test_query = input("Please enter your query: ")
    result = process_query(test_query, model, faq_embeddings, officer_embeddings, faq_answers, officers_df)
    print(result)
