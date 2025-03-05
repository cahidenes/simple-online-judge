from typing import Union, Annotated, Any, List
from fastapi import FastAPI, Request, Body, Depends, HTTPException, status, APIRouter, Response
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import re
import os
from datetime import datetime
import ast
import markdown

color1 = 'F9F7F7'
color2 = 'DBE2EF'
color3 = '66bb6a'
color33 = '3F72AF'
color4 = '112D4E'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class Credentials(BaseModel):
    username: str
    password: str

class UserData(BaseModel):
    username: str
    password: str
    name: str
    visible: bool

class Sample(BaseModel):
    solution: str
    input: str = ""
    generator: str = ""

class Answer(BaseModel):
    input: str
    history: List[Union[int, str]]

DATA_DIR = os.path.expanduser('~/.config/simple-online-judge/')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
    os.system("cp data/* " + DATA_DIR)

with open(DATA_DIR + 'users.json') as f:
    users = json.load(f)
def save_users():
    with open(DATA_DIR + 'users.json', 'w') as f:
        json.dump(users, f)

with open(DATA_DIR + 'questions.json') as f:
    questions = json.load(f)
def save_questions():
    with open(DATA_DIR + 'questions.json', 'w') as f:
        json.dump(questions, f)

with open(DATA_DIR + 'sections.json') as f:
    sections = json.load(f)
def save_sections():
    with open(DATA_DIR + 'sections.json', 'w') as f:
        json.dump(sections, f)

with open(DATA_DIR + 'resources.json') as f:
    resources = json.load(f)
def save_resources():
    with open(DATA_DIR + 'resources.json', 'w') as f:
        json.dump(resources, f)


def handle_user(request: Request):
    user = request.cookies.get('username')
    password = request.cookies.get('password')
    if user not in users or users[user]['password'] != password:
        response = RedirectResponse(url='/login')
        return response

def get_group(content, keyword):
    content = content.split('\n')
    start = content.index(f'<!-- {keyword} -->')
    end = content.index(f'<!-- {keyword} end -->')
    group = '\n'.join(content[start+1:end])
    before = '\n'.join(content[:start])
    after = '\n'.join(content[end+1:])
    return group, before, after

def replace_keywords(content, **keywords):
    for keyword in keywords:
        content = content.replace(f'{{{{{keyword}}}}}', str(keywords[keyword]))
    return content

def remove_templates(content):
    content = re.sub(r'{{[^}]*}}', '', content)
    for keyword in re.findall(r'<!-- ([^ ]*) end -->', content):
        grup, before, after = get_group(content, keyword)
        content = before + after
    return content

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')

@app.get('/files/{dosya}')
def download(request: Request, dosya: str):
    return FileResponse(f'files/{dosya}')

@app.get('/')
def home(request: Request):
    return get_sections(request, 'questions')

@app.get('/resources')
def get_resources(request: Request):
    return get_sections(request, 'resources')

def get_sections(request: Request, type):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    with open('templates/main.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    if type == 'questions':
        content = replace_keywords(content, active_home='class="active"', active_resources='')
    elif type == 'resources':
        content = replace_keywords(content, active_home='', active_resources='class="active"')

    section_template, before, after = get_group(content, 'section')
    sorted_sections = sorted(sections.items(), key=lambda x: x[1]['order'])
    for section_id, section in sorted_sections:
        if user != 'admin' and not section['visible']:
            continue
        if type == 'questions' and section['resource']:
            continue
        if type == 'resources' and not section['resource']:
            continue

        total = 0
        done = 0
        for question_id in questions:
            if questions[question_id]['section'] != section_id:
                continue
            total += questions[question_id]['points']
            if question_id in users[user]['solves']:
                done += users[user]['solves'][question_id]['points']
        before += replace_keywords(section_template,
                                   section_id=section_id,
                                   disabled='' if user == 'admin' or section['active'] else 'disabled',
                                   name=section['title'],
                                   percent='0' if total == 0 else str(100 * done // total),
                                   label=f'{done} / {total}',
                                   visible='<img src="/files/visible.png"/>' if not section['visible'] else ('' if (section['active'] or user != 'admin') else '<img src="/files/disabled.png"/>'))

    content = before + after
    return HTMLResponse(content=content)

@app.get("/login")
async def login():
    with open('templates/login.html') as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.post("/login")
async def login(credentials: Credentials):
    username = credentials.username
    password = credentials.password
    if username not in users:
        response = JSONResponse(content={'error': 'Incorrect username'}, status_code=400)
    elif users[username]['password'] != password:
        response = JSONResponse(content={'error': 'Incorrect password'}, status_code=400)
    else:
        response = JSONResponse(content={}, status_code=200)
    response.set_cookie(key="username", value=username)
    response.set_cookie(key="password", value=password)
    return response

@app.get('/adduser')
def adduser(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/adduser.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    return HTMLResponse(content=content)

@app.post('/adduser')
def adduserpost(request: Request, userdata: UserData):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if userdata.username in users:
        return JSONResponse(content={'error': 'Username already exists'}, status_code=400)
    users[userdata.username] = {'password': userdata.password, 'name': userdata.name, 'visible': userdata.visible, 'solves': {}}
    save_users()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/listusers')
def listusers(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/listusers.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    user_template, before, after = get_group(content, 'user')
    for username in users:
        user = users[username]
        user_content = replace_keywords(user_template, username=username, name=user['name'], scoreboard='Yes' if user['visible'] else 'No')
        before += user_content
    content = before + after

    return HTMLResponse(content=content)

@app.get('/edituser/{username}')
def edituser(request: Request, username: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/edituser.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    content = replace_keywords(content, username=username, password=users[username]['password'], name=users[username]['name'], scoreboard='true' if users[username]['visible'] else 'false')
    return HTMLResponse(content=content)

@app.post('/edituser/{username}')
def edituser(request: Request, username: str, userdata: UserData):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    solves = users[username]['solves']
    del users[username]
    users[userdata.username] = {'password': userdata.password, 'name': userdata.name, 'visible': userdata.visible, 'solves': solves}
    save_users()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/addquestion')
def addquestion(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/addquestion.html') as f:
        content = f.read()
    content = replace_keywords(content,
                               default_selected="selected",
                               save_hidden="hidden")
    section_option, before, after = get_group(content, 'section_option')
    for sectionid, section in sections.items():
        if section['resource']:
            continue
        before += replace_keywords(section_option,
                                   value=sectionid,
                                   name=section['title'],
                                   selected='')
    content = remove_templates(before + after)
    return HTMLResponse(content=content)

@app.get('/editquestion/{question_id}')
def editquestion(request: Request, question_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/addquestion.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    question = questions[question_id]
    content = replace_keywords(content,
                               title=question['title'],
                               question=question['question'],
                               presolution=question['presolution'],
                               tmpsolution=question['tmpsolution'],
                               postsolution=question['postsolution'],
                               envfiles=question['envfiles'],
                               id=question_id,
                               points=question['points'],
                               add_hidden='hidden')

    section_option, before, after = get_group(content, 'section_option')
    for sectionid, section in sections.items():
        if section['resource']:
            continue
        before += replace_keywords(section_option,
                                   value=sectionid,
                                   name=section['title'],
                                   selected='selected' if sectionid == question['section'] else '')
    content = before + after

    if question['type'] == 'outputonly':
        content = replace_keywords(content, output_selected='selected')
        content = replace_keywords(content, outputonly_output=question['output'])
    elif question['type'] == 'testcaseonly':
        content = replace_keywords(content, testcase_selected='selected')
        testcasepair_template, before, after = get_group(content, 'testcaseonly_testcasepair')
        for testcasepair in question['testcases']:
            before += replace_keywords(testcasepair_template,
                                       testcaseonly_input=testcasepair['input'],
                                       testcaseonly_output=testcasepair['output'],
                                       testcaseonly_show='checked' if testcasepair['show'] else '')
        content = before + after
    elif question['type'] == 'solution':
        content = replace_keywords(content, solution_selected='selected')
        content = replace_keywords(content,
                                   solution_solution=question['solution'],
                                   solution_generator=question['generator'])
        testcasepair_template, before, after = get_group(content, 'solution_testcasepair')
        for testcasepair in question['testcases']:
            before += replace_keywords(testcasepair_template,
                                       solution_sampleinput=testcasepair['input'],
                                       solution_sampleoutput=testcasepair['output'])
        content = before + after
    elif question['type'] == 'checker':
        content = replace_keywords(content,
                                   checker_selected='selected',
                                   checker_checker=question['checker'])
    elif question['type'] == 'guessinput':
        content = replace_keywords(content,
                                   guessinput_selected='selected',
                                   guessinput_code=question['guessinputcode'],
                                   guessinput_output=question['output'],
                                   guessinput_input=question['input'])
    elif question['type'] == 'codegolf':
        content = replace_keywords(content,
                                   codegolf_selected='selected',
                                   codegolf_output=question['output'],
                                   codegolf_score=question['score'])
    elif question['type'] == 'manual':
        content = replace_keywords(content,
                                   manual_selected='selected')

    content = remove_templates(content)

    return HTMLResponse(content=content)


@app.post('/addquestion')
def addquestionpost(request: Request, question: Any = Body(None)):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    if question['id'] == '-1':
        id = '0' if (len(questions.keys()) == 0) else str(max(map(int, questions.keys())) + 1)
        question['id'] = id
    else:
        id = question['id']
    questions[id] = question

    if question['type'] == 'codegolf' and not question['title'].endswith('🚩'):
        question['title'] += ' 🚩'
    if question['type'] == 'guessinput' and not question['title'].endswith('🔍'):
        question['title'] += ' 🔍'

    save_questions()
    return JSONResponse(content={'success': True}, status_code=200)


@app.post('/samplerun')
def samplerun(request: Request, sample: Sample):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    if user != 'admin':
        try:
            ast = ast.parse(sample.solution)
            for node in ast.walk(ast):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    return JSONResponse({'error': 'Import statements are not allowed'})
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"open", "eval", "exec"}:
                        return JSONResponse({'error': f'{node.func.id} statements are not allowed'})
        except:
            pass

    if not os.path.exists(f'tmp/{user}'):
        os.makedirs(f'tmp/{user}')

    # clear directory
    os.system(f'rm -rf tmp/{user}/*')
    with open(f'tmp/{user}/solution.py', 'w') as f:
        f.write(sample.solution)
    if sample.generator:
        with open(f'tmp/{user}/generator.py', 'w') as f:
            f.write(sample.generator)
        os.system(f'python3 tmp/{user}/generator.py > tmp/{user}/input.txt')
    else:
        with open(f'tmp/{user}/input.txt', 'w') as f:
            f.write(sample.input)

    result = os.system(f'timeout 1s python3 tmp/{user}/solution.py < tmp/{user}/input.txt > tmp/{user}/output.txt 2> tmp/{user}/error.txt')
    if result == 31744:
        ret = {'error': 'Took too long to execute'}
    else:
        ret = {
            'input': open(f'tmp/{user}/input.txt').read(),
            'output': open(f'tmp/{user}/output.txt').read(),
            'error': open(f'tmp/{user}/error.txt').read()
            }
    return JSONResponse(content=ret)

@app.get('/listquestions')
def listquestions(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/listquestions.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    question_template, before, after = get_group(content, 'question')
    for id in questions:
        question = questions[id]
        desc = re.sub(r'</?(li|ul|ol|img)>', '', question['question'])
        question_content = replace_keywords(question_template, id=id, title=question['title'], description=desc, section='-' if question['section'] in ['-', 'default'] else sections[question['section']]['title'])
        before += question_content
    content = before + after
    return HTMLResponse(content=content)

@app.post('/deletequestion/{question_id}')
def deletequestion(request: Request, question_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    del questions[question_id]
    save_questions()
    content = replace_keywords(content, current_user=user)
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/addresource')
def addresource(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/addresource.html') as f:
        content = f.read()
    content = replace_keywords(content,
                               save_hidden="hidden")
    section_option, before, after = get_group(content, 'section_option')
    for sectionid, section in sections.items():
        if not section['resource']:
            continue
        before += replace_keywords(section_option,
                                   value=sectionid,
                                   name=section['title'],
                                   selected='')
    content = remove_templates(before + after)
    return HTMLResponse(content=content)

@app.get('/editresource/{resource_id}')
def editresource(request: Request, resource_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/addresource.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    resource = resources[resource_id]
    content = replace_keywords(content,
                               title=resource['title'],
                               text=resource['text'],
                               id=resource_id,
                               add_hidden='hidden')

    section_option, before, after = get_group(content, 'section_option')
    for sectionid, section in sections.items():
        if not section['resource']:
            continue
        before += replace_keywords(section_option,
                                   value=sectionid,
                                   name=section['title'],
                                   selected='selected' if sectionid == resource['section'] else '')
    content = remove_templates(before + after)

    return HTMLResponse(content=content)


@app.post('/addresource')
def addresourcepost(request: Request, resource: Any = Body(None)):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    if resource['id'] == '-1':
        id = '0' if (len(resources.keys()) == 0) else str(max(map(int, resources.keys())) + 1)
        resource['id'] = id
    else:
        id = resource['id']
    resources[id] = resource

    save_resources()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/listresources')
def listresources(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/listresources.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    resource_template, before, after = get_group(content, 'resource')
    for id in resources:
        resource = resources[id]
        resource_content = replace_keywords(resource_template,
                                            id=id,
                                            title=resource['title'],
                                            text=resource['text'],
                                            section='-' if resource['section'] in ['-', 'default'] else (sections[resource['section']]['title'] if resource['section'] in sections else 'Deleted Section'))
        before += resource_content
    content = before + after
    return HTMLResponse(content=content)

@app.post('/deleteresource/{resource_id}')
def deleteresource(request: Request, resource_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    del resources[resource_id]
    save_resources()
    content = replace_keywords(content, current_user=user)
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/resource/{resource_id}')
def get_resource(request: Request, resource_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    resource = resources[resource_id]
    section = sections[resource['section']]
    if not section['active'] or not section['visible']:
        return RedirectResponse('/')

    with open('templates/resource.html') as f:
        content = f.read()
    
    import re
    text = resource['text']

    text = re.sub(r'^\| (.+)$', r'<p class="round">\1</p>', text, flags=re.MULTILINE)

    text = re.sub(r'```\n([^`]+?)\n---\n([^`]+?)\n```',
                  r'''
<div style="display: flex;">
    <b style="width: 75%">
        Code:
    </b>
    <b style="width: 24%; padding-left: 1%;">
        Input:
    </b>
</div>
<div style="display: flex;">
    <div class="user-input" style="width: 75%">
        <div class="editor" style="width:100%; min-height:100px;">\1</div>
    </div>
    <div class="user-input" style="width: 24%; font-size: 18px; margin-left: 1%;">
        <div class="editor-input" style="width:100%; min-height:100px;">\2</div>
    </div>
</div>
<div style="display: flex;">
    <div class="button" onclick="runCode(this)" style="align-items: center; display: flex;"><div class="triangle"></div></div>
    <div class="user-input" style="width: 100%; margin-top: 10px; margin-left: 10px;"></div>
</div>
''', 
                  text, flags=re.MULTILINE | re.DOTALL)

    text = re.sub(r'```\n([^`]+?)\n```',
                  r'''
<div style="display: flex;">
    <div class="user-input" style="width:100%">
        <div class="editor" style="width:100%; min-height:100px;">\1</div>
    </div>
</div>
<div style="display: flex;">
    <div class="button" onclick="runCode(this)" style="align-items: center; display: flex;"><div class="triangle"></div></div>
    <div class="user-input" style="width: 100%; margin-top: 10px; margin-left: 10px;"></div>
</div>
''', 
                  text, flags=re.MULTILINE | re.DOTALL)

    text = markdown.markdown(text)

    content = replace_keywords(content,
                               current_user=user,
                               title=resource['title'],
                               text=text)

    return HTMLResponse(content=content)

@app.get('/listsections')
def listsections(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/listsections.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    section_template, before, after = get_group(content, 'section')
    for id in sections:
        section = sections[id]
        question_list = []
        for question_id in questions:
            question = questions[question_id]
            if question['section'] == id:
                question_list.append(question['title'])
        section_content = replace_keywords(section_template,
                                           id=id,
                                           title=section['title'],
                                           visible='checked' if section['visible'] else '',
                                           active='checked' if section['active'] else '',
                                           resource='checked' if section['resource'] else '',
                                           order=section['order'],
                                           questions=', '.join(question_list))
        before += section_content
    content = before + after
    return HTMLResponse(content=content)

@app.post('/addsection')
def addsection(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    id = str(max(map(int, sections.keys())) + 1) if sections.keys() else '0'
    sections[id] = {'title': 'New Section', 'visible': False, 'active': False, 'resource': False, 'order': 0}
    save_sections()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/savesections')
def savesections(request: Request, new_sections: Any = Body(None)):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    global sections
    sections = new_sections
    save_sections()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/deletesection/{id}')
def deletesection(request: Request, id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    for question_id in questions:
        if questions[question_id]['section'] == id:
            break
    else:
        del sections[id]
        return JSONResponse(content={'success': True}, status_code=200)
    return JSONResponse(content={'error': 'The section has questions'})

@app.get('/section/{section_id}')
def getsection(request: Request, section_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    with open('templates/section.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    if section_id not in sections or sections[section_id]['active'] == False or sections[section_id]['visible'] == False:
        if user != 'admin':
            return RedirectResponse('/')
    
    if sections[section_id]['resource']:
        content = replace_keywords(content, type='resource')
    else:
        content = replace_keywords(content, type='question')

    question_template, before, after = get_group(content, 'question')

    if sections[section_id]['resource']:
        for resource_id in resources:
            if resources[resource_id]['section'] != section_id:
                continue
            before += replace_keywords(question_template, id=resource_id, title=resources[resource_id]['title'], done='notdone')
    else:
        sorted_questions = sorted(questions.items(), key=lambda x: x[1]['points'])
        for question_id, _ in sorted_questions:
            if questions[question_id]['section'] != section_id:
                continue
            done = 'notdone'
            if question_id in users[user]['solves']:
                if users[user]['solves'][question_id]['points'] > 0:
                    done = 'partiallydone'
                if users[user]['solves'][question_id]['points'] == questions[question_id]['points']:
                    done = 'done'

            before += replace_keywords(question_template, id=question_id, title=questions[question_id]['title'], done=done)

    content = before + after

    return HTMLResponse(content=content)


@app.get('/question/{question_id}')
def get_question(request: Request, question_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    question = questions[question_id]
    section = sections[question['section']]
    if not section['active'] or not section['visible']:
        if user != 'admin':
            return RedirectResponse('/')

    with open('templates/question.html') as f:
        content = f.read()
    
    content = replace_keywords(content,
                               current_user=user,
                               qname=question['title'],
                               statement=question['question'],
                               codegolfscoring=f'<b>Scoring:</b> {question["points"]} * ({question["score"]})' if question['type'] == 'codegolf' else '',
                               presolution=question['presolution'].replace('\n', '\\n'),
                               tmpsolution=question['tmpsolution'].replace('\n', '\\n'),
                               postsolution=question['postsolution'].replace('\n', '\\n'),
                               score=question['points'])
    
    guess_input_template, before, _ = get_group(content, 'guessinput')
    input_form_template, _, after = get_group(content, 'inputform')

    if question['type'] == 'guessinput':
        content = before + replace_keywords(guess_input_template,
                                            output=question['output'].replace('\n', '<br>')) + \
                replace_keywords(after, guessinputcode=question['guessinputcode'].replace('\n', '\\n'))

    else:
        content = before + input_form_template + after

    sample_template, before, after = get_group(content, 'sample')
    if 'testcases' in question:
        for testcase in question['testcases']:
            if not 'show' in testcase or testcase['show']:
                before += replace_keywords(sample_template, input=testcase['input'], output=testcase['output'])
    content = before + after

    return HTMLResponse(content=content)


@app.post('/question/{question_id}')
def evaluate(request: Request, question_id: str, answer: Answer):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    question = questions[question_id]
    section = sections[question['section']]
    if not section['active'] or not section['visible']:
        return JSONResponse({'error': 'Not allowed'})

    # Save attempt to tries
    time = datetime.now()
    time = time.strftime('%Y-%m-%d %H:%M:%S')
    if question_id not in users[user]['solves']:
        users[user]['solves'][question_id] = {'points': 0, 'best_solution': None, 'tries': []}
    users[user]['solves'][question_id]['tries'].append({'time': time, 'code': answer.input, 'history': answer.history})
    save_users()

    # Check if forbidden statements are used
    try:
        tree = ast.parse(answer.input)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                return JSONResponse({'error': 'Import statements are not allowed'})
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in {"open", "eval", "exec"}:
                    return JSONResponse({'error': f'{node.func.id} statements are not allowed'})
    except:
        pass

    def get(filename):
        with open(dir + '/' + filename) as f:
            data = f.read()
        return data

    points = 0
    msg = ''
    dir = f'tmp/{user}'
    os.system(f'mkdir -p {dir}')
    os.system(f'rm -f {dir}/*')
    for envfile in question['envfiles'].split(','):
        if envfile:
            os.system(f'cp files/{envfile.strip()} {dir}/{envfile.strip()}')

    if question['type'] == 'solution':
        with open(dir + '/solution.py', 'w') as f:
            f.write(question['solution'])
        with open(dir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(dir + '/generator.py', 'w') as f:
            f.write(question['generator'])


        for i in range(100):
            result = os.system(f'python3 {dir}/generator.py > {dir}/input.txt 2> {dir}/generator_error.txt')
            if result:
                return JSONResponse({'error': 'An error occured when generating input: ' + get('generator_error.txt')})

            with open(f'{dir}/output.txt', 'w') as f:
                f.write('No output is generated')
            with open(f'{dir}/error.txt', 'w') as f:
                f.write('No error is generated')
            result = os.system(f'timeout 1s python3 {dir}/code.py < {dir}/input.txt > {dir}/output.txt 2> {dir}/error.txt')
            if result:
                if result == 31744:
                    return JSONResponse({'error': 'Took too long to execute', 'input': get('input.txt')})
                else:
                    return JSONResponse({'error': get('error.txt'), 'input': get('input.txt')})

            result = os.system(f'python3 {dir}/solution.py < {dir}/input.txt > {dir}/expected.txt 2> {dir}/solution_error.txt')
            if result:
                return JSONResponse({'error': 'An error occured when generating solution: ' + get('solution_error.txt')})

            if os.system(f'diff -w {dir}/output.txt {dir}/expected.txt > /dev/null'):
                return JSONResponse({'input': get('input.txt'), 'output': get('output.txt'), 'expected': get('expected.txt')}) 
        points = 1
    elif question['type'] == 'checker':
        with open(dir + '/checker.py', 'w') as f:
            f.write(question['checker'])
        with open(dir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{dir}/output.txt', 'w') as f:
            f.write('No output is generated')

        result = os.system(f'python3 {dir}/checker.py > {dir}/output.txt 2> {dir}/error.txt')
        if result:
            error = get('error.txt')
            output = get('output.txt')
            if error:
                return JSONResponse({'error': error})
            else:
                return JSONResponse({'error': output})
        else:
            points = 1
    elif question['type'] == 'outputonly':
        with open(dir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{dir}/output.txt', 'w') as f:
            f.write('No output is generated')
        error_code = os.system(f'python3 {dir}/code.py > {dir}/output.txt 2> {dir}/error.txt')

        if error_code:
            error = get('error.txt')
            output = get('output.txt')
            if error:
                return JSONResponse({'error': error})
            else:
                return JSONResponse({'error': output})
        else:
            output = get('output.txt')
            expected = question['output']
            if output.strip() != expected.strip():
                return JSONResponse({'error': 'Your output is not correct'})
            else:
                points = 1
    elif question['type'] == 'guessinput':
        with open(dir + '/code.py', 'w') as f:
            f.write(answer.input)
        if answer.input.strip() == question['input'].strip():
            points = 1
        else:
            points = 0
    elif question['type'] == 'testcaseonly':
        with open(dir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])

        for testcase in question['testcases']:
            with open(f'{dir}/output.txt', 'w') as f:
                f.write('No output is generated')
            with open(f'{dir}/error.txt', 'w') as f:
                f.write('No error is generated')
            with open(f'{dir}/input.txt', 'w') as f:
                f.write(testcase['input'])

            result = os.system(f'timeout 1s python3 {dir}/code.py < {dir}/input.txt > {dir}/output.txt 2> {dir}/error.txt')
            if result:
                if result == 31744:
                    return JSONResponse({'error': 'Took too long to execute', 'input': get('input.txt')})
                else:
                    if testcase['show']:
                        return JSONResponse({'error': get('error.txt'), 'input': get('input.txt')})
                    else:
                        return JSONResponse({'error': get('error.txt'), 'input': 'Hidden'})

            output = get('output.txt')
            if output.strip() != testcase['output'].strip():
                if testcase['show']:
                    return JSONResponse({'input': get('input.txt'), 'output': get('output.txt'), 'expected': testcase['output'].strip()}) 
                else:
                    return JSONResponse({'error': 'Your output is not correct on a hidden testcase'})
        points = 1
    elif question['type'] == 'codegolf':
        with open(dir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{dir}/output.txt', 'w') as f:
            f.write('No output is generated')
        error_code = os.system(f'python3 {dir}/code.py > {dir}/output.txt 2> {dir}/error.txt')

        if error_code:
            error = get('error.txt')
            output = get('output.txt')
            if error:
                return JSONResponse({'error': error})
            else:
                return JSONResponse({'error': output})
        else:
            output = get('output.txt')
            expected = question['output']
            if output.strip() != expected.strip():
                return JSONResponse({'error': 'Your output is not correct'})
            else:
                length = len(answer.input)
                points = max(0, min(1, eval(question['score'].replace('c', str(length)))))
                msg = f"Character count: {length}\n" \
                      f"Score: {int(points * questions[question_id]['points'])}/{questions[question_id]['points']}"
    elif question['type'] == 'manual':
        users[user]['solves'][question_id]['waiting'] = True
        save_users()
        return JSONResponse({'result': 'submitted', 'error': 'Your solution is submitted and will be evaluated'})

    users[user]['solves'][question_id]['points'] = int(points * questions[question_id]['points'])
    users[user]['solves'][question_id]['best_solution'] = {'time': time, 'code': answer.input}
    save_users()
    response = {}
    if msg:
        response['error'] = msg
    if points == 1:
        response['result'] = 'success'
    elif points == 0:
        response['result'] = 'wrong'
    else:
        response['result'] = 'partial'
    return JSONResponse(response)

@app.post('/judge')
def submit_judge(request: Request, body: Any = Body(None)):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return JSONResponse({'error': 'Not allowed'})
    
    if body['points'] == True:
        body['points'] = questions[body['question_id']]['points']
    elif body['points'] == False:
        body['points'] = 0

    if body['question_id'] not in users[body['username']]['solves']:
        print('here')
        users[body['username']]['solves'][body['question_id']] = {
            'best_solution': {'time': '', 'code': ''}, 
            'tries': [{
                'time': '',
                'code': '',
                'history': ['']
            }]}
        
    users[body['username']]['solves'][body['question_id']]['waiting'] = False
    users[body['username']]['solves'][body['question_id']]['points'] = body['points']
    if body['points'] == questions[body['question_id']]['points']:
        users[body['username']]['solves'][body['question_id']]['best_solution'] = users[body['username']]['solves'][body['question_id']]['tries'][-1]
    
    save_users()
    
    return JSONResponse({'result': 'success'})

@app.get('/scoreboard')
def get_scoreboard(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    with open('templates/scoreboard.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    active_questions = []
    sorted_sections = []
    for section_id in sections:
        section = sections[section_id]
        if section['visible']:
            sorted_sections.append((section['order'], section_id))

    sorted_sections.sort()
    for _, section_id in sorted_sections:
        sorted_questions = sorted(questions.items(), key=lambda q: q[1]['points'])
        for question_id, question in sorted_questions:
            if question['section'] == section_id:
                active_questions.append(question_id)

    question_template, before, after = get_group(content, 'question')
    for question_id in active_questions:
        before += replace_keywords(question_template, onclick=f"window.location.href = '/question/{question_id}'", name=questions[question_id]['title'])

    content = before + after

    user_template, before, after = get_group(content, 'user')
    user_strings = []
    for username in users:
        if users[username]['visible'] == False:
            continue
        solved_template, user_before, user_after = get_group(user_template, 'solved')
        user_before = replace_keywords(user_before, name=users[username]['name'])

        total_point = 0
        for question_id in active_questions:
            point = 0 if question_id not in users[username]['solves'] else users[username]['solves'][question_id]['points']
            user_point = 0 if question_id not in users[user]['solves'] else users[user]['solves'][question_id]['points']
            expected = questions[question_id]['points']

            if question_id in users[username]['solves'] and 'waiting' in users[username]['solves'][question_id] and users[username]['solves'][question_id]['waiting'] == True:  state = replace_keywords(solved_template, solved='waiting')
            elif point <= 0:        state = replace_keywords(solved_template, solved='unsolved')
            elif point < expected:  state = replace_keywords(solved_template, solved='partially_solved')
            else:                   state = replace_keywords(solved_template, solved='solved')

            if user_point >= expected or user == 'admin':
                onclick = f"location.href='/viewcode/{username}/{question_id}'"
                cursor = "pointer"
            else:
                onclick = ""
                cursor = "default"
            user_before += replace_keywords(state, onclick=onclick, point=point, cursor=cursor)
            total_point += point

        user_before += replace_keywords(solved_template, solved="unsolved", onclick="", point=total_point)
        user_strings.append((total_point, user_before + user_after))

    user_strings.sort(reverse=True)
    for _, user_string in user_strings:
        before += user_string

    content = before + after

    return HTMLResponse(content=content)

@app.get('/viewcode/{username}/{question_id}')
def viewcode(request: Request, username: str, question_id: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    user_point = 0 if question_id not in users[user]['solves'] else users[user]['solves'][question_id]['points']
    expected = questions[question_id]['points']
    if user_point < expected and user != 'admin':
        return RedirectResponse('/scoreboard')

    with open('templates/view_code.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user, username=username, question_id=question_id)
    code = []
    if username == 'solution':
        if 'solution' in questions[question_id]:
            code = [{
                'time': 'Solution',
                'code': questions[question_id]['solution']
                }]
        else:
            code = [{
                'time': 'Solution',
                'code': 'No solution provided'
                }]
    elif question_id in users[username]['solves']:
        code = [users[username]['solves'][question_id]['best_solution']]
        if user == 'admin':
            code = users[username]['solves'][question_id]['tries'] + code
    
    content = replace_keywords(content, codes=json.dumps(code))
    return HTMLResponse(content=content)

@app.get('/files')
def files(request: Request):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    with open('templates/files.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    file_template, before, after = get_group(content, 'file')
    for filename in os.listdir('files'):
        filetype = filename.split('.')[-1]
        before += replace_keywords(file_template, filename=filename, filetype=filetype)
        
    content = before + after
    return HTMLResponse(content=content)

@app.get('/editfile/{filename}')
def show_file(request: Request, filename: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')

    with open('templates/editfile.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    file_content = open(f'files/{filename}').read()
    content = replace_keywords(content, filename=filename, file_content=file_content)
    
    return HTMLResponse(content=content)

@app.post('/editfile/{filename}')
def newfile(request: Request, filename: str, body: Any = Body(None)):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    print("Editfile: ", filename)
    with open('files/' + filename, 'w') as f:
        f.write(body['content'])
    return JSONResponse(content='{}')

@app.post('/deletefile/{filename}')
def deletefile(request: Request, filename: str):
    if handle_user(request):
        return handle_user(request)
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    os.system(f'rm -f files/{filename}')
    return JSONResponse(content='{}')