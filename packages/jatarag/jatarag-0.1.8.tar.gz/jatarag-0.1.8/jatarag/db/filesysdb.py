from __future__ import annotations

from pathlib import Path
import numpy as np
from datetime import datetime
from tqdm import tqdm
from pypdf import PdfReader
from fuzzywuzzy import process, fuzz
import re
# import metaphone

from .interface import Database, ParagraphResult, MetadataResult
from jatarag.extractor import Extractor
from jatarag.embedder import Embedder


def tokenize(text: str):
    # Remove non-alphabetic characters and split into tokens
    return re.findall(r'\b\w+\b', text.lower())


class InvertedIndex:
    def __init__(self):
        self.index: dict[str, list[str]] = {}  # map terms to document ids where they appear
        self.unique_terms = None

    def update_unique_terms(self):
        if self.unique_terms is None:
            self.unique_terms = list(self.index.keys())

    def add_document(self, doc_id: str, text):
        terms = tokenize(text)
        for term in terms:
            if term not in self.index:
                self.index[term] = []
            if doc_id not in self.index[term]:
                self.index[term].append(doc_id)
        self.unique_terms = None

    def search(self, query):
        query_terms = tokenize(query)
        doc_ids = set()
        for term in query_terms:
            if term in self.index:
                doc_ids.update(self.index[term])
        return list(doc_ids)

    def fuzzy_search(self, search_term: str, threshold=80) -> list[tuple[str, int]]:
        """
        Find documents that match the search term using fuzzy matching.

        Args:
            search_term: The term to search for.
            threshold: The minimum score for a match to be considered valid.

        Returns:
            A list of tuples containing the document id and the score.
        """
        self.update_unique_terms()

        # Find matches using a scoring threshold
        matches = process.extract(search_term, self.unique_terms, limit=None, scorer=fuzz.token_sort_ratio)
        matches = [(match, score) for match, score in matches if score >= threshold]

        # TODO: better score aggregation
        doc_ids = set()
        scores: dict[str, int] = {}
        for term, score in matches:
            matched_ids = self.index[term]
            doc_ids.update(matched_ids)
            for doc_id in matched_ids:
                scores[doc_id] = max(scores.get(doc_id, 0), score)

        return [(doc_id, scores[doc_id]) for doc_id in doc_ids]


class PhoneticIndex:
    ...  # TODO:...


class FileSystemDB(Database):
    def __init__(self, root: str | Path, extractor: Extractor, embedder: Embedder, cache: bool = True, logdir: str | Path | None = None):

        self.extractor = extractor
        self.embedder = embedder
        self.cache = cache

        self.root = Path(root)

        # set up the logging directory
        if logdir is not None:
            self.logdir = Path(logdir)
        else:
            self.logdir = self.root / 'logs'

        # These all will be set by `collect_documents()`
        self.document_ids = []  # list of file roots in the database
        # self.document_id_to_index = {}          #map from each root name to its index in the database
        self.titles = []  # list of titles for each document
        self.authors = []  # list of authors for each document
        self.title_index = InvertedIndex()  # index for searching by title
        self.author_index = InvertedIndex()  # index for searching by author
        # self.author_phonetics = PhoneticIndex()  #phonetic index for searching by author
        self.embeddings: np.ndarray = None  # single contiguous array of all the embeddings concatenated together
        self.title_embeddings: np.ndarray = None  # single contiguous array of all the title embeddings concatenated together
        # list of lists of paragraphs. each list of paragraphs corresponds to a document
        self.raw_text: list[list[str]] = []
        # map[embedding_idx] -> (document_id, paragraph_idx)
        self.embedding_idx_to_source_idx: list[tuple[str, int]] = []

        # preprocess pdfs into text files
        self.extract_pdf_documents()

        # collect all the documents into a vector space
        self.collect_documents()

        # collect metadata
        self.collect_metadata()

        # # DEBUG
        # ref = self.query_single_document('185', 'Federal Ministry for Economic Cooperation and Development')
        # res = self.query_titles("world energy outlook 2023")
        # # self.query_titles("USAID 2023 Global Water Strategy")
        # pdb.set_trace()
        # ...

    def query_all_documents(self, query: str, max_results: int = 10) -> list[ParagraphResult]:
        """
        Find the top paragraphs in the database that are relevant to the query.

        Args:
            query (str): the query to search for
            max_results (int, optional): the maximum number of results to return. Defaults to 10.

        Returns:
            list[ParagraphResult]: a list of objects containing scores, database root names, and paragraph indices of the top results
        """

        # embed the query
        embedding = self.embedder.embed_paragraphs([query])

        # take the cosine similarity between the query and all the documents
        scores = self.embeddings @ embedding[0]

        # sort the scores and grab the embedding_idx and score of the top results
        top_embedding_idxs = np.argsort(scores)[::-1][:max_results]
        scores = scores[top_embedding_idxs].tolist()

        # convert the raw embedding idx to the corresponding (document_id, paragraph_idx)
        document_ids, paragraph_idxs = zip(*[self.embedding_idx_to_source_idx[idx] for idx in top_embedding_idxs])

        # get the text of the results
        paragraphs = [self.get_document_paragraph(document_id, paragraph_idx)
                      for document_id, paragraph_idx in zip(document_ids, paragraph_idxs)]

        # convert to a list of ParagraphResult objects
        results = [ParagraphResult(*r) for r in zip(document_ids, paragraph_idxs, paragraphs, scores)]

        return results

    def query_single_document(self, document_id: str, query: str, max_results: int = 10) -> list[ParagraphResult]:
        """
        Find the top paragraphs in a single document that are relevant to the query.

        Args:
            document_id (str): the root name of the document to search in
            query (str): the query to search for
            max_results (int, optional): the maximum number of results to return. Defaults to 10.

        Returns:
            list[ParagraphResult]: a list of objects containing scores, database root names, and paragraph indices of the top results
        """

        # determine the range of the embeddings for the document, and grab them
        doc_embedding_idxs = [idx for idx, (doc_id, _) in enumerate(
            self.embedding_idx_to_source_idx) if doc_id == document_id]
        start_idx, stop_idx = doc_embedding_idxs[0], doc_embedding_idxs[-1]+1
        document_embeddings = self.embeddings[start_idx:stop_idx]

        # embed the query
        embedding = self.embedder.embed_paragraphs([query])[0]

        # take the cosine similarity between the query the paragraphs in the document
        scores = document_embeddings @ embedding

        # sort the scores and grab the embedding_idx and score of the top results
        top_embedding_idxs = np.argsort(scores)[::-1][:max_results]
        scores = scores[top_embedding_idxs].tolist()

        # build the results
        document_idx = self.document_id_index[document_id]
        paragraphs = [self.raw_text[document_idx][i] for i in top_embedding_idxs]
        results = [ParagraphResult(document_id, paragraph_idx, paragraph, score)
                   for paragraph_idx, paragraph, score in zip(top_embedding_idxs, paragraphs, scores)]

        return results

    def query_titles(self, query: str, max_results: int = 10) -> list[MetadataResult]:
        """
        Find the top titles in the database that match the query

        Args:
            query (str): the query to search for
            max_results (int, optional): the maximum number of results to return. Defaults to 10.

        Returns:
            list[MetadataResult]: a list of results containing the document metadata of the top results
        """

        # embed the query
        embedding = self.embedder.embed_paragraphs([query])

        # take the cosine similarity between the query and all the documents
        scores = self.title_embeddings @ embedding[0]

        # sort the scores and grab the embedding_idx and score of the top results
        top_embedding_idxs = np.argsort(scores)[::-1][:max_results]
        scores = scores[top_embedding_idxs].tolist()

        # grab the document ids and titles of the top results
        return [MetadataResult(self.document_ids[idx], self.titles[idx], self.authors[idx], 'unknown', scores[i]) for i, idx in enumerate(top_embedding_idxs)]

    def query_authors(self, author: str, max_results: int = 10) -> list[MetadataResult]:
        """
        Find the top authors in the database that match the query

        Args:
            query (str): the query to search for
            max_results (int, optional): the maximum number of results to return. Defaults to 10.

        Returns:
            list[MetadataResult]: a list of results containing the document metadata of the top results
        """

        # since semantic search is unlikely to work on author names, we will use a fuzzy search
        fuzzy_results = self.author_index.fuzzy_search(author)
        results = []
        for doc_id, score in fuzzy_results:
            idx = self.document_id_index[doc_id]
            results.append(MetadataResult(doc_id, self.titles[idx], self.authors[idx], 'unknown', score/100))

        return results

    def query_publishers(self, publisher: str, max_results: int = 10) -> list[MetadataResult]:
        """
        Find the top publishers in the database that match the query

        Args:
            query (str): the query to search for
            max_results (int, optional): the maximum number of results to return. Defaults to 10.

        Returns:
            list[MetadataResult]: a list of results containing the document metadata of the top results
        """
        raise NotImplementedError

    def get_document_title(self, name: str) -> str:
        """get the metadata for a document"""
        return self.titles[self.document_id_index[name]]

    def get_document_author(self, name: str) -> str:
        """get the metadata for a document"""
        return self.authors[self.document_id_index[name]]

    def get_document_paragraphs(self, name: str) -> list[str]:
        """get a list of all paragraphs in a document"""
        paragraphs = self.raw_text[self.document_id_index[name]]
        return paragraphs

    def get_document_text(self, name: str) -> str:
        """get the text of a document"""
        paragraphs = self.get_document_paragraphs(name)
        return '\n\n'.join(paragraphs)

    def get_document_paragraph(self, name: str, idx: int) -> str:
        """get a single paragraph from a document"""
        paragraphs = self.get_document_paragraphs(name)
        return paragraphs[idx]

    def extract_pdf_documents(self):
        """extract text from a list of pdf documents"""
        files = sorted(self.root.glob(f"*pdf"))

        # create the log directory if it doesn't exist
        self.logdir.mkdir(parents=True, exist_ok=True)
        logfilename = f'extract_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log'
        logfilepath = self.logdir / logfilename

        for file in tqdm(files, desc="extracting text from pdfs", miniters=1):

            # check if the file was already extracted
            if self.cache and file.with_suffix(".mmd").exists():
                continue

            # extract text from the pdf with nougat-ocr. capture output in extract.log
            header = f"#################### extracting {file} ######################\n"
            try:
                with open(logfilepath, 'a') as f:
                    f.write(header)
                    f.flush()
                    text = self.extractor.extract_pdf_text(file, log=f)
                    file.with_suffix('.mmd').write_text(text)

            except:
                # grab all the lines from the log file that were added since the header
                with open(logfilepath, 'r') as f:
                    error_lines = f.readlines()
                    error_lines = error_lines[error_lines.index(header)+1:]
                    raise Exception(f"error extracting {file}.\n{''.join(error_lines)}")

    def collect_documents(self):
        """collect all the documents (paragraphs) into the database vector space"""
        # get/save the names of the text documents that will be in the database
        self.document_ids = sorted([*{p.stem for p in self.root.glob(f"*.mmd")}])

        embeddings_list = []

        for document_id in tqdm(self.document_ids, desc="embedding documents as vectors", mininterval=0):
            text_file = self.root / f"{document_id}.mmd"
            embeddings_file = text_file.with_suffix(".npy")
            # check if the file was already embedded
            if self.cache and embeddings_file.exists():
                # grab the cached embeddings
                embeddings = np.load(embeddings_file)
                embeddings_list.append(embeddings)

                # grab the cached text
                text = text_file.read_text()
                paragraphs = self.extractor.convert_to_paragraphs(text)
                self.raw_text.append(paragraphs)
                continue

            assert text_file.exists(), f"file {text_file} has not been extracted yet"

            # get the text from the file, break into paragraphs and save the raw text in memory
            # TODO: allow convert_to_paragraphs to be a function the user passes in
            text = text_file.read_text()
            paragraphs = self.extractor.convert_to_paragraphs(text)
            self.raw_text.append(paragraphs)

            paragraph_embeddings = self.embedder.embed_paragraphs(paragraphs)
            embeddings_list.append(paragraph_embeddings)

            # cache the embeddings on disk
            np.save(embeddings_file, paragraph_embeddings)

        # concatenate all the embeddings into a single matrix
        self.embeddings = np.concatenate(embeddings_list, axis=0)

        # create a mapping from the index of the embedding to the name of the document
        self.embedding_idx_to_source_idx = [(document_id, i) for embeddings, document_id in zip(
            embeddings_list, self.document_ids) for i in range(len(embeddings))]
        self.document_id_index = {name: idx for idx, name in enumerate(self.document_ids)}

        assert len(self.raw_text) == len(embeddings_list), "INTERNAL ERROR: number of raw text and embeddings don't match"
        assert len(self.embedding_idx_to_source_idx) == len(
            self.embeddings), "INTERNAL ERROR: number of embeddings and names don't match"

    def collect_metadata(self):
        """collect metadata for each document"""
        # self.titles = []
        # self.authors = []
        # self.title_index = InvertedIndex()
        # self.author_index = InvertedIndex()

        for document_id in tqdm(self.document_ids, desc="collecting metadata", mininterval=0):
            pdf_file = self.root / f"{document_id}.pdf"
            pdf = PdfReader(pdf_file)
            # TODO: handle if metadata is None
            self.titles.append(pdf.metadata.title or document_id)
            self.authors.append(pdf.metadata.author or "unknown")
            self.title_index.add_document(document_id, pdf.metadata.title or document_id)
            self.author_index.add_document(document_id, pdf.metadata.author or "unknown")
        assert len(self.titles) == len(self.document_ids), "INTERNAL ERROR: number of titles and document ids don't match"
        assert len(self.authors) == len(
            self.document_ids), "INTERNAL ERROR: number of authors and document ids don't match"

        # create title embeddings if they don't exist, or the cached length doesn't match the number of documents
        print("embedding titles")
        title_embeddings_file = self.root / "title_embeddings.npy"
        if title_embeddings_file.exists():
            self.title_embeddings = np.load(title_embeddings_file)

        if self.title_embeddings is None or len(self.title_embeddings) != len(self.document_ids):
            self.title_embeddings = self.embedder.embed_paragraphs(self.titles)
            np.save(title_embeddings_file, self.title_embeddings)

        print("done embedding titles")
