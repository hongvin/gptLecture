import streamlit as st
import base64
from streamlit_extras.stateful_button import button
from md2pdf.core import md2pdf
from get_youtube_video import get_youtube_videos, read_youtube_data
from vtt_processor import process_vtt
from prompt_engineering import prompt_engineering

def show_pdf(file_path):
    with open(file_path,"rb") as f:
          base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.title('Summarize your recorded lectures!')
st.markdown('Harnessing the power of GPT to provide you the gist of the recorded lectures!')

#summarize_button = None

youtube_link = str(st.text_input('Enter a Youtube link','https://www.youtube.com/watch?v=u0T4iu_2PZA'))
submit_video_bttn = button('Get the video',key="button1")


if submit_video_bttn:
    try:
        with st.spinner('Downloading...'):
            get_youtube_videos(youtube_link)
            st.markdown(f'Video Title: **{read_youtube_data("video.info.json")}**')
            process_vtt("video.en.vtt")
            st.markdown('---')
            st.markdown('Before proceeding, I would need some extra info to get more accurate summary from the video!')
            university = str(st.text_input('University Name', 'National Technological University Singapore'))

            col1, col2 = st.columns(2)

            with col1:
                course_code = str(st.text_input('Course Code','MH1811'))
                course_name = str(st.text_input('Course Name','Mathematics 2'))
            
            with col2:
                lecture_num = str(st.text_input('Lecture Number','1'))
                lecture_name = str(st.text_input('Lecture Title','Single Variable Calculus'))
            
            summarize_button = button('Get a summarized note now!',key="button2")
            st.markdown('---')

            if ((st.session_state['button1']) and summarize_button):
                st.markdown('##### Your summarized notes from video')
                with open('video.en.txt','r',encoding='utf-8') as file:
                    transcript_lines = file.readlines()
                num_lines = len(transcript_lines)


                strings = ''
                titles =f'#### {course_code} Lecture {lecture_num}: {lecture_name}'
                strings+=titles

                st.markdown(titles)
                for parts in range(int(num_lines/30)+1):
                    current_chunk = "".join(transcript_lines[parts*30:parts*30+30])
                    current_summary = prompt_engineering(university,course_code,course_name,lecture_num,lecture_name,parts,current_chunk)
                    strings+=current_summary
                    st.markdown(current_summary)
                

                st.markdown('Download the note in PDF!')
                md2pdf('note.pdf',md_content=strings)
                #show_pdf('note.pdf')
                st.download_button(label="Download PDF Note!", 
                                    data=PDFbyte,
                                    file_name="note.pdf",
                                    mime='application/octet-stream')

    except Exception as e:
        st.error(f'Error: {e}',icon="🚨")
