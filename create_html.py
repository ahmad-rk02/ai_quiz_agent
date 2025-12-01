import json


def create_html(mcqs):
    """
    Generates an interactive HTML quiz string from a list of MCQs.
    Works both locally and on Render (no file writing).
    """

    if not mcqs or ("error" in mcqs[0] if isinstance(mcqs[0], dict) else False):
        return "<html><body><h1>Error: No MCQs generated.</h1></body></html>"

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Quiz</title>
    <style>
        body {{
    font-family: 'Segoe UI', sans-serif;
    padding: 20px;
    background: linear-gradient(135deg, #e3ecff, #f5f7fa);
    min-height: 100dvh;    /* FIX */
    display: block;        /* FIX */
    animation: fadeIn 1s ease-in-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        h1 {{
            text-align: center;
            color: #2a2a72;
            margin-bottom: 20px;
        }}

        .quiz-container {{
            width: 100%;
            max-width: 600px;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}

        .question-box {{
            display: none;
            margin-bottom: 20px;
        }}

        .question-box.active {{
            display: block;
        }}

        label {{
            display: block;
            padding: 12px;
            border-radius: 10px;
            margin: 8px 0;
            background: #eef1f7;
            cursor: pointer;
        }}

        button {{
            width: 100%;
            padding: 15px;
            font-size: 18px;
            border: none;
            background: #2a2a72;
            color: white;
            border-radius: 10px;
            cursor: pointer;
            margin-top: 20px;
        }}

        .progress-bar {{
            height: 15px;
            background: #eef1f7;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
        }}

        .progress-bar-fill {{
            height: 100%;
            width: 0%;
            background: #2a2a72;
            transition: width 0.5s ease;
        }}
    </style>
</head>

<body>

<h1>AI Quiz</h1>

<div class="quiz-container">
    <div class="progress-bar"><div class="progress-bar-fill"></div></div>
    <form id="quizForm">
"""

    # ADD QUESTIONS
    for i, mcq in enumerate(mcqs):
        options_html = "".join(
            [
                f'<label><input type="radio" name="q{i}" value="{chr(65+j)}"> {opt}</label>'
                for j, opt in enumerate(mcq["options"])
            ]
        )

        html += f"""
        <div class="question-box" id="q{i}">
            <p><strong>Question {i+1}:</strong> {mcq['question']}</p>
            {options_html}
            <button type="button" onclick="nextQuestion({i})">{'Next' if i < len(mcqs)-1 else 'Submit'}</button>
        </div>
"""

    # JS + Footer
    html += (
        """
    </form>
</div>

<script>
const mcqs = """
        + json.dumps(mcqs)
        + """;

let current = 0;
let answers = new Array(mcqs.length).fill(null);
let score = 0;
const total = mcqs.length;

document.getElementById('q0').classList.add('active');
updateProgress(current);

function nextQuestion(i) {
    const selected = document.querySelector(`input[name="q${i}"]:checked`);

    if (!selected) {
        alert("Please select an option!");
        return;
    }

    answers[i] = selected.value;

    if (i < total - 1) {
        document.getElementById(`q${i}`).classList.remove('active');
        document.getElementById(`q${i+1}`).classList.add('active');
        current++;
        updateProgress(current);
    } else {
        showResult();
    }
}

function updateProgress(index) {
    document.querySelector('.progress-bar-fill').style.width =
        ((index + 1) / total * 100) + '%';
}

function showResult() {
    mcqs.forEach((q, i) => {
        if (answers[i] === q.correct) score++;
    });

    let html = `
        <h2 style="text-align:center; color:#2a2a72;">Quiz Complete!</h2>
        <h3 style="text-align:center;">Your Score: ${score} / ${total}</h3>
        <hr><h3>Detailed Report</h3>
    `;

    mcqs.forEach((q, i) => {
        html += `
            <div style="margin-bottom:20px; padding:15px; border-radius:10px; background:#f3f4ff">
                <p><b>Q${i+1}: ${q.question}</b></p>
                <p>Your Answer: <b>${answers[i] || "Not answered"}</b></p>
                <p>Correct Answer: <b style="color:green">${q.correct}</b></p>
            </div>
        `;
    });

    html += `<button onclick="goHome()">Return Home</button>`;
    document.querySelector('.quiz-container').innerHTML = html;
}

function goHome() {
    window.location.href = "/";
}
</script>

<footer style="text-align:center;margin-top:30px; font-size:14px;">
Created by <b>Ahmad Raza Khan</b> • AI Quiz Generator © 2025
</footer>

</body>
</html>
"""
    )

    return html  # ❤️ RETURN, DO NOT WRITE FILE
