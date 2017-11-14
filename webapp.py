from flask import Flask, render_template, request, session, redirect, url_for, Markup, flash
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
				tmp = Markup("You didn't type in enough words.  Words Detected: <b>{0}</b> Words needed: <b>7</b>".format(len(wordList)))
			else:
				tmp = Markup('You typed in too many words.  Words Detected: <b>{0}</b> Words needed: <b>7</b>'.format(len(wordList)))
			flash(tmp)
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
				tmp = Markup('You used these wrong letters <b>[{0}]</b> in this word: <b>{1}</b>.'.format(','.join(wrongLettersList), words))
				flash(tmp)
		#Rule Two
		spellCheck = wordgame.check_spellings(wordList)
		for words in spellCheck:
			if words[1] == False:
				winner = False
				tmp = Markup('The word: <b>{0}</b> is not spelled correctly'.format(words[0]))
				flash(tmp)
		#Rule Three/
		length = word_utils.check_size(wordList)
		for words in length:
			if words[1] == False:
				winner = False
				tmp = Markup('The word: <b>{0}</b> is not three or more characters long'.format(words[0]))
				flash(tmp)
		#Rule Four
		if word_utils.duplicates(wordList):
			winner = False
			wordListCopy = wordList.copy()
			for words in wordList:
				wordListCopy.remove(words)
				if words in wordListCopy:
					tmp = Markup('The word: <b>{0}</b> was duplicated'.format(words))
					flash(tmp)
		#Rule Five
		sameSourceWord = []
		sameSourceWord = word_utils.check_not_sourceword(wordList, session['sourceWord'])
		if len(sameSourceWord) != 0:
			winner = False
			tmp = Markup('You tried to use the source word <b>{0}</b> time(s)'.format(len(sameSourceWord)))
			flash(tmp)
		#End Rules
		if winner:
			return render_template('winner.html',
									the_title='Winner!',
									timeTook = session['timeTook'])
		return render_template('loser.html',
								the_title='Loser')


@app.route('/processtime', methods=['POST', 'GET'])
def topten():
	if request.method == 'POST':
		session['name'] = request.form['name'].strip()
		data_utils.add_to_scores(session['name'], session['timeTook'])
		return redirect(url_for('topten'))
	elif request.method == 'GET':
		leaderBoard = data_utils.get_sorted_leaderboard()
		return render_template('processtime.html',
								the_title='Top Ten for Word Game',
								board = leaderBoard,
								pos = leaderBoard.index((session['timeTook'], session['name']))+1,
								total = len(leaderBoard))

if __name__ == '__main__':
	app.secret_key = 'itsmybirthdaythatsthepassword'
	app.run(debug = True)
