import tiktoken


TEXT = "In one or two sentences, what’s the best way to protect against ransomware?"

TOKENIZERS = {
    "cl100k_base (modern GPT models)": "cl100k_base",
    "p50k_base (older GPT-3.5 era)": "p50k_base",
    "r50k_base (very old / GPT-2 style)": "r50k_base",
}


def visualize_whitespace(text: str) -> str:
    return (
        text.replace(" ", "␠")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
    )


def main() -> None:
    print("Original text:")
    print(TEXT)
    print("=" * 80)

    for label, encoding_name in TOKENIZERS.items():
        encoding = tiktoken.get_encoding(encoding_name)
        token_ids = encoding.encode(TEXT)

        print(f"\nTokenizer: {label}")
        print(f"Encoding name: {encoding_name}")
        print(f"Token count: {len(token_ids)}")
        print("-" * 80)

        for i, tid in enumerate(token_ids, start=1):
            token_text = encoding.decode([tid])
            visible = visualize_whitespace(token_text)
            print(f"{i:>3}. '{visible}'")

        print("-" * 80)


if __name__ == "__main__":
    main()
