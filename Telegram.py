import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

class TelegramBot:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        # 토큰을 token.bin 파일에서 읽어옵니다
        token_file = 'token.bin'

        with open(token_file, 'rb') as file:
             self.token = file.read().decode().strip()

        self.application = ApplicationBuilder().token(self.token).build()
        self._setup_handlers()

    def _setup_handlers(self):
        # /start 명령어를 처리하기 위한 핸들러
        start_handler = CommandHandler('start', self.start)
        self.application.add_handler(start_handler)

        # 모든 메시지를 처리하기 위한 핸들러
        echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo)
        self.application.add_handler(echo_handler)

        # 에러 핸들러 추가
        self.application.add_error_handler(self.error)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('안녕하세요! 저는 Echo 봇입니다. 메시지를 보내주시면 제가 다시 돌려드릴게요.')

    async def echo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(update.message.text)

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.error(f'Update {update} caused error {context.error}')

    def run(self):
        self.application.run_polling()

def read_token_from_bin_file(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return file.read().decode().strip()

if __name__ == '__main__':
    # 로깅 설정



    # TelegramBot 객체 생성 및 실행
    bot = TelegramBot()
    bot.run()
