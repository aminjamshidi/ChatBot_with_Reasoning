from fastapi import FastAPI
from fastapi.responses import JSONResponse
from Agent.input_processor import classify_query
from Agent.LLM import LLM_call
from Agent.response_logic_checking import (
    cross_checking_factual_questions,
    rhyme_checking_poem,
)

app = FastAPI()


@app.post("/agent/")
async def agent(query: str):
    # classify query
    query_class = classify_query(query=query)
    # get output of LLM
    ans = LLM_call(query=query, type=query_class)

    # check output of the LLM
    # if it is Factual Question
    if query_class == "Factual Question":
        flag, check_answer = cross_checking_factual_questions(query, ans.KeyAnswer)
        if flag:
            output = "{}, \n reasoning:that is checked on the internet".format(
                ans.KeyAnswer
            )
        else:
            output = "{},\n reasoning: incompatible!!! ,resulte of searching the internet is {} ".format(
                ans.KeyAnswer, check_answer
            )
    # for Creative Task , we have reasoning only for poem creation
    elif query_class == "Creative Task":
        if "poem" in query:
            poem = LLM_call(query, "poem Task")
            poem_list = [
                stanza.replace("\n", "").replace(",", "").replace(".", "")
                for stanza in poem.stanzaList
            ]
            flag = rhyme_checking_poem(poem_list)
            final_poem = []
            for i, stanza in enumerate(poem_list):
                if i % 2 == 0:
                    final_poem.append(stanza + "\n")
                else:
                    final_poem.append(stanza + " , ")
            final_poem = "".join(final_poem)
            if flag:
                output = "{} \n reasoning: each 2 consecutive stanzas of the poem have a same rhyme".format(
                    final_poem
                )
            else:
                output = "{} \n reasoning: each 2 consecutive stanzas of the poem does not  have a same rhyme".format(
                    final_poem
                )
        else:
            other = LLM_call(query, "other")
            output = "{} \n reasoning: does not suport reasoning".format(other)

    return JSONResponse({"output": output})
