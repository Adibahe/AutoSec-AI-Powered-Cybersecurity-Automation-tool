
#enable this when not using web
from taskfind import tasksfinder


def main():
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Exiting...")
            break
        for data in tasksfinder(user_query):
            print(data, end="")

if __name__ == "__main__":
    main()


# def main():
#     while True:
#         user_query = input("Enter your query (or type 'exit' to quit): ")
#         if user_query.lower() == "exit":
#             print("Exiting...")
#             break
#         print(tasksfinder(user_query))
       

# if __name__ == "__main__":
#     main()

# from flask import Flask, Response, request
# from pydantic import BaseModel
# import time

# app = Flask(__name__)

# # Define the UserQuery model using Pydantic
# class UserQuery(BaseModel):
#     query: str  # User input query string

# # Function to generate SSE stream based on user query
# def generate_stream(user_query: str):
#     responses = [
#         f"Processing query: {user_query}",
#         "Fetching relevant information...",
#         "Analyzing...",
#         "Generating response...",
#         "Final response: Here is your answer!"
#     ]
    
#     for msg in responses:
#         yield f"data: {msg}\n\n"  # SSE format (data: <message>\n\n)
#         time.sleep(2)  # Simulating delay

# # SSE route that accepts user input via POST request
# @app.route('/stream', methods=['POST'])
# def stream():
#     # Parse request JSON
#     data = request.get_json()
#     user_query = data.get("query", "Default Query")  # Default if query is missing

#     # Return SSE response
#     return Response(tasksfinder(user_query), content_type='text/event-stream')

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True, threaded=True)

