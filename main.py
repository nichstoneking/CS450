import chromadb

def main():
    print("Hello from cs450!")
    client = chromadb.PersistentClient(path="./chromadb")
    collection = client.get_collection("slides")

    print(collection.count())

if __name__ == "__main__":
    main()
