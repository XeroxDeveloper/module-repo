# Module developed by XeroxDeveloper
# For Heroku Userbot (https://github.com/coddrago/Heroku)
# Meta developer: @XeroxDevelopment

import os
from PIL import Image
from .. import loader, utils

@loader.tds
class Photo2GifMod(loader.Module):
    
    strings = {
        "name": "Photo2Gif",
        "no_reply": "<b>[Photo2Gif] Ошибка: Ответьте на фото!</b>",
        "no_photo": "<b>[Photo2Gif] Ошибка: Это не фото.</b>",
        "processing": "<b>[Photo2Gif] Конвертирую в GIF...</b>",
    }

    async def p2fcmd(self, message):

        reply = await message.get_reply_message()
        
        if not reply or not reply.media:
            await utils.answer(message, self.strings("no_reply"))
            return

        # Проверяем, что это именно фото или документ-картинка
        is_photo = False
        if hasattr(reply.media, 'photo'):
            is_photo = True
        elif hasattr(reply.media, 'document') and reply.media.document.mime_type.startswith('image/'):
            is_photo = True

        if not is_photo:
            await utils.answer(message, self.strings("no_photo"))
            return

        await utils.answer(message, self.strings("processing"))

        # Пути к файлам
        photo_path = await message.client.download_media(reply)
        gif_path = photo_path.rsplit(".", 1)[0] + ".gif"

        try:
            # Открываем изображение и сохраняем как GIF
            with Image.open(photo_path) as img:
                # Конвертируем в палитру GIF (опционально, сохраняет оригинальный размер)
                img.save(gif_path, "GIF")

            # Отправляем результат
            # Используем force_document=False, чтобы Телеграм мог распознать это как анимацию
            await message.client.send_file(
                message.chat_id, 
                gif_path, 
                reply_to=reply.id,
                video_note=False # Убеждаемся, что не кружок
            )
            
            # Удаляем сообщение "Конвертирую..."
            await message.delete()

        except Exception as e:
            await utils.answer(message, f"<b>Ошибка:</b> <code>{str(e)}</code>")
        
        finally:
            # Чистим временные файлы
            if os.path.exists(photo_path):
                os.remove(photo_path)
            if os.path.exists(gif_path):
                os.remove(gif_path)
