import openai
import streamlit as st
openai.api_key = st.secrets["openai_key"]


def prompt_engineering(university: str, course: str, course_name: str, lecture_number: str,
                      lecture_title: str, part: int, chunk: str) -> str:

    """Generate summary with OpenAI API given a chunk of text.

    Args:
        university (str): Name of the university
        course (str): Course code
        course_name (str): The course's full name
        lecture_number (str): The lecture number or week of the lecture
        lecture_title (str): The title of the lecture
        part (int): Part of the transcript. If given 0, it will include `first chunk` in the prompt.
        chunk (str): Chunk of the trnascript.

    Returns:
        str: Summarized transcript provided by the API.
    """

    prompt = f'''You are a perfectly articulate and knowledgable chatbot that turns lectures from
    {university}'s {course} {course_name} class into detailed notes for students to learn from. 
    You are currently summarizing Lecture {lecture_number}: {lecture_title}.
    Here is the transcript of the for the {'first' if part == 0 else 'next'} chunk of the lecture:
    
    {chunk}
    
    Please convert this speech into notes. 
    Speak in 3rd person, use bullet points only, and only include relevant information on the topic of 
    this class: {lecture_title}.'''

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.75,
        max_tokens=256,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    response_text = response.choices[0].text

    return response_text


if __name__ == '__main__':
    with open('/workspaces/codespace/MH1811 Lecture 1 part 1 [u0T4iu_2PZA].en.txt','r',
              encoding='utf-8') as file:
        transcript_lines = file.readlines()
    num_lines = len(transcript_lines)

    COURSE = 'MH1811'
    CNAME = 'Mathematics 2'
    UNI = 'National Technological University Singapore'
    LNUM = '1'
    LTITLE = 'Single Variable Calculus'

    print(f'#### {COURSE} Lecture {LNUM}: {LTITLE}', end='')

    for parts in range(int(num_lines/30)+1):
        current_chunk = "".join(transcript_lines[parts*30:parts*30+30])
        print(prompt_engineering(UNI,COURSE,CNAME,LNUM,LTITLE,parts,current_chunk))