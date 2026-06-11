from flask import Flask, render_template, request
import os
from pdf import process_pdf, retrieve_chunks, chat_agent, chat_with_pdf

app = Flask(__name__)

os.makedirs("uploads",exist_ok=True)

chunks=None
chunk_embeddings=None
pdf_summary=None
history=[]

@app.route("/",methods=["GET","POST"])
def home():
    global chunks
    global chunk_embeddings
    global pdf_summary
    global history
    
    answer=""
    if request.method=="POST":
        if "pdf_file" in request.files:
            pdf_file=request.files["pdf_file"]
            if pdf_file.filename!="":
                password=request.form.get("password","")
                pdf_path=os.path.join("uploads",pdf_file.filename)
                pdf_file.save(pdf_path)

                try:
                    _,chunks,chunk_embeddings,pdf_summary=process_pdf(pdf_path,password)
                    answer="pdf uploaded succesfully"
                    history = []  # Reset history for new PDF
                except Exception as e:
                    answer=str(e)    

        question=request.form.get("question")            
        if question and chunks is not None and chunk_embeddings is not None:
            # Check if user wants to exit
            if question.lower() in ["exit", "quit"]:
                answer = "Chat session ended. Upload a new PDF to start again."
                chunks = None
                chunk_embeddings = None
                pdf_summary = None
                history = []
            else:
                answer, history = chat_with_pdf(question, chunks, chunk_embeddings, pdf_summary, history)
    
    return render_template("index.html", answer=answer, history=history)

if __name__ == "__main__":
    app.run(debug=True)





