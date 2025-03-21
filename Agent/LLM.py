from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from Agent.utils import answer, stanzaList

load_dotenv()

# use gemini for LLM
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
)

# prompt and parser for factual question
answer_parser = PydanticOutputParser(pydantic_object=answer)
factual_question_prompt = PromptTemplate.from_template(
    template="You should answer the factual question: {query} and give the answer of the question in the fomat  \n\n {key_answer} \n\n  give only answer as key answer and give no description",
    partial_variables={"key_answer": answer_parser.get_format_instructions()},
)


# prompt and parser for poem creation
stanza_parser = PydanticOutputParser(pydantic_object=stanzaList)
poem_prompt = PromptTemplate.from_template(
    template="{query} and consider each 2 consecutive stanzas of the poem have a same rhyme and separate each stanza with ',' and I want to each stanza of the poam as item of list in the format \n\n {stanza_List} \n\n  and the poem should not be long ",
    partial_variables={"stanza_List": stanza_parser.get_format_instructions()},
)


def LLM_call(query, type):
    if type == "Factual Question":
        prompt = factual_question_prompt.invoke({"query": query})
        ans = model.invoke(prompt)
        ans = answer_parser.parse(ans.content)
    if type == "poem Task":
        prompt = poem_prompt.invoke({"query": query})
        ans = model.invoke(prompt)
        ans = stanza_parser.parse(ans.content)
    else:
        ans = model.invoke(query)

    return ans
