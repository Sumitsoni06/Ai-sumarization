from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

client = genai.Client()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    user_text = request.form.get('text_to_summarize')
    length_choice = request.form.get('summary_length') # Catches 'short', 'medium', or 'long'
    
    if not user_text:
        return render_template('index.html', summary="Please enter some text to summarize.")

    # Dynamically change the AI instructions based on what the user picked
    if length_choice == "short":
        prompt_instruction = "Please provide an extremely concise, punchy summary of the following text in exactly 3 bullet points:"
    elif length_choice == "long":
        prompt_instruction = "Please provide a thorough, detailed multi-paragraph summary exploring all major points of the following text:"
    else:
        prompt_instruction = "Please provide a standard, clear, bulleted summary highlighting the core concepts of the following text:"

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{prompt_instruction}\n\n{user_text}",
        )
        ai_summary = response.text
        
    except Exception as e:
        ai_summary = f"Error generating summary: {str(e)}"

    return render_template('index.html', summary=ai_summary)

if __name__ == '__main__':
    app.run(debug=True)