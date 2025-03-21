from taskfind import tasksfinder

def main():
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == "exit":
            print("Exiting...")
            break
        print(tasksfinder(user_query))

if __name__ == "__main__":
    main()
