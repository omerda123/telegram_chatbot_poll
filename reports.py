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
    18-30: {results.count_documents({"age": "18-30"})}
    30-40: {results.count_documents({"age": "30-40"})}
    40-50: {results.count_documents({"age": "40-50"})}
    """


def companies_distributions(results):
    return f""" 
    the number of votes are: {results.count_documents({})}
    Likud: {results.count_documents({"party": "ליכוד"})}
    kahol lavan: {results.count_documents({"party": "כחול לבן"})}
    Shas: {results.count_documents({"party": "שס"})}
    Yemina: {results.count_documents({"party": "ימינה"})}
    """


def companies_graph(results):
    total_votes = results.count_documents({})
    char = "|"
    return f"""
    {'Likud:':15} {char * int(results.count_documents({"party": "ליכוד"}) * 100 / total_votes)} 
    {'kahol lavan:':15} {char * int(results.count_documents({"party": "כחול לבן"}) * 100 / total_votes)} 
    {'Shas:':15} {char * int(results.count_documents({"party": "שס"}) * 100 / total_votes)} 
    {'Likud:':15} {char * int(results.count_documents({"party": "ימינה"}) * 100 / total_votes)} 
    """


while True:
    print("what do you want to do?")
    print("""
        1. see how many people voted 
        2. see how many people accepted the vote
        3. see ages distributions 
        4. companies distribution
        5. companies graph
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
    elif choice == "4":
        print(companies_distributions(all_results))
    elif choice == "5":
        print(companies_graph(all_results))
