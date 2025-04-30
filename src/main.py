
#enable this when not using web
from taskfind import tasksfinder
from flask_cors import CORS
from Chain import Chain

# def main():
#     while True:
#         user_query = input("Enter your query (or type 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Exiting...")
#             break
#         # for data in tasksfinder(user_query):
#         #     print(data, end="")
#         Chain(user_query)

# if __name__ == "__main__":
#     main()


# def main():
#     while True:
#         user_query = input("Enter your query (or type 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Exiting...")
#             break
#         print(tasksfinder(user_query))
       

# if __name__ == "__main__":
#     main()

from flask import Flask, Response, request
from pydantic import BaseModel
import time

app = Flask(__name__)
CORS(app) 

class UserQuery(BaseModel):
    query: str  




@app.route('/stream', methods=['POST'])
def stream():
   
    data = request.get_json()
    user_query = data.get("query", "Default Query") 
    print(user_query)
  
    return Response(tasksfinder(user_query), content_type='text/event-stream')




if __name__ == '__main__':
    app.run(debug=True, threaded=True)

