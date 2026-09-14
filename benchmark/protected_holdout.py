"""Sequestered holdout evaluation for the bounded H100 benchmark.

Shard 06541 is stored outside ``prepare.DATA_DIR`` so the upstream tokenizer,
training loader, and pinned validation loader cannot ingest it.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import os
from pathlib import Path

import pyarrow.parquet as pq
import requests
import torch

from prepare import CACHE_DIR, MAX_SEQ_LEN, Tokenizer, get_token_bytes


HOLDOUT_SHARD = 6541
HOLDOUT_FILENAME = f"shard_{HOLDOUT_SHARD:05d}.parquet"
HOLDOUT_URL = (
    "https://huggingface.co/datasets/karpathy/climbmix-400b-shuffle/"
    f"resolve/main/{HOLDOUT_FILENAME}"
)
HOLDOUT_DIR = Path(CACHE_DIR) / "protected_holdout"
HOLDOUT_PATH = HOLDOUT_DIR / HOLDOUT_FILENAME
HOLDOUT_EVAL_TOKENS = 40 * 524288


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_holdout() -> dict[str, object]:
    """Download the predeclared shard once and return its identity record."""
    HOLDOUT_DIR.mkdir(parents=True, exist_ok=True)
    if not HOLDOUT_PATH.exists():
        temporary = HOLDOUT_PATH.with_suffix(".parquet.tmp")
        with requests.get(HOLDOUT_URL, stream=True, timeout=60) as response:
            response.raise_for_status()
            with temporary.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        os.replace(temporary, HOLDOUT_PATH)
    return {
        "shard": HOLDOUT_SHARD,
        "filename": HOLDOUT_FILENAME,
        "url": HOLDOUT_URL,
        "path": str(HOLDOUT_PATH),
        "size_bytes": HOLDOUT_PATH.stat().st_size,
        "sha256": sha256_file(HOLDOUT_PATH),
        "eval_tokens": HOLDOUT_EVAL_TOKENS,
    }


def _document_batches(tokenizer_batch_size: int = 128):
    if not HOLDOUT_PATH.exists():
        raise FileNotFoundError("Protected holdout is absent; run with --prepare first")
    epoch = 1
    while True:
        parquet = pq.ParquetFile(HOLDOUT_PATH)
        for row_group in range(parquet.num_row_groups):
            texts = parquet.read_row_group(row_group).column("text").to_pylist()
            for index in range(0, len(texts), tokenizer_batch_size):
                yield texts[index:index + tokenizer_batch_size], epoch
        epoch += 1


def make_holdout_dataloader(tokenizer: Tokenizer, batch_size: int, sequence_len: int,
                            buffer_size: int = 1000):
    """Mirror upstream best-fit packing while reading only the holdout shard."""
    row_capacity = sequence_len + 1
    batches = _document_batches()
    bos_token = tokenizer.get_bos_token_id()
    documents: list[list[int]] = []

    def refill() -> None:
        texts, _ = next(batches)
        documents.extend(tokenizer.encode(texts, prepend=bos_token))

    row_buffer = torch.empty((batch_size, row_capacity), dtype=torch.long)
    cpu_buffer = torch.empty(2 * batch_size * sequence_len, dtype=torch.long, pin_memory=True)
    gpu_buffer = torch.empty(2 * batch_size * sequence_len, dtype=torch.long, device="cuda")
    cpu_inputs = cpu_buffer[:batch_size * sequence_len].view(batch_size, sequence_len)
    cpu_targets = cpu_buffer[batch_size * sequence_len:].view(batch_size, sequence_len)
    inputs = gpu_buffer[:batch_size * sequence_len].view(batch_size, sequence_len)
    targets = gpu_buffer[batch_size * sequence_len:].view(batch_size, sequence_len)

    while True:
        for row_index in range(batch_size):
            position = 0
            while position < row_capacity:
                while len(documents) < buffer_size:
                    refill()
                remaining = row_capacity - position
                best_index = -1
                best_length = 0
                for index, document in enumerate(documents):
                    length = len(document)
                    if length <= remaining and length > best_length:
                        best_index = index
                        best_length = length
                if best_index >= 0:
                    document = documents.pop(best_index)
                    row_buffer[row_index, position:position + len(document)] = torch.tensor(document)
                    position += len(document)
                else:
                    shortest = min(range(len(documents)), key=lambda i: len(documents[i]))
                    document = documents.pop(shortest)
                    row_buffer[row_index, position:position + remaining] = torch.tensor(document[:remaining])
                    position += remaining
        cpu_inputs.copy_(row_buffer[:, :-1])
        cpu_targets.copy_(row_buffer[:, 1:])
        gpu_buffer.copy_(cpu_buffer, non_blocking=True)
        yield inputs, targets


@torch.no_grad()
def evaluate_protected_bpb(model, tokenizer: Tokenizer, batch_size: int) -> float:
    """Evaluate BPB on the sequestered shard using the upstream formula."""
    token_bytes = get_token_bytes(device="cuda")
    loader = make_holdout_dataloader(tokenizer, batch_size, MAX_SEQ_LEN)
    steps = HOLDOUT_EVAL_TOKENS // (batch_size * MAX_SEQ_LEN)
    total_nats = 0.0
    total_bytes = 0
    for _ in range(steps):
        inputs, targets = next(loader)
        flat_loss = model(inputs, targets, reduction="none").view(-1)
        flat_targets = targets.view(-1)
        byte_lengths = token_bytes[flat_targets]
        mask = byte_lengths > 0
        total_nats += (flat_loss * mask).sum().item()
        total_bytes += byte_lengths.sum().item()
    return total_nats / (math.log(2) * total_bytes)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the sequestered holdout shard")
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    if not args.prepare:
        parser.error("--prepare is required when running this module directly")
    import json
    print(json.dumps(prepare_holdout(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
