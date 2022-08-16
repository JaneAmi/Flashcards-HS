from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


def main_menu(sess):
    try:
        answ = input('1. Add flashcards\n2. Practice flashcards\n3. Exit\n')
        assert answ in ['1', '2', '3'], f'\n{answ} is not an option\n'
        if answ == '1':
            sub_menu(sess)
            main_menu(sess)
        elif answ == '2':
            pr_flashcards(sess)
            main_menu(sess)
        elif answ == '3':
            print('\nBye!')
    except AssertionError as err:
        print(err)
        main_menu(sess)


def sub_menu(sess):
    try:
        answ = input('\n1. Add a new flashcard\n2. Exit\n')
        assert answ in ['1', '2'], f'\n{answ} is not an option'
        if answ == '1':
            add_flashcard(sess)
            sub_menu(sess)
    except AssertionError as err:
        print(err)
        sub_menu(sess)


def add_flashcard(sess):
    quest, answ = '', ''
    while quest == '':
        quest = input('Question:\n').strip()
    while answ == '':
        answ = input('Answer:\n').strip()
    new_card = Cards(questions=quest, answers=answ, box_number=1)
    sess.add(new_card)
    sess.commit()


def pr_flashcards(sess):
    fl_cards = sess.query(Cards).all()
    if fl_cards:
        for i in range(len(fl_cards)):
            answ = 'o'
            while answ != 'y' and answ != 'n' and answ != 'u':
                print(f'\nQuestion: {fl_cards[i].questions}')
                answ = input('press "y" to see the answer:\npress "n" to skip:\npress "u" to update:\n')
                if answ == 'y':
                    print(f'\nAnswer: {fl_cards[i].answers}\n')
                    learn_cards(sess, fl_cards[i].id, fl_cards[i].box_number)
                elif answ == 'u':
                    upd_flashcards(sess, fl_cards[i].id, fl_cards[i].questions, fl_cards[i].answers)
                elif answ != 'n':
                    print(f'{answ} is not an option')
    else:
        print('\nThere is no flashcard to practice!\n')


def upd_flashcards(sess, card_id, question, answer):
    query = sess.query(Cards)
    card_filter = query.filter(Cards.id == card_id)
    try:
        answ = input('press "d" to delete the flashcard:\npress "e" to edit the flashcard:')
        assert answ in ['e', 'd'], f'{answ} is not an option'
        if answ == 'd':
            card_filter.delete()
            sess.commit()
        elif answ == 'e':
            print(f'current question: {question}')
            new_quest = input('please write a new question:')
            if new_quest.strip() != '':
                card_filter.update({'questions': new_quest})
                sess.commit()
            print(f'current answer: {answer}')
            new_answ = input('please write a new answer:')
            if new_answ.strip() != '':
                card_filter.update({'answers': new_answ})
                sess.commit()
    except AssertionError as err:
        print(err)
        upd_flashcards(sess, card_id, question, answer)


def learn_cards(sess, card_id, box_number):
    query = sess.query(Cards)
    card_filter = query.filter(Cards.id == card_id)
    answ = 'o'
    while answ != 'y' and answ != 'n':
        answ = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
        if answ == 'n':
            card_filter.update({'box_number': 1})
            sess.commit()
        elif answ == 'y':
            new_box_number = box_number + 1
            if new_box_number == 3:
                card_filter.delete()
                sess.commit()
            else:
                card_filter.update({'box_number': new_box_number})
                sess.commit()
        else:
            print(f'{answ} is not an option')


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base = declarative_base()


class Cards(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    questions = Column(String)
    answers = Column(String)
    box_number = Column(Integer)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


main_menu(session)
