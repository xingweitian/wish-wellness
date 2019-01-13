from pymongo import MongoClient
from instance.config import MONGO_URL_GCP


class MongoTransaction(object):

    def __init__(self):
        self.m = MongoClient(MONGO_URL_GCP)
        self.db = self.m["starterhack2019"]
        self.user_info_collection = self.db["user_info"]
        self.user_survey_collection = self.db["user_survey"]

    def insert(self, email, age, gender, interests, medication, first_name, last_name):
        data = dict()
        data['email'] = email
        data['age'] = age
        data['gender'] = gender
        data['interests'] = interests
        data['medication'] = medication
        data['first_name'] = first_name
        data['last_name'] = last_name
        try:
            self.user_info_collection.insert_one(data)
        except Exception as e:
            print(e)

    def search(self, username):
        try:
            res = self.user_info_collection.find_one({"email": username})
            if res:
                return res
            else:
                return None
        except Exception as e:
            print(e)

    def survey(self, email, anxiety, mood, eating, psych, pers):
        data = dict()
        data['email'] = email
        data['anxiety'] = anxiety
        data['mood'] = mood
        data['eating'] = eating
        data['psych'] = psych
        data['pers'] = pers
        try:
            self.user_survey_collection.insert_one(data)
            return True
        except Exception as e:
            print(e)
            return False

    def search_survey_data(self, email):
        try:
            cursor = self.user_survey_collection.find({'email': email})
            i, res = 0, []
            for each in cursor:
                res.append(each)
                i += 1
                if i == 7:
                    break
            return res
        except Exception as e:
            print(e)


if __name__ == "__main__":
    m = MongoTransaction()
    print(type(m.search("postman")))
    print(m.search("postman"))
