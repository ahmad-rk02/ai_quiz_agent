import json


def create_html(mcqs):
    if (not mcqs) or (isinstance(mcqs[0], dict) and "error" in mcqs[0]):
        return "<html><body><h1>Error: No MCQs generated.</h1></body></html>"

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Quiz</title>

<style>
/* RESET */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

/* PAGE BACKGROUND */
body {{
    font-family: "Segoe UI", sans-serif;
    background: linear-gradient(135deg, #e8eef7 0%, #f9fbff 100%);
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

/* TITLE */
h1 {{
    font-size: clamp(26px, 5vw, 40px);
    margin-bottom: 20px;
    color: #1e2a78;
    font-weight: 700;
    animation: fadeIn 0.8s ease-out;
}}

/* ANIMATION */
@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

/* CONTAINER */
.quiz-container {{
    width: 100%;
    max-width: 900px;
    background: rgba(255, 255, 255, 0.65);
    padding: 30px;
    border-radius: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.12);
    backdrop-filter: blur(12px);
    animation: fadeIn 0.7s ease-out;
}}

/* EACH QUESTION CARD */
.question-box {{
    margin-bottom: 28px;
    padding: 22px;
    background: #fff;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transition: 0.3s ease;
}}

.question-box:hover {{
    transform: translateY(-2px);
}}

p {{
    font-size: 18px;
    margin-bottom: 14px;
    color: #111;
}}

/* OPTIONS */
label {{
    display: flex;
    align-items: center;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    background: #f0f3ff;
    cursor: pointer;
    transition: all 0.2s ease;
}}

label:hover {{
    background: #dfe6ff;
}}

input[type="radio"] {{
    margin-right: 12px;
    transform: scale(1.2);
}}

/* BUTTON */
button {{
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: #1e2a78;
    color: white;
    font-size: 18px;
    cursor: pointer;
    margin-top: 20px;
    transition: 0.3s ease;
}}

button:hover {{
    background: #16205a;
    transform: translateY(-2px);
}}

/* RESULTS */
.result-box {{
    padding: 14px;
    margin-top: 10px;
    background: #eef2ff;
    border-radius: 12px;
}}

footer {{
    margin-top: 20px;
    font-size: 13px;
    color: #555;
}}
</style>
</head>

<body>

<h1>AI Quiz</h1>

<div class="quiz-container">
<form id="quizForm">
"""

    # ADD ALL QUESTIONS AT ONCE
    for i, mcq in enumerate(mcqs):
        options_html = "".join(
            f'<label><input type="radio" name="q{i}" value="{chr(65+j)}"> {opt}</label>'
            for j, opt in enumerate(mcq["options"])
        )

        html += f"""
        <div class="question-box">
            <p><strong>Question {i+1}:</strong> {mcq['question']}</p>
            {options_html}
        </div>
        """

    # SUBMIT BUTTON
    html += (
        """
<button type="button" onclick="submitQuiz()">Submit Quiz</button>
</form>
</div>

<script>
const mcqs = """
        + json.dumps(mcqs)
        + """;

function submitQuiz() {
    let score = 0;
    let answers = [];

    mcqs.forEach((q, i) => {
        const selected = document.querySelector(`input[name="q${i}"]:checked`);
        let ans = selected ? selected.value : null;
        answers.push(ans);
        if (ans === q.correct) score++;
    });

    let html = `
        <h2 style='text-align:center; color:#1e2a78;'>Quiz Completed</h2>
        <h3 style='text-align:center; margin-bottom:20px;'>Score: <b>${score}/${mcqs.length}</b></h3>
        <h3>Detailed Report</h3><hr><br>
    `;

    mcqs.forEach((q, i) => {
        html += `
            <div class='result-box'>
                <p><b>Q${i+1}: ${q.question}</b></p>
                <p>Your Answer: <b>${answers[i] || "Not Answered"}</b></p>
                <p>Correct Answer: <b style='color:green;'>${q.correct}</b></p>
            </div>
        `;
    });

    html += `<button onclick="goHome()">Return Home</button>`;

    document.querySelector(".quiz-container").innerHTML = html;
}

function goHome() {
    window.location.href = "/";
}
</script>

<footer>Created by <b>Ahmad Raza Khan</b> — AI Quiz 2025</footer>

</body>
</html>
"""
    )

    return html
