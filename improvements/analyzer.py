import openai

def analyze_usage(data):
    prompt=f"""
    Analyse legal practice workflow.
    Suggest improvements, automation and efficiency tips.

    Data:
    {data}
    """

    res=openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return res['choices'][0]['message']['content']
