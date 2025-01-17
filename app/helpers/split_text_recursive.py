from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text_recursive(
    text: str,
    chunk_size: int = 100,
    chunk_overlap: int = 25,
) -> list[str]:
    split_text_recursive = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    result = split_text_recursive.split_text(text)
    return result


if __name__ == "__main__":
    example_text = """Lorem Ipsum Foo Bar Text to test the split text recursive function"""
    list_of_texts = split_text_recursive(example_text)
    print(list_of_texts)
