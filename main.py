import asyncio, os, random
from parser.parser import parse
from telegram import Bot, Update, Chat, StickerSet
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
# TELEGRAM_TOKEN='' TEST

bot = Bot(token=TELEGRAM_TOKEN)


async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    possible_phrases = ["Да-да, я жив","Я жив"]
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=random.choice(possible_phrases))

async def par(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update['message']['text'].split()[1]
    print(f'ЗАПУСТИЛ ПАРСИНГ {url}')
    await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Запускаю парсинг по ссылке {url}')
    try:
        document=open(parse(url),'rb')
        await context.bot.send_document(chat_id=update.effective_chat.id,document=document)
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Закончил парсинг по ссылке {url}')
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text=f'Не смог выполнить парсинг, возможно, некорректно указана ссылка - {url}')



def init_handlers():    
    handlers = (
        CommandHandler('ping', ping),
        CommandHandler('parser', par),
    )
    return handlers

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handlers(init_handlers())
    application.run_polling()
