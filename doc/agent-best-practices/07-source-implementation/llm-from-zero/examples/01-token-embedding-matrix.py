from __future__ import annotations

TOKENS = ["猫", "喜欢", "鱼"]

VOCAB = {
    "猫": 0,
    "狗": 1,
    "鱼": 2,
    "喜欢": 3,
    "微积分": 4,
}

ID_TO_TOKEN = {token_id: token for token, token_id in VOCAB.items()}

# These values are illustrative. Real embeddings are learned parameters.
EMBEDDING_TABLE = [
    [0.80, 0.10, 0.70, -0.20],
    [0.76, 0.14, 0.66, -0.18],
    [0.64, -0.05, 0.62, -0.08],
    [0.10, 0.72, 0.15, 0.40],
    [-0.30, 0.88, -0.42, 0.65],
]


def encode(tokens: list[str], vocab: dict[str, int]) -> list[int]:
    return [vocab[token] for token in tokens]


def make_one_hot_matrix(token_ids: list[int], vocab_size: int) -> list[list[float]]:
    rows = []
    for token_id in token_ids:
        row = [0.0] * vocab_size
        row[token_id] = 1.0
        rows.append(row)
    return rows


def matmul(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    right_columns = list(zip(*right))
    return [
        [sum(a * b for a, b in zip(row, column)) for column in right_columns]
        for row in left
    ]


def embedding_lookup(
    token_ids: list[int],
    embedding_table: list[list[float]],
) -> list[list[float]]:
    return [embedding_table[token_id] for token_id in token_ids]


def print_matrix(name: str, matrix: list[list[float]], labels: list[str]) -> None:
    print(f"{name} shape: {len(matrix)} x {len(matrix[0])}")
    for label, row in zip(labels, matrix):
        values = ", ".join(f"{value:>5.2f}" for value in row)
        print(f"{label:<4} [{values}]")
    print()


def main() -> None:
    token_ids = encode(TOKENS, VOCAB)
    labels = [ID_TO_TOKEN[token_id] for token_id in token_ids]

    one_hot_matrix = make_one_hot_matrix(token_ids, len(VOCAB))
    x_by_matrix = matmul(one_hot_matrix, EMBEDDING_TABLE)
    x_by_lookup = embedding_lookup(token_ids, EMBEDDING_TABLE)

    print("tokens:", TOKENS)
    print("token ids:", token_ids)
    print()

    print_matrix("one_hot_matrix", one_hot_matrix, labels)
    print_matrix("X = one_hot_matrix @ embedding_table", x_by_matrix, labels)
    print("matrix multiply equals direct lookup:", x_by_matrix == x_by_lookup)


if __name__ == "__main__":
    main()

