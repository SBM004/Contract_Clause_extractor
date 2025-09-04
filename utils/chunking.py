from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunking(pdf_text):
    splitter=RecursiveCharacterTextSplitter(
        # chunk_size=10000,
        # chunk_overlap=400
        chunk_size=4000, 
        chunk_overlap=200,
        separators=['\n','\n\n']
    )

    chunks=splitter.split_text(pdf_text)
    print(len(chunks))
    return chunks