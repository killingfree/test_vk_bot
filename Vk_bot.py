import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from data import token, group_id
import logging

log = logging.getLogger('bot')


def configure_log():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler(filename='bot.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y,%H:%M'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot:

    def __init__(self, group_id, token):
        self.group_id = group_id
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)
        self.api = self.vk.get_api()

    def run(self):
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception('ошибка в обработке события')

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug('отправляем сообщение назад')
            self.api.messages.send(message='Я тебя понял, бери свое сообщение назад)' + ' ' + event.object.text,
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.peer_id
                                   )
        else:
            log.info('я пока не умею обрабатывать такое событие%s', event.type)


if __name__ == '__main__':
    configure_log()
    bot = Bot(group_id, token)
    bot.run()
