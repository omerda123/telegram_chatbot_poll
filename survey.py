from pymongo import MongoClient


def insert_questions():
    client = MongoClient()
    db = client.get_database("survey")
    questions = db.get_collection("questions")

    questions.insert_one(
        {
            "id": 0,
            "question": "היי, האם תרצה להשתתף בסקר קצר לקראת הבחירות?",
            "answers": [
                "כן",
                "לא",
            ]
        }
    )

    questions.insert_one(
        {
            "id": 1,
            "question": "How old are you?",
            "answers": [
                f"18 - 30",
                f"30 - 40",
                f"40 - 50",
                f" > 50",
            ]
        }
    )
    questions.insert_one(
        {
            "id": 2,
            "question": "What is your gender?",
            "answers": [
                "Male",
                "Female",
                "undefined"
            ]
        }
    )
    questions.insert_one(
        {
            "id": 3,
            "question": "Where do you live?",
        }

    )

    questions.insert_one(
        {
            "id": 4,
            "question": "which party you are going to vote??",
            "answers": [
                "ליכוד",
                "כחול לבן",
                "ש''ס",
                "ימינה",
            ]
        }
    )


def get_answers_array_by_id(id: int):
    client = MongoClient()
    db = client.get_database("survey")
    questions = db.get_collection("questions")
    res = questions.find_one({"question_id": id})
    return res
