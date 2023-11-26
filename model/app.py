from flask import Flask, request, jsonify
from flask_cors import CORS
import sentiment_explorerVersion7 as lib1
import sentiment_explorerVersion8 as lib2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate', methods=['POST'])
def get_score():
    text = request.get_data(as_text=True)
    print("\nReceived sentiment text in text format:", text)

    text = lib1.newtext_fullstop(text)
    # print("\nAfter cleaning:", text)
    # text = newtext(text)
    polarity4_list = lib1.findPolarity4_too_like(text)
    score4 = lib1.countPolarity4(polarity4_list, 7)
    sarcasm = lib1.recognise_sarcasm(polarity4_list)
    score4 = lib1.flip(sarcasm, score4)
    polarity5_list = lib1.findPolarity5(text)
    score5 = lib1.countPolarity5(polarity5_list, 7)
    polarity6_list = lib1.findPolarity6(text)
    is_adversative_present = lib1.adversative_present(polarity6_list)
    polarity_count_after_adversative = lib1.update_p_after_adversative(is_adversative_present, score4, score5)
    polarity_count_after_adversative = lib1.qn_mark(text, polarity_count_after_adversative)
    score_multi = lib1.multi_value(polarity6_list, text, polarity_count_after_adversative, 5)
    score_multi = lib1.qn_mark(text, score_multi)
    final_score = lib1.new_multi(score_multi)
    sentiment = ""
    print("\nAfter cleaning:", text)

    if (final_score == -2) :
        sentiment = "Strongly Negative"

    elif (final_score == -1) :
        sentiment = "Negative"
    
    elif (final_score == 0) :
        sentiment = "Neutral"
    
    elif (final_score == 1) :
        sentiment = "Positive"
    
    elif (final_score == 2) :
        sentiment = "Strongly Positive"
    


    return jsonify(
        {
            "code": 200,
            "text": text,
            "data": sentiment,
        }
    )

@app.route('/generate2', methods=['POST'])
def get_score2():
    text = request.get_data(as_text=True)
    print("\nReceived sentiment text in text format:", text)

    # test for number of sentences
    if text[-1] != ".":
        text = text + "."

    # test for number of sentences, if 1, call for /generate instead
    sentence_list = lib2.breakParagraph(text)
    print(sentence_list)
    if len(sentence_list) == 1:
        return get_score()

    #create a dictionary to store original_phases as key and target_produced_words1 and sentiment as the values from ngram_glen2023_replace_words.csv
    replace_words_dic = {}
    replace_words_sentiment_dic = {}
    with open('ngram_glen2023_replace_words.csv', 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split(',')
            replace_words_dic[line[4]] = line[6]
            replace_words_sentiment_dic[line[6]] = line[9]

    sentence_list = lib2.breakParagraph(text)
    clean_sentence_list = []
    for sentence in sentence_list:
        clean_sentence_list.append(lib2.newtext_fullstop(sentence))
    
    total_score = 0
    total_count = 0
    average_score = 0
    neutral_count = 0
    non_neutral_count = 0
    negative_count = 0
    positive_count = 0
    sentiment = "To be determined"
    for sentence in clean_sentence_list:
        for k, v in replace_words_sentiment_dic.items():
            if k in sentence:
                if v == "Positive":
                    total_score += 1
                elif v == "Negative":
                    total_score -= 1
                elif v == "Strongly Positive":
                    total_score += 2
                elif v == "Strongly Negative":
                    total_score -= 2
                elif v == "Slightly Positive":
                    total_score += 0.5
                elif v == "Slightly Negative":
                    total_score -= 0.5
        
        if sentence != ".":
            total_count += 1
            polarity4_list = lib2.findPolarity4_too_like(sentence)
            score4 = lib2.countPolarity4(polarity4_list, 7)
            sarcasm = lib2.recognise_sarcasm(polarity4_list)
            score4 = lib2.flip(sarcasm, score4)
            polarity5_list = lib2.findPolarity5(sentence)
            score5 = lib2.countPolarity5(polarity5_list, 7)
            polarity6_list = lib2.findPolarity6(sentence)
            is_adversative_present = lib2.adversative_present(polarity6_list)
            polarity_count_after_adversative = lib2.update_p_after_adversative(is_adversative_present, score4, score5)
            polarity_count_after_adversative = lib2.qn_mark(sentence, polarity_count_after_adversative)
            score_multi = lib2.multi_value(polarity6_list, sentence, polarity_count_after_adversative, 5)
            score_multi = lib2.qn_mark(sentence, score_multi)
            final_score = lib2.new_multi(score_multi)

        if final_score == 0:
            neutral_count += 1
        elif final_score < 0:
            non_neutral_count += 1
            negative_count += 1
        else:
            non_neutral_count += 1
            positive_count += 1

        if total_count == 1: 
            final_score = final_score * 2

        total_score += final_score
    
    if non_neutral_count == 0:  #this is to find the average among the weighted sentiment values
        average_score = 0
        
        positive_percentage = 0
        
        negative_percentage = 0
        
    else:
        average_score = round((total_score / non_neutral_count), 2)
        
        positive_percentage = round(((positive_count / non_neutral_count) * 100), 2) #this is to calculate percentage of positive sentiments

        negative_percentage = round(((negative_count / non_neutral_count) * 100), 2) #this is to calculate percentage of negative sentiments

    # calculate sentiment of paragraph
    if average_score == 0: #neutral
        if (positive_percentage - negative_percentage >= 20):
            sentiment = "Positive"
        elif (negative_percentage - positive_percentage >= 20):
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
    elif (average_score >= 1) and (positive_percentage - negative_percentage >= 30): #strongly positive
        sentiment = "Strongly Positive"
    
    elif (average_score > 0): #positive
        if ((non_neutral_count/total_count)*100 > 80) and (non_neutral_count >= 5):
            sentiment = "Strongly Positive"
        elif (positive_percentage - negative_percentage >= 0):
            sentiment = "Positive"
        else:
            sentiment = "Mixed Positive"
        
    elif (average_score <= -1) and (negative_percentage - positive_percentage >= 30): #strongly negative
        sentiment = "Strongly Negative"
    
    elif (average_score < 0): #negative
        if ((non_neutral_count/total_count)*100 > 80) and (non_neutral_count >= 5):
            sentiment = "Strongly Negative"
        elif (negative_percentage - positive_percentage >= 0):
            sentiment = "Negative"
        else:
            sentiment = "Mixed Negative"

    return jsonify(
        {
            "code": 200,
            "text": text,
            "data": sentiment,
        }
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)