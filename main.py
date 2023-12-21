from typing import Union, Annotated
from fastapi import FastAPI, Request, Body, Depends, HTTPException, status, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Cookie
from pydantic import BaseModel
from uuid import uuid4
import datetime
import json
import os

color1 = 'F9F7F7'
color2 = 'DBE2EF'
color3 = '66bb6a'
color33 = '3F72AF'
color4 = '112D4E'

WEEKS = [6]

app = FastAPI()

class Solution(BaseModel):
    input: str

with open('backend/users.json') as f:
    users = json.load(f)

def handle_user(request: Request):
    try:
        user = request.cookies['username']
        pw = request.cookies['password']
        error = ''
        if user not in users:
            error = 'İsim hatalı'
        elif users[user]['password'] != pw:
            error = 'Şifre hatalı'
        if error:
            file = open('pages/login.html').read()
            index = file.find('</form>')
            file = file[:index] + open('pages/wrong.html').read().format(error) + file[index:]
            return HTMLResponse(content=file)
    except:
        file = open('pages/login.html').read()
        return HTMLResponse(content=file)



@app.get('/')
def root(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']
    page = open('pages/main.html').read()

    for week in range(6):
        item = open('pages/main_item.html').read()
        solved = len(users[user]['solved'][week])
        intime = len(users[user]['intime'][week])
        item = item.replace('{percent}', str(solved*10))
        item = item.replace('{puan}', str(intime+solved))
        item = item.replace('{hafta}', str(week+1))
        if week+1 not in WEEKS and user != 'cahid':
            item = item.replace('000', '888')
        else:
            item = item.replace('disabled ', '')
        page += item

    page += open('pages/main_end.html').read()


    page = page.replace('{background_color}', color1)
    page = page.replace('{progress_bar_empty_color}', color2)
    page = page.replace('{progress_bar_fill_color}', color3)
    page = page.replace('{border_color}', color4)
    page = page.replace('{text_color}', '000')

    return HTMLResponse(content=page)

@app.get("/login")
def main():
    file = open('pages/login.html').read()
    return HTMLResponse(content=file)

@app.get("/loginn")
async def login(username: str, password: str):
    response = RedirectResponse(url='/')
    response.set_cookie(key="username", value=username)
    response.set_cookie(key="password", value=password)
    return response

@app.get("/hafta/{week}")
def getWeek(request: Request, week: int):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']

    if len(users[user]['solved']) == 5:
        users[user]['solved'].append([])
        users[user]['intime'].append([])

    if not (0 < week <= max(WEEKS)):
        return RedirectResponse("/")

    if week == 6:
        page = open('pages/final.html').read()
    else:
        page = open('pages/week.html').read()

    for q in range(10):
        page = page.replace(f'{{name{q}}}', open(f'weeks/week{week}/q{q}/name.txt').read())
        page = page.replace(f'{{q{q}}}', color3 if q in users[user]['solved'][week-1] else color2)

    page = page.replace(f'{{q10}}', color3 if users[user]['golf'] >= 10 else color2)

    page = page.replace('{background_color}', color1)
    page = page.replace('{progress_bar_empty_color}', color2)
    page = page.replace('{progress_bar_fill_color}', color3)
    page = page.replace('{border_color}', color4)
    page = page.replace('{text_color}', '000')
    page = page.replace('{hafta}', str(week))


    return HTMLResponse(content=page)

@app.get("/hafta/{week}/{question}")
def getQuestion(request: Request, week: int, question: int):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']

    if not (0 < week <= max(WEEKS)) or not (0 <= question <= 10):
        return RedirectResponse("/")
    if week == 6 and 4 < question < 10:
        page = open('pages/sifrebul.html').read()
        page = page.replace('{kod}', open(f'weeks/week{week}/q{question}/kod.py').read())
        page = page.replace('{cikti}', open(f'weeks/week{week}/q{question}/cikti').read())
    elif week == 6 and question == 10:
        page = open('pages/codegolf.html').read()
        page = page.replace('{cikti}', open(f'weeks/week{week}/q{question}/cikti').read())
        page = page.replace('{puan}', str(users[user]['golf']))
    else:
        page = open('pages/soru.html').read()

        for i in range(10):
            if f'in{i}' in os.listdir(f'weeks/week{week}/q{question}'):
                if f'out{i}' not in os.listdir(f'weeks/week{week}/q{question}'):
                    os.system(f'python3 weeks/week{week}/q{question}/sol.py < weeks/week{week}/q{question}/in{i} > weeks/week{week}/q{question}/out{i}')
                sample = open('pages/soru_item.html').read()
                sample = sample.replace('{sampleinput}', open(f'weeks/week{week}/q{question}/in{i}').read())
                sample = sample.replace('{sampleoutput}', open(f'weeks/week{week}/q{question}/out{i}').read())
                page += sample

        page += open('pages/soru_end.html').read()

    page = page.replace('{statement}', open(f'weeks/week{week}/q{question}/q.html').read())
    page = page.replace('{qname}', open(f'weeks/week{week}/q{question}/name.txt').read())

    page = page.replace('{background_color}', color1)
    page = page.replace('{color2}', color2)
    page = page.replace('{color3}', color3)
    page = page.replace('{border_color}', color4)
    page = page.replace('{text_color}', '000')
    page = page.replace('{question}', str(question))
    page = page.replace('{week}', str(week))

    return HTMLResponse(content=page)



@app.post("/hafta/{week}/{question}")
def solve(request: Request, week: int, question: int, solution: Solution):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']
    if not (0 < week <= max(WEEKS)) or not (0 <= question <= 10):
        return {'result': 'illegal'}

    code = solution.input;
    # if 'import ' in code:
    #     return {'result': 'import yasak >:('}
    if 'eval(' in code:
        return {'result': 'eval yasak >:('}
    if 'exec(' in code:
        return {'result': 'exec yasak >:('}

    with open(f'codes/{user}/tmpinput', 'w') as f:
        f.write(' ')
    with open(f'codes/{user}/tmpoutput', 'w') as f:
        f.write(' ')
    with open(f'codes/{user}/tmperror', 'w') as f:
        f.write(' ')
    with open(f'codes/{user}/tmpexpected', 'w') as f:
        f.write(' ')

    codefile = f'codes/{user}/week{week}/q{question}/'
    os.system('mkdir -p ' + codefile)
    codefile += str(datetime.datetime.now()).replace(' ', '-')
    f = open(codefile, 'w')
    f.write(code)
    f.close()

    path = f'weeks/week{week}/q{question}/'

    if week == 6 and 4 < question < 10:
        correct = open(f'{path}sifre').read()
        if correct.strip() != code.strip():
            return {'result': 'Maalesef'}
    elif week == 6 and question == 10:
        correct = open(f'{path}cikti').read()
        result = os.system(f'timeout 1s python3 {codefile} >codes/{user}/tmpoutput 2> codes/{user}/tmperror')
        if result:
            return {'result': 'Maalesef'}
        output = open(f'codes/{user}/tmpoutput').read()
        if correct.strip() != output.strip():
            return {'result': 'Maalesef'}
        users[user]['golf'] = max(users[user]['golf'], 16-len(code)//60)
        print(users[user]['golf'])
        usersjson = open('backend/users.json', 'w')
        usersjson.write(json.dumps(users))
        usersjson.close()
        return {'result': 'success', 'codelen': str(len(code)), 'puan': str(16-len(code)//60), 'yenipuan': str(users[user]['golf'])}
    elif not os.path.exists(f'{path}check.py'):
        for _ in range(100):
            os.system(f'python3 {path}gen.py > codes/{user}/tmpinput')
            result = os.system(f'timeout 1s python3 {codefile} < codes/{user}/tmpinput > codes/{user}/tmpoutput 2> codes/{user}/tmperror')
            if result == 31744:
                return {
                        'result': 'Patladı :(',
                        'input': open(f'codes/{user}/tmpinput').read(),
                        'output': 'Ohoo kodun çalışması çok uzun sürdü.'
                        }
            elif result:
                return {
                        'result': 'Patladı :(',
                        'input': open(f'codes/{user}/tmpinput').read(),
                        'output': open(f'codes/{user}/tmperror').read(),
                        }
            os.system(f'python3 {path}sol.py < codes/{user}/tmpinput > codes/{user}/tmpexpected')
            result = os.system(f'diff -w codes/{user}/tmpoutput codes/{user}/tmpexpected')
            if result:
                return {
                        'result': 'Patladı :(',
                        'input': open(f'codes/{user}/tmpinput').read(),
                        'output': open(f'codes/{user}/tmpoutput').read(),
                        'expected': open(f'codes/{user}/tmpexpected').read()
                        }
    else:
        os.system(f'cp {codefile} codes/{user}/tmpcode.py')
        os.system(f'cp {path}check.py codes/{user}/tmpcheck.py')
        os.system(f'rm codes/{user}/tmperror')
        result = os.system(f'cd codes/{user}; timeout 10s python3 tmpcheck.py > tmpexpected 2> tmperror')
        if result:
            if not os.system(f'[ -s codes/{user}/tmperror ]'):
                return {
                        'result': 'Patladı :(',
                        'input': open(f'codes/{user}/tmpinput').read(),
                        'output': open(f'codes/{user}/tmperror').read(),
                        'expected': ''
                        }
            else:
                return {
                        'result': 'Patladı :(',
                        'input': open(f'codes/{user}/tmpinput').read(),
                        'output': open(f'codes/{user}/tmpoutput').read(),
                        'expected': open(f'codes/{user}/tmpexpected').read()
                        }



    codefile = f'codes/{user}/week{week}/q{question}/'
    os.system('mkdir -p ' + codefile)
    codefile += 'accepted.py'
    f = open(codefile, 'w')
    f.write(code)
    f.close()

    if question not in users[user]['solved'][week-1]:
        users[user]['solved'][week-1].append(question)
    if (datetime.datetime.now() < datetime.datetime(2023, 11, 18, 14, 0, 0, 0) + datetime.timedelta(days=7*(week-1))) and question < 5:
        if question not in users[user]['intime'][week-1]:
            users[user]['intime'][week-1].append(question)
    usersjson = open('backend/users.json', 'w')
    usersjson.write(json.dumps(users))
    usersjson.close()
    return {'result': 'success'}

@app.get('/scoreboard')
def scoreboard(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']
    page = open('pages/scoreboard.html').read()
    if len(users[user]['solved']) == 5:
        users[user]['solved'].append([])
        users[user]['intime'].append([])

    for week in range(5, max(WEEKS)):
        for q in range(11):
            qname = open(f'weeks/week{week+1}/q{q}/name.txt').read()

            if q in users[user]['solved'][week] or user == 'cahid':

                page += f'<th><div class="ver"><a href="bak/cahid/{week+1}/{q}">{qname}</a></div></th>'
            else:
                page += f'<th><div class="ver">{qname}</div></th>'
    page += f'<th><div class="ver">Toplam</div></th>'
    page += f'<td class="empty-column"></td>'

    page += " </tr> </thead> <tbody> "

    sirala = []

    for adam in users:
        if len(users[adam]['solved']) == 5:
            users[adam]['solved'].append([])
            users[adam]['intime'].append([])
        if 'golf' not in users[adam]:
            users[adam]['golf'] = 0
        if not users[adam]['show']:
            continue
        isim = users[adam]['fullname']
        part = f" <tr> <td><strong>{isim}</strong></td> "
        puan = 0
        for week in range(5, max(WEEKS)):
            for q in range(10):
                if q in users[adam]['solved'][week]:
                    if q in users[user]['solved'][week] or user == 'cahid':
                        part += f'<td class="solved"><a href="bak/{adam}/{week+1}/{q}">M</a></td>'
                    else:
                        part += '<td class="solved"></td>'
                    puan += 3
                else:
                    part += '<td></td>'
            if users[adam]['golf'] >= 10:
                part += f'<td class="solved">{users[adam]["golf"]}</td>'
            else:
                part += f'<td>{users[adam]["golf"]}</td>'
            puan += users[adam]['golf']
        part += f'<td>{puan}</td></tr>'
        sirala.append((puan, part))

    usersjson = open('backend/users.json', 'w')
    usersjson.write(json.dumps(users))
    usersjson.close()

    sirala.sort(reverse=True)
    for puan, part in sirala:
        page += part


    page = page.replace('{color1}', color1)
    page = page.replace('{color2}', color2)
    page = page.replace('{color3}', color3)
    page = page.replace('{color33}', color33)
    page = page.replace('{color4}', color4)
    page += '</tbody> </table> </body> </html>'

    return HTMLResponse(content=page)

@app.get('/bak/{ouser}/{week}/{question}')
def bak(request: Request, ouser: str, week: int, question: int):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies['username']
    try:
        if user != 'cahid' and question not in users[user]['solved'][week-1]:
            return "Illegal"
        page = open('pages/bak.html').read()
        page = page.replace('{color1}', color1)
        page = page.replace('{color2}', color2)
        page = page.replace('{color3}', color3)
        page = page.replace('{color33}', color33)
        page = page.replace('{color4}', color4)
        codefile = f'codes/{ouser}/week{week}/q{question}/accepted.py'
        if ouser == 'cahid':
            codefile = f'weeks/week{week}/q{question}/sol.py'
        page = page.replace('{code}', open(codefile).read().replace('\n', '<br>').replace(' ', '&nbsp;').replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;'))

    except Exception as e:
        return str(e)
    return HTMLResponse(content=page)
