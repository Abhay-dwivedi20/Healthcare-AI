import json
from database.db import get_db

def create_report(user_id, disease_type, input_data):
    print("📌 Saving report for:", disease_type)  # DEBUG LINE

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (user_id, disease_type, input_data)
        VALUES (?, ?, ?)
    """, (user_id, disease_type, json.dumps(input_data)))

    report_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return report_id



def create_diagnostic_result(report_id, prediction, confidence, model_used):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO diagnostic_results 
        (report_id, prediction, confidence, model_used)
        VALUES (?, ?, ?, ?)
    """, (report_id, prediction, confidence, model_used))

    conn.commit()
    conn.close()

def save_chat_log(user_message, bot_reply):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_logs (user_message, bot_reply)
        VALUES (?, ?)
    """, (user_message, bot_reply))

    conn.commit()
    conn.close()


def get_all_predictions():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            r.id,
            r.disease_type,
            r.input_data,
            d.prediction,
            d.confidence,
            d.model_used,
            r.created_at
        FROM reports r
        JOIN diagnostic_results d ON r.id = d.report_id
        ORDER BY r.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows
