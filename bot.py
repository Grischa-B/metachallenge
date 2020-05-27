import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
						  ConversationHandler)
import os

#Constants depending on bot's release way
PORT = int(os.environ.get('PORT', 5000))
TOKEN = ''
HOST_URL = ''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)
logger = logging.getLogger(__name__)

#Dict to store user's data
users = {}

#Label to handle convesation
QUESTION = range(1)

#Questions to ask user
questions=(
'1. Для меня как отрицательные, так и положительные эмоции служат источником знания о том, как поступать в жизни.',
'2. Отрицательные эмоции помогают мне понять, что я должен изменить в своей жизни.',
'3. Я спокоен, когда испытываю давление со стороны.',
'4. Я способен наблюдать изменение своих чувств.',
'5. Когда необходимо, я могу быть спокойным и сосредоточенным, чтобы действовать в соответствии с запросами жизни.',
'6. Когда необходимо, я могу вызвать у себя широкий спектр положительных эмоций, такие, как веселье, радость, внутренний подъем и юмор.',
'7. Я слежу за тем, как я себя чувствую.',
'8. После того как что-то расстроило меня, я могу легко совладать со своими чувствами.',
'9. Я способен выслушивать проблемы других людей.',
'10. Я не зацикливаюсь на отрицательных эмоциях.',
'11. Я чувствителен к эмоциональным потребностям других.',
'12. Я могу действовать на других людей успокаивающе.',
'13. Я могу заставить себя снова и снова встать перед лицом препятствия.',
'14. Я стараюсь подходить к жизненным проблемам творчески.',
'15. Я адекватно реагирую на настроения, побуждения и желания других людей.',
'16. Я могу легко входить в состояние спокойствия, готовности и сосредоточенности.',
'17. Когда позволяет время, я обращаюсь к своим негативным чувствам и разбираюсь, в чем проблема.',
'18. Я способен быстро успокоиться после неожиданного огорчения.',
'19. Знание моих истинных чувств важно для поддержания «хорошей формы».',
'20. Я хорошо понимаю эмоции других людей, даже если они не выражены открыто.',
'21. Я могу хорошо распознавать эмоции по выражению лица.',
'22. Я могу легко отбросить негативные чувства, когда необходимо действовать.',
'23. Я хорошо улавливаю знаки в общении, которые указывают на то, в чем другие нуждаются.',
'24. Люди считают меня хорошим знатоком переживаний других людей.',
'25. Люди, осознающие свои истинные чувства, лучше управляют своей жизнью.',
'26. Я способен улучшить настроение других людей.',
'27. Со мной можно посоветоваться по вопросам отношений между людьми.',
'28. Я хорошо настраиваюсь на эмоции других людей.',
'29. Я помогаю другим использовать их побуждения для достижения личных целей.',
'30. Я могу легко отключиться от переживания неприятностей.'
)

#Variations of answer to the questions
answers = (('Полностью согласен', 'Полностью не согласен'),
	(' В основном согласен', 'В основном не согласен'),
	('Отчасти согласен', 'Отчасти не согласен'))

#Class to store user's characteristics in one object
class USER(object):
	def __init__(self):
		self.em_osv = 0
		self.upr = 0
		self.samo = 0
		self.emp = 0
		self.rasp = 0
		self.progress = 0

#Function to handle /start command
#Returns label to start asking questions
def start(update, context):
	reply_keyboard = [['Start!']]
	users[update.message.from_user.id] = USER()
	update.message.reply_text(
		'Привет, предлагаю тебе пройти тест на эмоциональный интеллект по Холлу.',
		reply_markup=ReplyKeyboardMarkup(reply_keyboard))

	return QUESTION

#Function to handle answers to the past question and ask a new one
#If it's not the last question, returns label to continue asking questions
#else returns label to end conversation
def question(update, context):
	user = update.message.from_user
	#computing scores of each parameter after every answer
	if users[user.id].progress > 0:
		val=0
		if update.message.text in answers[0]:
			val = 6 if update.message.text == answers[0][0] else 1
		elif update.message.text in answers[1]:
			val = 5 if update.message.text == answers[1][0] else 2
		elif update.message.text in answers[2]:
			val = 4 if update.message.text == answers[2][0] else 3

		if users[user.id].progress in (1, 2, 4, 17, 19, 25):
			users[user.id].em_osv+=val
		elif users[user.id].progress in (3, 7, 8, 10, 18, 30):
			users[user.id].upr+=val
		elif users[user.id].progress in (5, 6, 13, 14, 16, 22):
			users[user.id].samo+=val
		elif users[user.id].progress in (9, 11, 20, 21, 23, 28):
			users[user.id].emp+=val
		elif users[user.id].progress in (12, 15, 24, 26, 27, 29):
			users[user.id].rasp+=val

	if users[update.message.from_user.id].progress < 30:
	#continue asking
		update.message.reply_text(questions[users[update.message.from_user.id].progress],
			reply_markup=ReplyKeyboardMarkup(answers))

		users[update.message.from_user.id].progress+=1
		return QUESTION
	else:
	#end conversation and give results
		update.message.reply_text("""
Эмоциональная осведомленность: {0}/36
Управление своими эмоциями: {1}/36
Самомотивация: {2}/36
Эмпатия: {3}/36
Распознавание эмоций других людей: {4}/36
		""".format(users[user.id].em_osv,
				users[user.id].upr,
				users[user.id].samo,
				users[user.id].emp,
				users[user.id].rasp), reply_markup=ReplyKeyboardRemove())
		return ConversationHandler.END

#Fallback function to end convesation immediately
def cancel(update, context):
	user = update.message.from_user
	logger.info("User %s canceled the conversation.", user.first_name)
	update.message.reply_text('Bye! I hope we can talk again some day.',
							  reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END

#Log Errors caused by Updates.
def error(update, context):
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	#Objects to handle receive
	updater = Updater(TOKEN, use_context=True)
	dp = updater.dispatcher

	#Handle the conversation
	conv_handler = ConversationHandler(
		entry_points=[CommandHandler('start', start)],

		states={

			QUESTION: [MessageHandler(Filters.text, question)],

			},

		fallbacks=[CommandHandler('cancel', cancel)]
	)

	dp.add_handler(conv_handler)

	# log all errors
	dp.add_error_handler(error)

	# Start the Bot
	updater.start_webhook(listen="0.0.0.0",
						  port=int(PORT),
						  url_path=TOKEN)
	updater.bot.setWebhook(HOST_URL + TOKEN)

	updater.idle()


if __name__ == '__main__':
	main()
