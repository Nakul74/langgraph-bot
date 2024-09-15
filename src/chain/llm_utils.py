from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def get_prompt_tamplate(system_prompt,system_prompt_variables,human_prompt,human_prompt_variables):
    system_prompt = PromptTemplate(input_variables = system_prompt_variables, template=system_prompt)
    system_message_prompt = SystemMessagePromptTemplate(prompt=system_prompt)

    human_prompt = PromptTemplate(input_variables=human_prompt_variables,template=human_prompt)
    human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
    return chat_prompt

def create_chain(system_prompt,system_prompt_variables,human_prompt,human_prompt_variables,structured_llm):
    chat_prompt = get_prompt_tamplate(system_prompt,system_prompt_variables,human_prompt,human_prompt_variables)
    chain = chat_prompt | structured_llm
    return chain