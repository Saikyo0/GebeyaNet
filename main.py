import logging
import time

from telegram import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
illegal_chars = ['#', '@', '!', '%', '$', '^', '&', '*', '~', '`', '[', ']', '(', ')', '{',
                 '}', ',', '/', '?', '+', '-', '.', '<', '>', ':', ';', '-', '_', '=', '|', '\\']

Token = ""


class bot:
    def __init__(self):
        self.current_item = 'N'
        self.image = ''
        self.num_in_stock = 0
        self.value = 0
        self.description = ""
        self.name = ''
        self.delivery_time = ''
        self.chat_id = ''
        self.type = ''
        self.current_message = None

    def start(self, update: Update, context: CallbackContext) -> None:
        if update.message.text.endswith('ver'):
            self.buy_id = update.message.text.replace('ver', '').replace('/start ', '')
            keyboard = [[InlineKeyboardButton('Cancel', callback_data='paranoid')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("When is the delivery date?", reply_markup=reply_markup)
            self.current_item = 'DeliveryDate'
        else:
            reply_keyboard = [['Post', 'Status'],
                              ['Help', 'Settings']
                              ]
            update.message.reply_text(
                'Welcome, This bot is used for posting and managing items' +
                ' sold or being sold by you, Choose one of the options in the menu below',
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, input_field_placeholder='Menu:'
                ),
            )

    def controller(self, update: Update, context: CallbackContext) -> None:
        if self.current_item == 'N':
            pass

        elif self.current_item == 'Name':
            try:
                self.name = update.message.text
            except:
                self.name = None
            name_list = self.name
            for x in name_list:
                for y in illegal_chars:
                    if x == y:
                        self.name = 'illegal'
            if self.name != '' and self.name is not None and self.name != 'illegal':
                update.message.delete()
                keyboard = [[InlineKeyboardButton('Cancel', callback_data='Cancel')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text="Send me the description of your prouct",
                                          reply_markup=reply_markup)
                self.current_item = 'Description'
            else:
                update.message.reply_text("Sorry, but the name you\'ve inputted isn't allowed, Reasons:\n"
                                          '1, the name contains illegal characters like: !@$%^&#\n'
                                          '2, you\'re input isn\'t a text message\n'
                                          'Correct Example: Prime Water')

        elif self.current_item == 'Description':
            try:
                self.description = update.message.text
            except:
                self.description = None
            if self.description != '' and self.description is not None and len(self.description.split(' ')) < 50:
                update.message.delete()
                keyboard = [[InlineKeyboardButton('Cancel', callback_data='Cancel')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(text='Nice, now could send me an Image of the product?',
                                          reply_markup=reply_markup)
                self.current_item = 'Image'
            else:
                update.message.reply_text("Sorry, but the description you\'ve inputted isn't allowed, Reasons:\n"
                                          '1, the length is more than 50 letters\n'
                                          '2, you\'re input isn\'t a text message\n')

        elif self.current_item == 'Image':
            try:
                self.image = update.message.photo[0].file_id
            except:
                self.image = None
            if self.image is not None and self.image != '':
                update.message.delete()
                keyboard = [[InlineKeyboardButton('Cancel', callback_data='Cancel')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Done, now What\'s the amount of products in stock?',
                                          reply_markup=reply_markup)
                self.current_item = 'Stock'
            else:
                update.message.reply_text("Sorry, but the image you\'ve sent isn't allowed, Reasons:\n"
                                          '1, it\'s not an image\n'
                                          '2, the image might be corrupted, resend it\n'
                                          '3, you might\'ve sent the image as a file')

        elif self.current_item == 'Stock':
            try:
                self.num_in_stock = int(update.message.text)
            except:
                self.num_in_stock = None
            if self.num_in_stock is not None and self.num_in_stock != 0:
                update.message.delete()
                keyboard = [[InlineKeyboardButton('Cancel', callback_data='Cancel')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text('Alrighty, What\'s the value of the product?',
                                          reply_markup=reply_markup)
                self.current_item = 'Value'
            else:
                update.message.reply_text("Sorry, but the Amount you\'ve sent isn't allowed, Reasons:\n"
                                          '1, it\'s not an number\n'
                                          '2, the number might have additional characters that aren\'t numbers\n')

        elif self.current_item == 'Value':
            try:
                self.value = update.message.text
            except:
                self.value = None
            if self.value is not None and self.value != '':
                char_list = self.value.split()
                num = ''
                prefix = ''
                for x in char_list:
                    if x.isnumeric():
                        num = x
                    if not x.isnumeric():
                        prefix = x
                if num.isnumeric() and prefix.isascii():
                    self.value = f'{num} {prefix}'
                    print(self.value)
                    update.message.delete()
                    update.message.reply_text("All Done! now could you please check over the data:")
                    self.caption = (f"Description:\n   {self.description}\nIn Stock:\n"
                                    f"   {self.num_in_stock}\nPrice:\n   {self.value} \n#{self.type} goods")
                    keyboard = [
                        [InlineKeyboardButton('Done', callback_data='Done')],
                        [InlineKeyboardButton('Cancel', callback_data='Cancel')]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_photo(photo=self.image, caption=self.caption, reply_markup=reply_markup)
                else:
                    update.message.reply_text("Sorry, but the Amount you\'ve sent isn\'t allowed, it doesn\'t"
                                              " have numbers or it doesn\'t have a prefix\n"
                                              'Example: 100 birr')
            else:
                update.message.reply_text("Sorry, but the Amount you\'ve sent isn't allowed, Reasons:\n"
                                          '1, it\'s not a text\n'
                                          '2, the number might have additional characters that aren\'t numbers\n')
        elif self.current_item == 'DeliveryDate':
            self.delivery_time = update.message.text
            keyboard = [
                [InlineKeyboardButton('Done', callback_data='Done-t')],
                [InlineKeyboardButton('Change', callback_data='Change-t')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(f'You Have inputted {self.delivery_time} as Delivery Time',
                                      reply_markup=reply_markup)
            pass

        elif update.message.text == 'Cancel':
            update.message.reply_text("Roger! Hope you continue next time")
            self.image = ''
            self.caption = ''
            self.num_in_stock = 0
            self.description = ''
            self.value = 0
            self.current_item = 'N'
        else:
            pass

    def help(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Welcome to the help section, commands:-\n'
                                  'post --> post a product in the catalogue channel\n'
                                  'status --> check the status of posted product\n'
                                  'settings --> tweak the options for your usage\n'
                                  'myCustomers --> contains both your usual buyers and blacklist'
                                  )

    def post(self, update: Update, context: CallbackContext) -> None:
        keyboard = [
            [
                InlineKeyboardButton("Luxury goods", callback_data='catluxury'),
            ],
            [
                InlineKeyboardButton("Home Appliences", callback_data='cathome'),
            ],
            [
                InlineKeyboardButton("Day-to-Day goods", callback_data='catday-to-day')
            ],
            [
                InlineKeyboardButton("Electronics", callback_data='catelectronics')
            ],
            [
                InlineKeyboardButton("Clothing", callback_data='catclothing')
            ],
            [
                InlineKeyboardButton("Miscallenous goods", callback_data='catmiscallenous')
            ],
            [
                InlineKeyboardButton("Cancel", callback_data='Cancel')
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        self.current_message = update.message.reply_text('Please choose the catagory of your product:',
                                                         reply_markup=reply_markup)

    def button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        query.answer()

        if str(query.data).startswith('cat'):
            self.type = query.data.replace('cat', '')
            query.message.delete()
            keyboard = [[InlineKeyboardButton('Cancel', callback_data='Stop')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.message.reply_text(text="Send me the Name of your prouct", reply_markup=reply_markup)
            self.current_item = 'Name'

        elif str(query.data) == 'Done':
            query.message.delete()
            product_name = str(self.name.replace(' ', '_'))
            keyboard = [[InlineKeyboardButton('Buy', url=f'http://t.me/kisoskbot?start={product_name}_')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            product_message = query.bot.send_photo(chat_id='@cataloguech',
                                                   photo=self.image,
                                                   caption=self.caption,
                                                   reply_markup=reply_markup)

            product_file = open(f'./{product_name}_.txt', 'w+')
            product_file.write(f'{self.image}$${self.caption}\nLink: {product_message.link} \nTag: {self.type}')
            query.message.reply_text(text="Viola! we\'re done")

        elif str(query.data) == "Done-t":
            query.message.delete()
            query.bot.send_message(chat_id='@kioskbg', text=f'/verified {self.buy_id} {self.delivery_time}')

        elif str(query.data) == "Change-t":
            query.message.delete()
            query.message.reply_text("How much time would the delivery take?")
            self.current_item = 'Deliverytime'

        elif str(query.data) == 'Cancel':
            self.image = ''
            self.caption = ''
            self.num_in_stock = 0
            self.description = ''
            self.value = 0
            self.current_item = 'N'
            query.message.delete()
            query.message.reply_text(text='Roger! Hope you continue next time')

    def verify(self, update: Update, context: CallbackContext) -> None:
        query_data = update.message.caption.split('--')
        self.chat_id = query_data[-1]
        update.message.reply_text("How much time would the delivery take?")
        self.current_item = 'Deliverytime'

    def status(self, update: Update, context: CallbackContext) -> None:
        pass

    def settings(self, update: Update, context: CallbackContext) -> None:
        pass

    def main(self) -> None:
        updater = Updater(Token)
        updater.dispatcher.add_handler(CommandHandler('start', self.start))
        updater.dispatcher.add_handler(CallbackQueryHandler(self.button))
        updater.dispatcher.add_handler(CommandHandler('help', self.help))
        updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Post'), self.post))
        updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Status'), self.status))
        updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Settings'), self.settings))
        updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'Help'), self.help))
        updater.dispatcher.add_handler(MessageHandler(Filters.regex(r'verify'), self.verify))
        updater.dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, self.controller))
        updater.start_polling()
        updater.idle()


bot().main()
