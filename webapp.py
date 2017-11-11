from flask import Flask, render_template, request, session
from datetime import datetime

import word_utils
import data_utils
import wordgame

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('rules.html', 
								the_title='Welcome to Word Game!')
	
	
@app.route('/startgame', methods=['POST'])
def startGame():
	if request.method == 'POST':
		session['sourceWord'] = word_utils.get_source_word()
		session['startTime'] = datetime.now()
		return render_template('startgame.html',
								the_title='Word Game',
								source_word = session['sourceWord'])


@app.route('/processwords', methods=['POST'])
def processWords():
	if request.method == 'POST':
		wordList = list((request.form['wordList']).strip().split(' '))
		for words in wordList:
			words = words.lower()
		timeTook = round((datetime.now() - session['startTime']).total_seconds(),2)
		winner = True
		#Rule Zero
		if (len(wordList) != 7):
			winner = False

		#Rule One
		wrongLetters = {}
		for words in wordList:
			wrongLettersList = []
			tmp = word_utils.check_letters(session['sourceWord'], words)
			for letters in tmp:
				if letters[1] == False:
					winner = False
					wrongLettersList.append(letters[0])
			wrongLetters[words] = wrongLettersList
		#Rule Two
		wrongSpelling = []
		spelling = wordgame.check_spellings(wordList)
		for words in spelling:
			if words[1] == False:
				wrongSpelling.append(words)
		if len(wrongSpelling) != 0:
			winner = False
		#Rule Three
		wrongLength = []
		length = word_utils.check_size(wordList)
		for words in length:
			if words[1] == False:
				wrongLength.append(words)
		if len(wrongLength) != 0:
			winner = False
		#Rule Four
		duplicatesWords = []
		if word_utils.duplicates(wordList):
			winner = False
			tmp = wordList.copy()
			for words in wordList:
				tmp.remove(words)
				if words in tmp:
					duplicatesWords.append(words)
		#Rule Five
		sameSourceWord = []
		sameSourceWord = word_utils.check_not_sourceword(wordList, session['sourceWord'])
		if len(sameSourceWord) != 0:
			winner = False
		#Checks
		if winner:
			return render_template('winner.html',
									the_title='Winner!',
									timeTook = timeTook)
		errors = [wrongLetters, wrongSpelling, wrongLength, duplicatesWords, sameSourceWord]
		return render_template('loser.html',
								the_title='Loser',
								errors = errors)


if __name__ == '__main__':
	app.secret_key = 'itsmybirthdaythatsthepassword'
	app.run(debug = True)
