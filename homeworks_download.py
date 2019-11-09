import homeworks_db as db
import homeworks_head as head

def down_main():
    for item in db.homeworks:
        if len(item) == 1:
            item = item[0]

            homework_id = item['id']
            result = head.get_homework(homework_id)
            attachments = result['attachments']
            text = ''
    pass