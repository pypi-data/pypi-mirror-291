from openfinance.utils.embeddings.sentence_transformers import RemoteEmbeddings
from openfinance.utils.embeddings.sentence_transformers_cn import ChineseEmbeddings
# from openfinance.utils.embeddings.huggingface_embedding import HuggingFaceHubEmbeddings
# from openfinance.utils.embeddings.openai_embedding import OpenAIEmbeddings

EMDEDDINGS = {
    "remote" : RemoteEmbeddings,
    "cn" : ChineseEmbeddings,
    # "huggingface" : HuggingFaceHubEmbeddings,
    # "openai" : OpenAIEmbeddings
}
