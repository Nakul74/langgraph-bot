from src.chain import llm_utils, prompt, pydantic_class

def get_query_resolver_chain(chat_llm):
    structured_llm = chat_llm.with_structured_output(pydantic_class.QueryResolver)
    system_prompt = prompt.query_resolver_system_prompt
    system_prompt_variables = []

    human_prompt = ''
    human_prompt += "\n<<User query>>:\n{query}\n"
    human_prompt += '\n' + '###' * 30
    human_prompt += "\n<<Context>>:\n{context}\n"
    human_prompt_variables = ['query','context']

    chain = llm_utils.create_chain(system_prompt,system_prompt_variables,human_prompt,human_prompt_variables,structured_llm)
    return chain
