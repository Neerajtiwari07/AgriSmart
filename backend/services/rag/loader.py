from langchain_community.document_loaders import CSVLoader


def load_documents():

    loader = CSVLoader(
        file_path="datasets/agri_faq.csv",
        encoding="utf-8"
    )

    documents = loader.load()

    print(f"Loaded {len(documents)} documents")

    return documents