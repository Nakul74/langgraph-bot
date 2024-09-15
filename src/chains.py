from src.chain import query_resolver_chain, hallucination_chain
from src import models

query_resolver_llm_chain = query_resolver_chain.get_query_resolver_chain(models.openai_llm)
hallucination_llm_chain = hallucination_chain.get_hallucination_chain(models.openai_llm)