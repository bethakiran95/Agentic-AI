# Progress Log

## Vector Database Basics

This exercise introduced ChromaDB, a vector database that searches text by semantic similarity (meaning) rather than only exact keyword matches.

Notebook: [vector_db_basics.ipynb](vector_db_basics.ipynb)

## What Was Built

### 1. Created a ChromaDB client

```python
import chromadb

client = chromadb.Client()
```

- `chromadb.Client` is the client class (the blueprint).
- `chromadb.Client()` creates a usable client object from that class.
- `client` manages collections in the database.
- This default client is in-memory, so its data is lost when the notebook kernel/process is restarted.

### 2. Created a collection

```python
collection = client.get_or_create_collection("news")
```

A collection is similar to a table or folder containing related records. The `collection` object represents the collection named `news` and provides methods such as `upsert()`, `query()`, `get()`, `count()`, and `delete()`.

`get_or_create_collection()` was used instead of `create_collection()` so rerunning the cell does not fail when the collection already exists.

### 3. Stored four documents

```python
collection.upsert(
    ids=["id1", "id2", "id3", "id4"],
    documents=[
        "Apple is leading in a smart phone game with iPhone sales up by 35%",
        "Tesla booked a minor profit of 1 billion $ in Q2",
        "Apples are high in fiber, vitamin C, and various antioxidants",
        "SpaceX got NASA contract worth 10 billion $",
    ]
)
```

Each document has a unique ID. The number of IDs must equal the number of documents.

The original code had three IDs and four documents, which caused this error:

```text
ValueError: Unequal lengths for fields: ids: 3, documents: 4
```

Adding `"id4"` fixed the issue.

`upsert()` means **update or insert**:

- If an ID is new, ChromaDB inserts the record.
- If the ID already exists, ChromaDB updates the record.
- This is convenient in notebooks because the same cell can be rerun.

By comparison, `add()` is intended for new records and does not replace an existing ID.

## How Semantic Search Works

When documents are inserted, ChromaDB uses an embedding function to represent their meaning as numerical vectors. A query is also converted into a vector, and ChromaDB returns the stored vectors nearest to it.

```python
result = collection.query(
    query_texts=["This is a query related to Elon Musk"],
    n_results=2
)
print(result)
```

`n_results=2` asks ChromaDB to return the two nearest documents.

The Elon Musk query returned the Tesla and SpaceX documents. This shows semantic matching: the query did not need to contain the words `Tesla` or `SpaceX` to find related text.

The iPad query returned the iPhone document first. It also returned the fruit-related Apple document because both contain the word `Apple`. This demonstrates that embeddings can understand useful relationships but can also produce imperfect matches.

## Understanding the Query Result

The returned dictionary includes fields such as:

- `ids`: IDs of the matched records.
- `documents`: text of the matched records.
- `distances`: distance between each query vector and result vector. For the same collection and distance metric, a smaller distance generally means a closer match.
- `metadatas`: optional structured information associated with each record. It is `None` here because no metadata was added.
- `embeddings`: `None` in the output because embeddings were not requested as returned data. They are still used internally for the search.

## Important Limitation

A vector database returns the nearest available results; it does not automatically know whether those results are truly relevant.

For example, the collection contains no information about Bill Gates, but this query still returns two documents because `n_results=2` requests two nearest matches:

```python
collection.query(
    query_texts=["who is Bill Gates"],
    n_results=2
)
```

This does not mean the returned documents answer the question. A real application should check distance/relevance, use metadata filters, or apply another validation step before presenting results as an answer.

## What Was Achieved

- Created an in-memory ChromaDB database client.
- Created a reusable `news` collection.
- Inserted and updated documents safely with `upsert()`.
- Converted text into embeddings automatically through ChromaDB.
- Performed semantic searches and inspected IDs, documents, and distances.
- Observed both useful semantic matches and irrelevant nearest matches.
- Made all notebook cells rerunnable and verified that all six cells execute successfully.

## Next Step

The natural next step is to add metadata (for example, category or company), test filtered queries, and use a persistent ChromaDB client so records survive kernel restarts.
