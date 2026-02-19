import openai

def negotiate(case_details):
    prompt=f"""
    Act as professional legal mediator.
    Provide negotiation steps, solutions and score settlement probability.

    Case:
    {case_details}
    """

    res=openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res['choices'][0]['message']['content']
