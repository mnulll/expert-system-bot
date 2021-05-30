import telebot
import time
import os
from dotenv import load_dotenv
from datetime import datetime
import traceback
from telebot.types import Message
from telebot import types
from telebot.apihelper import edit_message_reply_markup
from Quiz import Quiz
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
print(API_KEY)
bot = telebot.TeleBot(API_KEY)
counter = 1
quiz = 1
mark = 0
flag = True


def ctr():
    global counter
    counter += 1


def quiz_increment():
    global quiz
    quiz += 1


def quiz_reset():
    global quiz
    quiz = 1


def mark_increment():
    global mark
    mark += 1


def mark_reset():
    global mark
    mark = 0


def question(message):

    Class = f'Class{str(counter)}'
    question_turn = f'q{str(quiz)}'
    ans_choice = Quiz["Choice"][Class][question_turn].split("/")
    str_ans_choice = ""
    if len(ans_choice) == 4:
        str_ans_choice = "Answer:\n\n" + \
            ans_choice[0]+"\n\n"+ans_choice[1]+"\n\n" + \
            ans_choice[2]+"\n\n"+ans_choice[3]
        reply_board = types.ReplyKeyboardMarkup()
        choice_1 = types.KeyboardButton("/"+ans_choice[0][0])
        choice_2 = types.KeyboardButton("/"+ans_choice[1][0])
        choice_3 = types.KeyboardButton("/"+ans_choice[2][0])
        choice_4 = types.KeyboardButton("/"+ans_choice[3][0])
        reply_board.add(choice_1, choice_2, choice_3, choice_4)
    else:
        str_ans_choice = "Answer:\n\n" + \
            ans_choice[0]+"\n\n"+ans_choice[1]+"\n\n"
        reply_board = types.ReplyKeyboardMarkup()
        choice_1 = types.KeyboardButton("/"+ans_choice[0][0])
        choice_2 = types.KeyboardButton("/"+ans_choice[1][0])
        reply_board.add(choice_1, choice_2)

    bot.reply_to(message, "Question:\n\n"+Quiz["Question"][Class]
                 [question_turn], reply_markup=reply_board)
    bot.reply_to(message, str_ans_choice)
    bot.register_next_step_handler(message, answer)


def answer(message):
    Class = f'Class{str(counter)}'
    question_turn = f'q{str(quiz)}'
    reply_board = types.ReplyKeyboardRemove(selective=False)
    ans = str(message.text)[1]
    print(ans)
    reply_board = types.ReplyKeyboardMarkup()
    next = types.KeyboardButton("Next Question")
    reply_board.add(next)
    if ans == Quiz["Answer"][Class][question_turn]:
        mark_increment()
        bot.reply_to(message, "correct", reply_markup=reply_board)
    else:
        bot.reply_to(message, "wrong", reply_markup=reply_board)
    if quiz < 10:
        quiz_increment()
        bot.register_next_step_handler(message, question)
    else:
        if mark >= 7:
            if counter == 10:
                bot.reply.to(
                    message, "You passed the course, Congratulations!")
            else:
                mark_reset()
                quiz_reset()
                ctr()
                reply_board = types.ReplyKeyboardRemove(selective=False)
                bot.reply_to(message, quiz)
                reply_board = types.ReplyKeyboardMarkup()
                itemYes = types.KeyboardButton("/Ready")
                itemNo = types.KeyboardButton("/Not_Ready")
                reply_board.add(itemYes, itemNo)
                bot.reply_to(
                    message, "You passed. Are you ready for next class? ", reply_markup=reply_board)
        else:
            mark_reset()
            quiz_reset()
            reply_board = types.ReplyKeyboardRemove(selective=False)
            bot.reply_to(message, quiz)
            reply_board = types.ReplyKeyboardMarkup()
            itemYes = types.KeyboardButton("/Ready")
            itemNo = types.KeyboardButton("/Not_Ready")
            reply_board.add(itemYes, itemNo)
            bot.reply_to(
                message, "You failed. You need to repeat the class. Are you ready? ", reply_markup=reply_board)


def getTime():
    now = datetime.now()
    currenttime = now.strftime("%H")
    if(int(currenttime) < 6 or int(currenttime) >= 15):
        return "Evening"
    elif(int(currenttime) >= 6 and int(currenttime) < 12):
        return "Morning"
    elif(int(currenttime) >= 12 and int(currenttime) < 15):
        return "Afternoon"


@bot.message_handler(commands=['HelloDr'])
def greet(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, "Good "+getTime()+" " + name)

    def ready():
        reply_board = types.ReplyKeyboardMarkup()
        itemYes = types.KeyboardButton("/Ready")
        itemNo = types.KeyboardButton("/Not_Ready")
        reply_board.add(itemYes, itemNo)
        print(Quiz)
        bot.send_message(
            message.chat.id, "Are you ready to start the class?", reply_markup=reply_board)

        @bot.message_handler(commands=['Ready'])
        def letslearn(message):
            reply_board = types.ReplyKeyboardRemove(selective=False)
            material = f'Class{str(counter)}'
            note = material+".pptx"
            powerpoint = open(note, 'rb')
            bot.send_document(message.chat.id, powerpoint)
            bot.send_message(
                message.chat.id, "This are the topic for "+material)
            reply_board = types.ReplyKeyboardMarkup()
            itemUnderstand = types.KeyboardButton("/Dont_Understand")
            itemQuiz = types.KeyboardButton("/Proceed_To_Quiz")
            reply_board.add(itemUnderstand, itemQuiz)
            bot.send_message(
                message.chat.id, "Tell me if you don't understand but if you understand we shall proceed to the quiz", reply_markup=reply_board)
            reply_board = types.ReplyKeyboardRemove(selective=False)

            @ bot.message_handler(commands=['Dont_Understand'])
            def send_youtube(message):
                links = {
                    "Class1": "https://youtu.be/2ePf9rue1Ao",
                    "Class2": "https://youtu.be/XO6SV0Mup1E",
                    "Class3": "https://youtu.be/5OJv6iHMtVw",
                    "Class4": "https://youtu.be/PzEWHH2v3TE",
                    "Class5": "https://youtu.be/9-8Js62wzQs",
                    "Class6": "https://youtu.be/CMrHM8a3hqw",
                    "Class7": "https://youtu.be/oAVIf9z62CQ",
                    "Class8": " https://youtu.be/z-EtmaFJieY",
                    "Class9": "https://youtu.be/DKSZHN7jftI",
                    "Class10": "https://youtu.be/yCXm5cgG0UA"
                }
                material = f'Class{str(counter)}'
                bot.send_message(message.chat.id, links[material])
                reply_board = types.ReplyKeyboardMarkup()
                itemFAQ = types.KeyboardButton("/FAQ")
                itemQuiz = types.KeyboardButton("/Proceed_To_Quiz")
                reply_board.add(itemFAQ, itemQuiz)
                bot.send_message(
                    message.chat.id, "If you understand we shall proceed to the quiz or you can look up to FAQ before that", reply_markup=reply_board)
                reply_board = types.ReplyKeyboardRemove(selective=False)
                print(counter)

            @bot.message_handler(commands="FAQ")
            def send_faq(message):
                Class = Class = f'Class{str(counter)}'
                faq = Quiz["FAQ"][Class]
                reply_board = types.ReplyKeyboardMarkup()
                itemQuiz = types.KeyboardButton("/Proceed_To_Quiz")
                reply_board.add(itemQuiz)
                bot.send_message(message.chat.id, faq,
                                 reply_markup=reply_board)

            @ bot.message_handler(commands=['Proceed_To_Quiz'])
            def send_quiz(message):
                reply_board = types.ReplyKeyboardMarkup()
                itemYes = types.KeyboardButton("/Ready")
                itemNo = types.KeyboardButton("/Not_Ready")
                reply_board.add(itemYes, itemNo)
                bot.send_message(message.chat.id, "Are you ready",
                                 reply_markup=reply_board)
                bot.register_next_step_handler(message, question)

        @bot.message_handler(commands=['Not_Ready'])
        def notyet(message):
            bot.send_message(message.chat.id, "I will wait for you")
            ready()
    ready()


while True:
    try:
        bot.polling(none_stop=False)
    except Exception:
        print('crash')
        traceback.print_exc()
        time.sleep(1)
