# wordgame.py - the WordGame webapp - by Paul Barry.
# email: paul.barry@itcarlow.ie

import enchant
import time

import data_utils
import word_utils


# Before we do anything else, pre-process the words, then
# update our enchant dictionary.  We do this only ONCE.
# Yes, that's right: these are GLOBAL.
word_utils.pre_process_words()
wordgame_dictionary = enchant.DictWithPWL('en_GB', word_utils.ALL_WORDS)


def check_spellings(words) -> list:
    """Check a list of words for spelling errors.

       Is the word in the dictionary.
       Accepts a list of words and returns a list of tuples,
       with each tuple containing (word, bool) based on
       whether or not the word is spelled correctly."""
    spellings = []
    for w in words:
        spellings.append((w, wordgame_dictionary.check(w)))
    return spellings


if __name__ == '__main__':
    while True:
        print()
        sourceword = word_utils.get_source_word()
        start_time = time.perf_counter()
        we_have_a_winner = True
        print("You already know the rules, so do your worst...")
        print("\nHere's your sourceword:", sourceword)
        seven_words = list(input("\nGimme seven words: ").strip().split(' '))
        end_time = time.perf_counter()
        print()
        if seven_words[0] == '':
            print("You've gotta gimme something to work with here.")
            print()
            continue
        if len(seven_words) != 7:
            we_have_a_winner = False
            print('You did not provide seven words, maybe less, maybe more.')
        disallowed_letters = []
        for word in seven_words:
            disallowed = [letter for (letter, ok) in
                          word_utils.check_letters(sourceword, word)
                          if not ok]
            disallowed_letters.extend(disallowed)
        if disallowed_letters:
            we_have_a_winner = False
            print('Not allowed letters:', set(disallowed_letters))
        misspelt_words = [word for (word, ok) in
                          check_spellings(seven_words)
                          if not ok]
        if misspelt_words:
            we_have_a_winner = False
            print('Misspelt words:', sorted(misspelt_words))
        short_words = [word for (word, ok) in
                       word_utils.check_size(seven_words)
                       if not ok]
        if short_words:
            we_have_a_winner = False
            print('These words are too small:', sorted(short_words))
        if word_utils.duplicates(seven_words):
            we_have_a_winner = False
            print('You have duplicates:', sorted(seven_words))
        if word_utils.check_not_sourceword(seven_words, sourceword):
            we_have_a_winner = False
            print('You cannot use the source word:', sourceword)
        if we_have_a_winner:
            how_long = round(end_time-start_time, 2)
            print('You took', how_long, 'seconds.', end=' ')
            user = input("What's your name: ").strip()
            data_utils.add_to_scores(user, how_long)
            board = data_utils.get_sorted_leaderboard()
            print()
            print("Here's the leaderboard. How did you do?")
            print()
            pos = 1
            for timetook, username in board[:10]:
                print(f'{pos:2}: {username} in a time of {timetook} seconds.')
                pos += 1
            print()
            print('Position',
                  board.index((how_long, user))+1,
                  'out of',
                  len(board))
        print()
        ret = input('Are you going to go again? (y/n): ')
        if ret.lower()[0] == 'n':
            break
