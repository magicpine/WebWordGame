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
		session['timeTook'] = round((datetime.now() - session['startTime']).total_seconds(),2)
		winner = True
		errors = []
		#Rule Zero
		if len(wordList) != 7:
			winner = False
			if len(wordList) < 7:
				tmp = "You didn't type in enough words.  Words Detected: {0} Words needed: 7".format(len(wordList))
			else:
				tmp = 'You typed in too many words.  Words Detected: {0} Words needed: 7'.format(len(wordList))
			errors.append(tmp)
		#Rule One
		for words in wordList:
			wrongLettersList = []
			isError = False
			tmp = word_utils.check_letters(session['sourceWord'], words)
			for letters in tmp:
				if letters[1] == False:
					winner = False
					isError = True
					wrongLettersList.append(letters[0])	
			if (isError):
				isError = False
				tmp = 'You used these wrong letters [{0}] in this word: {1}.'.format(','.join(wrongLettersList), words)
				errors.append(tmp)
		#Rule Two
		length = word_utils.check_size(wordList)
		for words in length:
			if words[1] == False:
				winner = False
				tmp = 'The word: {0} is not three or more characters long'.format(words[0])
				errors.append(tmp)
		#Rule Four
		if word_utils.duplicates(wordList):
			winner = False
			wordListCopy = wordList.copy()
			for words in wordList:
				wordListCopy.remove(words)
				if words in wordListCopy:
					tmp = 'The word: {0} was duplicated'.format(words)
					errors.append(tmp)
		#Rule Five
		sameSourceWord = []
		sameSourceWord = word_utils.check_not_sourceword(wordList, session['sourceWord'])
		if len(sameSourceWord) != 0:
			winner = False
			tmp = 'You tried to use the source word {0} time(s)'.format(len(sameSourceWord))
			errors.append(tmp)
		#End Rules
		if winner:
			return render_template('winner.html',
									the_title='Winner!',
									timeTook = session['timeTook'])
		return render_template('loser.html',
								the_title='Loser',
								errors = errors)


@app.route('/processtime', methods=['POST'])
def topten():
	pass



if __name__ == '__main__':
	app.secret_key = 'itsmybirthdaythatsthepassword'
	app.run(debug = True)
