import openai
import streamlit as st
from PyPDF2 import PdfReader
from brain import Brain
import pandas as pd

#Init
openai.api_key = st.secrets["OPENAI_API_KEY"]
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

#maintain two session states. One to capture user prompt
#another to capture user prompt+relevant context for the model
#we only display messages state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "messages_context" not in st.session_state:
    st.session_state.messages_context = []

@st.cache_resource
def load_model():
    return Brain()
model = load_model()

@st.cache_data
def load_data(doc_name, _model):
    # creating a pdf reader object
    reader = PdfReader(doc_name)

    # Create lists to store data for each paragraph
    title = []
    heading = []
    content = []
    tokens = []

    # Function to count words in a paragraph
    def count_words(paragraph):
        return len(paragraph.split())

    # Extract data and populate the lists
    for page in range(len(reader.pages)):
        page_content = reader.pages[page].extract_text().split("\n\n")
        for paragraph_num, paragraph in enumerate(page_content):
            title.append(doc_name.name)
            heading.append(f'Page {page + 1}, Paragraph {paragraph_num}')
            content.append(paragraph)
            tokens.append(count_words(paragraph))

    # Create a dictionary to store the data
    data = {
        'title': title,
        'heading': heading,
        'content': content,
        'tokens': tokens
    }

    # Create the pandas DataFrame
    df = pd.DataFrame(data)
    document_embeddings = _model.compute_doc_embeddings(df)

    return df, document_embeddings


#Main App Below:

st.title("Q/A Bot")
st.write("Upload a document and ask GPT about the document.")

uploaded_file = st.file_uploader('Choose your .pdf file', type="pdf")
if uploaded_file:
    #UploadedFile(id=1, name='Resume for lawyer.pdf', type='application/pdf', size=58651)
    df, document_embeddings = load_data(uploaded_file, model)


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Send a message"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        prompt = model.construct_prompt(
            question=prompt,
            context_embeddings=document_embeddings,
            df=df
        )
        st.session_state.messages_context.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        messages = []
        for i in range(len(st.session_state.messages_context)):
            if st.session_state.messages_context[i]["role"] == "user":
                if i == len(st.session_state.messages_context)-1:
                    messages.append(st.session_state.messages_context[i])
                #we don't want to supply the context prompt to the chat history
                else:
                    messages.append(st.session_state.messages[i])   
            else:
                messages.append(st.session_state.messages_context[i])

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=messages,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.messages_context.append({"role": "assistant", "content": full_response})