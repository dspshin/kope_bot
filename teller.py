#!/usr/bin/python
# coding=utf-8
import sys
import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime
import re
import traceback

#텔레그램 상으로는 4096까지 지원함. 가독성상 1000정도로 끊자.
MAX_MSG_LENGTH = 1000

def sendMessage(id, msg):
    try:
        bot.sendMessage(id, msg)
    except:
        print str(datetime.now()).split('.')[0]
        traceback.print_exc(file=sys.stdout)

def help(id):
    sendMessage(id, '''아파트 전월세 정보 알림용 텔레그램 봇입니다.
명령어 사용법:
/noti add 지역코드 필터 : 노티 등록. howmuch의 사용법과 유사하며, 해당 결과가 있을 경우 매일 아침에 전송함(필터생략가능. 첫 노티는 전월 데이터도 전송됩니다).
 ex. /noti add 11710 잠실
/noti list : 노티 리스트 조회.
/noti remove 아이디 : 노티 제거.

자매품>
@apart_bot : 아파트 매매 봇
@officetel_bot : 연립/다세대 매매 봇
@house_meme_bot : 단독/다가구 매매 봇
@aptrent_bot : 아파트 전월세 봇
''')


def noti(command, user):
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT)')

    if command=='add':
        try:
            c.execute('INSERT INTO user (user) VALUES ("%s")'%(user))
            conn.commit()
        except:
            sendMessage(user, 'DB에러가 발생했습니다. 명렁어에 에러가 있나 살펴보시거나 잠시 후에 사용해 주세요.')
        else:
            sendMessage(user, '성공적으로 추가되었습니다. /noti list로 확인 가능합니다.')
        return True
    if command=='list':
        res=''
        printed = False
        c.execute('SELECT * from user WHERE user="%s"'%user)
        for data in c.fetchall():
            row = 'id:'+str(data[0])+'\n'
            if len(row+res)>MAX_MSG_LENGTH:
                sendMessage(user, res)
                res=row
                printed = True
            else:
                res+=row
        if res:
            sendMessage(user, res)
        elif not printed:
            sendMessage(user, '조회 결과가 없습니다.')
        return True
    if command=='remove':
        if not subparam:
            return False
        try:
            c.execute('DELETE FROM user WHERE user="%s"'%(user))
            conn.commit()
        except:
            sendMessage(user, 'DB에러가 발생했습니다. 명렁어에 에러가 있나 살펴보시거나 잠시 후에 사용해 주세요.')
        else:
            sendMessage(user, '성공적으로 제거되었습니다. /noti list로 확인 가능합니다.')
        return True
    if command=='all':
        res=''
        printed = False
        c.execute('SELECT * from user')
        for data in c.fetchall():
            row = 'id:'+str(data[0])+',user:'+data[1]+'\n'
            if len(row+res)>MAX_MSG_LENGTH:
                sendMessage(user, res)
                res=row
                printed = True
            else:
                res+=row
        if res:
            sendMessage(user, res)
        elif not printed:
            sendMessage(user, '조회 결과가 없습니다.')
        return True
    return False

def handle(msg):
    conn = sqlite3.connect('loc.db')
    c = conn.cursor()

    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return
    #pprint(msg)

    text = msg['text']
    args = text.split(' ')
    res = ''
    if text.startswith('/'):
        if text.startswith('/noti'):
            if len(args)>1:
                command = args[1]
                subparam = text.split(command)[1].strip()
                res = noti(command, subparam, chat_id)
                if res:
                    return

    help(chat_id)

TOKEN = sys.argv[1]
print 'received token :', TOKEN

bot = telepot.Bot(TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print 'Listening...'

while 1:
  time.sleep(10)
