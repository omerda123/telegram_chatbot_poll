from pymongo import MongoClient


def total_count(results):
    return f"the number of votes are: {results.count_documents({})}"


def get_data():
    client = MongoClient()
    db = client.get_database("survey")
    return db.get_collection("results")


all_results = get_data()


def total_accepted(results):
    return f""" 
    the number of votes are: {results.count_documents({})}
    the number of accepted are: {results.count_documents({"want": "כן"})}
    the number of decline are: {results.count_documents({"want": "לא"})}
    """


def ages_distributions(results):
    return f""" 
    the number of votes are: {results.count_documents({})}
    the number of accepted are are: {results.count_documents({"want": "כן"})}
    the number of decline are: {results.count_documents({"want": "לא"})}
    """


while True:
    print("what do you want to do?")
    print("""
        1. see how many people voted 
        2. see how many people accepted the vote
        3. see ages distributions 
        x. exit() 
    """)
    choice = input("")
    if choice == "x":
        break
    elif choice == "1":
        print(total_count(all_results))
    elif choice == "2":
        print(total_accepted(all_results))
    elif choice == "3":
        print(ages_distributions(all_results))
