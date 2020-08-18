from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import re
from newspaper import Article
import tkinter as tk


def frequency_table(formatted_article_text) -> dict:
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(formatted_article_text)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def sentences_score(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue


def average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average


def generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    print("\n")
    print("Sentence count in the summary: " + str(sentence_count))
    return summary


def get_article(art):


    article = Article(art, 'en')  # English
    article.download()
    article.parse()
    texte = article.text


    #with open("testing2.txt", "r+") as file:
        #infile = file.read()
    print("Original Article/Text: ")
    print(texte)
    print(len(texte))
    print("\n")

    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', texte)
    article_text = re.sub(r'\s+', ' ', article_text)
    print("Preprocessed Text: ")
    print(article_text)
    print(len(article_text))
    print("\n")
    # Removing special characters and digits


    freq_table = frequency_table(article_text)
    print("Words frequencies: ")
    print(freq_table)
    print("\n")

    '''
            We already have a sentence tokenizer, so we just need 
            to run the sent_tokenize() method to create the array of sentences.
    '''

    # 2 Tokenize the sentences
    sentences = sent_tokenize(article_text)
    print("Sentences: ")
    print(sentences)
    print("\n")

    # 3 Important Algorithm: score the sentences
    sentence_scores = sentences_score(sentences, freq_table)
    print("Sentence scores: ")
    print(sentence_scores)
    print("\n")

    # 4 Find the threshold
    threshold = average_score(sentence_scores)
    print("Threshold of the score: ")
    print(threshold)

    # 5 Important Algorithm: Generate the summary
    summary = generate_summary(sentences, sentence_scores, 1.5 * threshold)

    print("\n")
    print("Summarized Article/Text: ")
    print(summary)
    print(len(summary))

    #send summarized news into interface GUI
    label['text'] = summary

    # print data in text file
    with open('summarization_detail.dat', 'a') as f:

        f.write("Words frequencies: \n")
        f.write(str(freq_table))
        f.write("\n\n")

        f.write("Tokenized sentences: \n")
        f.write(str(sentences))
        f.write("\n\n")

        f.write("Sentence scores: \n")
        f.write(str(sentence_scores))
        f.write("\n\n")

        f.write("Threshold of the score: ")
        f.write(str(threshold))

        f.close()

    with open('summarization_summary.dat', 'a') as file:
        file.write(summary)
    file.close()

    return summary

#GUI Interface
HEIGHT = 700
WIDTH = 800

root = tk.Tk()
root.title("News Article Summarizer")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.1, anchor="center")

var = tk.StringVar()
label = tk.Label(root, textvariable=var, font=30)
label.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor="center")
var.set("NEWSPAPER SUMMARIZER\nPlease paste newspaper url")

entry = tk.Entry(frame, font=30)
entry.place(relwidth=0.65, relheight=0.65)

button = tk.Button(frame, text="Summarize News", font=40, command=lambda: get_article(entry.get()))
button.place(relx=0.7, relheight=0.65, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

label = tk.Label(lower_frame, wraplength=400, font=26, justify='left', bg='white')
label.place(relwidth=1, relheight=1)

root.mainloop()


if __name__ == "__main__":
    user_value = input("Please enter news article link:\n")
    get_article(user_value)
