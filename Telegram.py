import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from apartment_data import get_apart_trade_data_search
from region_code import *

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
        message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        self.application.add_handler(message_handler)

        # 에러 핸들러 추가
        self.application.add_error_handler(self.error)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('주소를 입력하면 해당 장소의 부동산 거래 기록을 알려드립니다\n\n[ 시, 도 ] [ 시, 군, 구 ] [ 읍, 면, 동 ] [ 년 ] [ 월 ] 순으로 입력해주세요.\n\n띄어 쓰기를 기준으로 구분되어야 합니다.')

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logging.error(f'Update {update} caused error {context.error}')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message_text = update.message.text.strip()
        words = message_text.split()
        print(words)
        print(sgg_codes)

        if len(words) != 5:
            await update.message.reply_text('에러: [ 시, 도 ] [ 시, 군, 구 ] [ 읍, 면, 동 ] [ 년 ] [ 월 ] 순으로 입력해주세요. 띄어쓰기를 기준으로 구분되어야 합니다.')
        elif not words[-2].isdigit() or not words[-1].isdigit():
            await update.message.reply_text('에러: [ 년 ] [ 월 ] 은 숫자로 입력해주세요.')
        elif words[0] not in sgg_codes:
            await update.message.reply_text('시/도 정보를 다시 확인해 주세요.')
        elif words[1] not in sgg_codes[words[0]]:
            await update.message.reply_text(f'시/군/구 정보를 다시 확인해 주세요. ({words[0]}에 없는 행정구역입니다.)')
        elif words[2] not in umds[f'{words[0]} {words[1]}']:
            await update.message.reply_text(f'읍/면/동 정보를 다시 확인해 주세요. ({words[1]}에 없는 행정구역입니다.)')
        else:
            result = self.process(words)
            if len(result ) == 0:
                await update.message.reply_text('해당하는 데이터가 없습니다.')
            else:
                await update.message.reply_text(result)

    def process(self, words: list) -> str:
        api_result = get_apart_trade_data_search(words[0], words[1], words[2], int(words[3]), int(words[4]))
        result = []
        for dict_item in api_result:
            item_str = "\n".join([f"{key}: {value}" for key, value in dict_item.items()])
            result.append(item_str)

        content = "\n---------------\n".join(result)

        return content


    def run(self):
        self.application.run_polling()

def read_token_from_bin_file(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return file.read().decode().strip()

def run_telegram_bot():
    # TelegramBot 객체 생성 및 실행
    bot = TelegramBot()
    bot.run()


if __name__ == '__main__':
    # TelegramBot 객체 생성 및 실행
    bot = TelegramBot()
    bot.run()
