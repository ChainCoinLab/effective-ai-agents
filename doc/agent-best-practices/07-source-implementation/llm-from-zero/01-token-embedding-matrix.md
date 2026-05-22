# 01. token id 如何查出 embedding 向量矩阵

[返回专题首页](README.md)

本节只完成一个小任务：把一段已经切好的 token 序列，变成模型可以继续计算的向量矩阵。

输入：

```text
["猫", "喜欢", "鱼"]
```

输出：

```text
token ids: [0, 3, 2]
X shape: 3 x 4
```

也就是得到一个 `3 x 4` 的矩阵：3 行对应 3 个 token，4 列对应每个 token 的 embedding 维度。

## 本节先不做什么

这一节先不实现 tokenizer 算法，也不训练 embedding。为了看清矩阵关系，我们手工准备一个很小的词表和一张 embedding table。

真实大模型里的词表可能有几万到十几万个 token，embedding 维度可能是几千。这里缩小成：

```text
词表大小 V = 5
向量维度 d = 4
序列长度 n = 3
```

## 关键矩阵关系

先定义词表：

```text
猫     -> 0
狗     -> 1
鱼     -> 2
喜欢   -> 3
微积分 -> 4
```

embedding table 可以看成一个 `V x d` 的矩阵：

```text
E shape = 5 x 4

          dim0   dim1   dim2   dim3
猫      [ 0.80,  0.10,  0.70, -0.20]
狗      [ 0.76,  0.14,  0.66, -0.18]
鱼      [ 0.64, -0.05,  0.62, -0.08]
喜欢    [ 0.10,  0.72,  0.15,  0.40]
微积分  [-0.30,  0.88, -0.42,  0.65]
```

输入 token：

```text
["猫", "喜欢", "鱼"]
```

先变成 token id：

```text
[0, 3, 2]
```

如果写成 one-hot 矩阵 `O`，它的形状是 `n x V`：

```text
O shape = 3 x 5

猫    [1, 0, 0, 0, 0]
喜欢  [0, 0, 0, 1, 0]
鱼    [0, 0, 1, 0, 0]
```

再和 embedding table 相乘：

```text
X = O @ E

X shape = (3 x 5) @ (5 x 4) = 3 x 4
```

结果就是输入矩阵 `X`：

```text
猫    [0.80,  0.10, 0.70, -0.20]
喜欢  [0.10,  0.72, 0.15,  0.40]
鱼    [0.64, -0.05, 0.62, -0.08]
```

这就是 Transformer 后续要处理的输入矩阵。

## 完整 Python 代码

示例脚本见 [examples/01-token-embedding-matrix.py](examples/01-token-embedding-matrix.py)。

```python
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

# 这里的数值只是示例。真实 embedding 是训练出来的可学习参数。
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
```

## 运行输出

```text
tokens: ['猫', '喜欢', '鱼']
token ids: [0, 3, 2]

one_hot_matrix shape: 3 x 5
猫    [ 1.00,  0.00,  0.00,  0.00,  0.00]
喜欢  [ 0.00,  0.00,  0.00,  1.00,  0.00]
鱼    [ 0.00,  0.00,  1.00,  0.00,  0.00]

X = one_hot_matrix @ embedding_table shape: 3 x 4
猫    [ 0.80,  0.10,  0.70, -0.20]
喜欢  [ 0.10,  0.72,  0.15,  0.40]
鱼    [ 0.64, -0.05,  0.62, -0.08]

matrix multiply equals direct lookup: True
```

## 为什么真实模型通常不用显式 one-hot

从数学上看：

```text
X = O @ E
```

其中：

- `O` 是 one-hot 矩阵，形状是 `n x V`。
- `E` 是 embedding table，形状是 `V x d`。
- `X` 是输入向量矩阵，形状是 `n x d`。

但真实模型一般不会真的构造巨大的 one-hot 矩阵。因为 one-hot 里绝大多数都是 0，显式相乘很浪费。

工程实现里通常直接查表：

```text
X = E[token_ids]
```

这和 `one_hot_matrix @ embedding_table` 的结果等价，但更快、更省内存。

## 本节要记住

- token id 是查表索引，不是语义数值。
- embedding table 是 `V x d` 的参数矩阵。
- 一段长度为 `n` 的 token 序列，会变成 `n x d` 的输入矩阵 `X`。
- one-hot 矩阵乘法能解释原理，真实实现通常用 embedding lookup。

下一步可以把这个 `X` 当成 Transformer 的输入，再回到正文理解 [从上下文问题到 Attention](../../00-llm-basics/11-attention-from-context.md) 和 [Transformer 如何一步步形成](../../00-llm-basics/12-transformer-architecture.md)。
