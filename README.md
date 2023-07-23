# QnAChatBot

### [Live Demo](https://qnachatbotgit-wt3gsf18sv.streamlit.app/)

QnAChatBot allows you to upload text heavy pdf documents, and chat with the bot based on the document.

## Use Cases
1. Company financials, and earnings call analyzer.
2. Ask questions about a Terms and Services document to uncover what you're legally signing up for.
3. Write cover letters based on resumes.
4. Ask questions on course work, lab materials, or any educational document

### Use Case Demo

1. Company Financials
![gif of company financials](https://afi225-learning-bucket.s3.amazonaws.com/embeddings_pdf_docs/earnings.gif)

1. Resume to Cover Letter
![gif of resume to cover letter](https://afi225-learning-bucket.s3.amazonaws.com/embeddings_pdf_docs/resume.gif)

## Prior Work

This work is inspired from my HackNYU Hackathon project, [GPT Tutor](https://devpost.com/software/tutor-bot). We built a Discord Bot that is able
to synthesize course material uploaded by a professor, and serve as a 24/7 available teacher's assistant. The success of the work enables us to expand beyond
just coursework, and extend it to a wider usecase. 

## To Reproduce (On MacOS)

1. Clone this repository
```bash
git clone https://github.com/farhan0167/QnAChatBot
cd QnAChatBot
```

2. Configure OpenAI API key and secrets folder
```bash
mkdir .streamlit
cd .streamlit
nano secrets.toml
```
and paste the following:
```
OPENAI_API_KEY = "your-openAI-api-key"
```
Press `Control+X` and `Y` to exit the editor. Go back to project directory:

3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the Application
```bash
streamlit run app.py
```