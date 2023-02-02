import streamlit as st
import base64

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

    


def set_page_container_style(
        padding_top=1
    ):
        st.markdown(
            f'''
            <style>
                .appview-container .main .block-container{{
                padding-top: {padding_top}rem;    }}
                .uploadedFile {{display: none}}
                header {{visibility: hidden;}}
                footer {{visibility: hidden;}}
            </style>
            ''',
            unsafe_allow_html=True,
        )


# Remove white lines in html
def revise_pyvis_html(html):
    f = open(html, 'r')
    copy_text = ''
    lines = f.readlines()
    for line in lines:
        if '<style type="text/css">' in line:
            copy_text += line
            copy_text += 'body {background-color: #111111;}\n'
        elif 'div class="card" style="width: 100%' in line:
            copy_text += '        <div class="card" style="width: 100%; border:#111111">\n'
        elif '<div id="mynetwork" class="card-body"' in line:
            copy_text += '            <div id="mynetwork" class="card-body" style="width: 100%; border:#111111"></div>\n'
        else:
            copy_text += line
    f.close()
    f = open(html, 'w')
    f.write(copy_text)