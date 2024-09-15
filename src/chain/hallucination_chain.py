from src.chain import llm_utils, prompt, pydantic_class

def get_hallucination_chain(chat_llm):
    structured_llm = chat_llm.with_structured_output(pydantic_class.Hallucination)
    system_prompt = prompt.hallucination_system_prompt
    system_prompt_variables = []

    human_prompt = ''
    human_prompt += "\n<<Facts>>:\n{documents}\n"
    human_prompt += '\n' + '###' * 30
    human_prompt += "\n<<Answer>>:\n{answer}\n"
    human_prompt_variables = ['documents','answer']

    chain = llm_utils.create_chain(system_prompt,system_prompt_variables,human_prompt,human_prompt_variables,structured_llm)
    return chain
