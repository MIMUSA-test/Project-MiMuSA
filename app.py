from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment_explorerVersion7 import *

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate', methods=['POST'])
def get_score():
    text = request.get_data(as_text=True)
    print("\nReceived sentiment text in text format:", text)

    # text = "There must be a reason why the officer did this to the PMD rider."
    # text = "The bad guy broke his arm, he was so lucky."
    text = newtext_fullstop(text)
    text = newtext(text)
    polarity4_list = findPolarity4_too_like(text)
    score4 = countPolarity4(polarity4_list, 7)
    sarcasm = recognise_sarcasm(polarity4_list)
    score4 = flip(sarcasm, score4)
    polarity5_list = findPolarity5(text)
    score5 = countPolarity5(polarity5_list, 7)
    polarity6_list = findPolarity6(text)
    is_adversative_present = adversative_present(polarity6_list)
    polarity_count_after_adversative = update_p_after_adversative(is_adversative_present, score4, score5)
    polarity_count_after_adversative = qn_mark(text, polarity_count_after_adversative)
    score_multi = multi_value(polarity6_list, text, polarity_count_after_adversative, 5)
    score_multi = qn_mark(text, score_multi)
    final_score = new_multi(score_multi)


    return jsonify(
        {
            "code": 200,
            "text": text,
            "data": final_score
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)