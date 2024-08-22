from __future__ import annotations

from pathlib import Path
import argparse
from easyrepl import REPL

from .db import FileSystemDB
from .extractor import NougatExtractor
from .embedder import AdaEmbedder
from .agent import OpenAIAgent
from .librarian import MultihopRagAgent
from .utils import set_openai_key


# debugging
from .utils import pdb_excepthook
import sys
sys.excepthook = pdb_excepthook


def streaming_demo(path: Path, cache: bool, batch_size: int, api_key: str | None):
    set_openai_key(api_key)
    logdir = Path(__file__).parent.parent / 'logs'

    extractor = NougatExtractor(batch_size=batch_size)
    embedder = AdaEmbedder()
    agent = OpenAIAgent(model='gpt-4o')
    db = FileSystemDB(path, extractor=extractor, embedder=embedder, cache=cache, logdir=logdir)

    librarian = MultihopRagAgent(db, agent)

    print('Ask a question about the documents in the database.')
    for query in REPL(history_file='history.txt'):
        results, answer_gen = librarian.ask(query, stream=True)

        # print the semantic search paragraph results
        print('Results:\n', '\n\n'.join(
            [f'[{i}]({result.document_id}.mmd ¶ {result.paragraph_idx}): {result.paragraph}' for i, result in enumerate(results)]))

        # stream print the answer
        print(f'\nAnswer: ', end='')
        for token in answer_gen:
            print(token, end='', flush=True)
        print()


if __name__ == "__main__":
    # handle command line arguments
    parser = argparse.ArgumentParser(description="extract and embed files in a specified directory.")
    parser.add_argument("directory", help="Path to the directory containing pdf files files")
    parser.add_argument("--no_cache", '-n', action="store_true", help="recompute cached files",
                        default=False)  # TODO:separate .mmd cache from .npy cache
    parser.add_argument("--batch_size", '-b', type=int, default=4, help="Batch size for OCR")
    parser.add_argument("--api_key", '-k', type=str, default=None,
                        help="OpenAI API key. If not set, uses OPENAI_API_KEY environment variable.")
    args = parser.parse_args()

    path = Path(args.directory)
    cache = not args.no_cache
    batch_size = args.batch_size
    api_key = args.api_key

    # run the demo
    streaming_demo(path, cache, batch_size, api_key)
