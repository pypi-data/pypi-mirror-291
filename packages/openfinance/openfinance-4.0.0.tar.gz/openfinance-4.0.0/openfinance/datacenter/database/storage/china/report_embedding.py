from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import SpacyTextSplitter
import sys
import asyncio
# sys.path.append("/Users/july/Desktop/openfinance")
from openfinance.datacenter.database.source.eastmoney.news import get_eastmoney_report
from openfinance.datacenter.database.source.eastmoney.util import report_summary
from openfinance.utils.recall.manager import IndexManager
from openfinance.utils.embeddings.embedding_manager import EmbeddingManager
from openfinance.utils.recall.faiss import Faiss
from openfinance.config import Config
from openfinance.agentflow.llm.manager import ModelManager

import pandas as pd
import re

CHUNK_SIZE = 64
OVERLAP_SIZE = 10

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=CHUNK_SIZE,
#     chunk_overlap=OVERLAP_SIZE,
#     separators=[
#         "\n\n",
#         "\n",
#         "。|！|？",
#         "\.\s|\!\s|\?\s",
#         "；|;\s",
#         "，|,\s"
#     ]
# )
# text_splitter = SpacyTextSplitter(pipeline="zh_core_web_sm", chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP_SIZE)


class Chunkizer():
    def __init__(self, chunk_size, overlap_size):
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        # self.text_splitter = RecursiveCharacterTextSplitter(
        #                         chunk_size=CHUNK_SIZE,
        #                         chunk_overlap=OVERLAP_SIZE,
        #                         separators=[
        #                             "\n\n",
        #                             "\n",
        #                             "。|！|？",
        #                             "\.\s|\!\s|\?\s",
        #                             "；|;\s",
        #                             "，|,\s"
        #                         ]
        #                     )
        '''
        pip install spacy
        python -m spacy download zh_core_web_sm
        '''
        self.text_splitter = SpacyTextSplitter(
            pipeline="zh_core_web_sm", chunk_size=CHUNK_SIZE, chunk_overlap=OVERLAP_SIZE)

    def do_chunk(self, text):
        pattern = r'(?<=\d)\.(?=\d)'  # 小数点会被切，这里统一替换
        formated_text = re.sub(pattern, '@mark@', data.CONTENT[0])
        chunks = self.text_splitter.split_text(formated_text)
        chunks = [x.replace("@mark@", ".") for x in chunks]
        # token计数可以用gpt的切词来做，先简单len(text)代替
        token_size = len(text)
        # text短，llm能接受，召回的text就直接是全文
        if token_size < 4096:
            return [[chunk, text] for i, chunk in enumerate(chunks)]
        else:  # 否则截取chunk的前后n个chunk扩大文本范围
            return [[chunk, ' '.join(chunks[max([0, i-10]), min([len(chunks), i+10])])] for i, chunk in enumerate(chunks)]


def create_db(data_obj, index_name, folder_path):
    my_chunkizer = Chunkizer(chunk_size=50, overlap_size=5)

    docs = dict()
    if isinstance(data_obj, pd.DataFrame):
        # data table ["STOCK_CODE", "STOCK_NAME", "RATING", "TITLE", "CONTENT", "PDF_LINK", "DATE", "QTYPE"]
        for index, row in data_obj.iterrows():
            # 需要使用title code等对key做增强  todo
            chunks = my_chunkizer.do_chunk(row["CONTENT"])
            for chunk in chunks:
                docs[chunk[0]] = {"title": row["TITLE"], "stock_code": row["STOCK_CODE"], "stock_name": row["STOCK_NAME"],
                                  "content": chunk[1], "rating": row["RATING"], "pdf_link": row["PDF_LINK"], "source": "eastmoney_report"}

    elif isinstance(data_obj, str):
        data_suffix = data_obj.split(".")[-1]

        if data_suffix == "pdf":
            from pypdf2 import PdfReader
            pdf_item = PdfReader(data_obj)
            pdf_content = ""
            for page in pdf_item.pages:
                pdf_content += page.extract_text()

            chunks = my_chunkizer.do_chunk(pdf_content)
            for chunk in chunks:
                docs[chunk[0]] = {"title": "", "stock_code": "", "stock_name": "",
                                  "content": chunk[1], "rating": "", "pdf_link": data_obj, "source": "upload_pdf"}
    else:
        raise ValueError(
            "data_obj should be a pandas DataFrame or a path to a pdf file")

    db = Faiss.from_embedding(
        inputs=docs,
        embedding=EmbeddingManager.get_embedding(
            {"faiss": {"embedding": "cn"}}
        )
    )

    db.save(folder_path, index_name)
    return 0


if __name__ == "__main__":
    import pandas as pd
    config = Config()
    model_manager = ModelManager(config=config)
    llm = model_manager.get_model("chatgpt")
    data = get_eastmoney_report(1, 1, 20)
    print(report_summary(data.CONTENT[0], llm))
    exit(-1)
    info = create_db(
        data, "news_test", "/Users/july/Desktop/openfinance/openfinance/datacenter/database/storage/china/test_data")
    db = Faiss.load(EmbeddingManager.get_embedding({"faiss": {
                    "embedding": "cn"}}), "/Users/july/Desktop/openfinance/openfinance/datacenter/database/storage/china/test_data", "news_test")
    res = db.similarity_search("中国", 2)
    print(res)
