from typing import Union, Any, List
from fastapi import FastAPI, Request, Body, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
import re
import os
import shutil
from datetime import datetime
import ast
import markdown

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
    for _seed_file in os.listdir('data'):
        shutil.copy(os.path.join('data', _seed_file), os.path.join(DATA_DIR, _seed_file))

with open(DATA_DIR + 'users.json') as f:
    users = json.load(f)
def save_users():
    with open(DATA_DIR + 'users.json', 'w') as f:
        json.dump(users, f)

def normalize_tags(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(t).strip() for t in value if str(t).strip()]
    return [t.strip() for t in str(value).split(',') if t.strip()]

with open(DATA_DIR + 'questions.json') as f:
    questions = json.load(f)
    for question in questions.values():
        if 'order' not in question:
            question['order'] = 0
        if 'tags' not in question:
            question['tags'] = []
def save_questions():
    with open(DATA_DIR + 'questions.json', 'w') as f:
        json.dump(questions, f)

with open(DATA_DIR + 'sections.json') as f:
    sections = json.load(f)
    for section in sections.values():
        section.pop('resource', None)
def save_sections():
    with open(DATA_DIR + 'sections.json', 'w') as f:
        json.dump(sections, f)

with open(DATA_DIR + 'resources.json') as f:
    resources = json.load(f)
    for resource in resources.values():
        if 'order' not in resource:
            resource['order'] = 0
        if 'tags' not in resource:
            resource['tags'] = []
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
        group, before, after = get_group(content, keyword)
        content = before + after
    return content

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse('static/favicon.ico')

def is_safe_filename(filename: str) -> bool:
    return bool(filename) and '/' not in filename and '\\' not in filename and '..' not in filename


@app.get('/files/{dosya}')
def download(request: Request, dosya: str):
    if not is_safe_filename(dosya):
        raise HTTPException(status_code=404)
    return FileResponse(os.path.join('files', dosya))

@app.get('/')
def home(request: Request):
    return get_sections(request, 'questions')

@app.get('/resources')
def get_resources(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    with open('templates/section.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    content = replace_keywords(content, type='resource')

    question_template, before, after = get_group(content, 'question')

    sorted_resources = sorted(resources.items(), key=lambda x: x[1].get('order', 0))
    for resource_id, resource in sorted_resources:
        before += replace_keywords(question_template, id=resource_id, title=resource['title'], done='notdone')

    content = before + after

    return HTMLResponse(content=content)

def get_sections(request: Request, section_type):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    with open('templates/main.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    if section_type == 'questions':
        content = replace_keywords(content, active_home='class="active"', active_resources='')
    elif section_type == 'resources':
        content = replace_keywords(content, active_home='', active_resources='class="active"')

    section_template, before, after = get_group(content, 'section')
    sorted_sections = sorted(sections.items(), key=lambda x: (x[1].get('order', 0), x[0]))
    for section_id, section in sorted_sections:
        if user != 'admin' and not section.get('visible'):
            continue

        total = 0
        done = 0
        for question_id in questions:
            if questions[question_id].get('section') != section_id:
                continue
            total += questions[question_id].get('points', 0)
            if question_id in users[user]['solves']:
                done += users[user]['solves'][question_id].get('points', 0)
        icons = ''
        if not section.get('visible'):
            icons += '<img src="/files/visible.png" alt=""/>'
        elif not section.get('active'):
            icons += '<img src="/files/disabled.png" alt=""/>'
        elif not section.get('points'):
            icons += '<img src="/files/nopoint.png" alt=""/>'
            
        before += replace_keywords(section_template,
                                   section_id=section_id,
                                   disabled='' if user == 'admin' or section.get('active') else 'disabled',
                                   name=section['title'],
                                   percent='0' if total == 0 else str(100 * done // total),
                                   label=f'{done} / {total}',
                                   visible=icons)

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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/adduser.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    return HTMLResponse(content=content)

@app.post('/adduser')
def adduserpost(request: Request, userdata: UserData):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/listusers.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    user_template, before, after = get_group(content, 'user')
    for username in users:
        listed_user = users[username]
        user_content = replace_keywords(user_template, username=username, name=listed_user['name'], scoreboard='Yes' if listed_user['visible'] else 'No')
        before += user_content
    content = before + after

    return HTMLResponse(content=content)

@app.get('/edituser/{username}')
def edituser(request: Request, username: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if username not in users:
        return RedirectResponse(url='/listusers')
    with open('templates/edituser.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    content = replace_keywords(content, username=username, password=users[username]['password'], name=users[username]['name'], scoreboard='true' if users[username]['visible'] else 'false')
    return HTMLResponse(content=content)

@app.post('/edituser/{username}')
def edituser(request: Request, username: str, userdata: UserData):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if username not in users:
        return JSONResponse(content={'error': 'User not found'}, status_code=404)
    solves = users[username]['solves']
    del users[username]
    users[userdata.username] = {'password': userdata.password, 'name': userdata.name, 'visible': userdata.visible, 'solves': solves}
    save_users()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/addquestion')
def addquestion(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
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
        before += replace_keywords(section_option,
                                   value=sectionid,
                                   name=section['title'],
                                   selected='')
    content = remove_templates(before + after)
    return HTMLResponse(content=content)

@app.get('/editquestion/{question_id}')
def editquestion(request: Request, question_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/addquestion.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    if question_id not in questions:
        return RedirectResponse(url='/listquestions')
    question = questions[question_id]
    content = replace_keywords(content,
                               title=question['title'],
                               question=question['question'],
                               presolution=question['presolution'],
                               tmpsolution=question['tmpsolution'],
                               postsolution=question['postsolution'],
                               solution_solution=question['solution'] if 'solution' in question else '',
                               envfiles=question['envfiles'],
                               id=question_id,
                               points=question['points'],
                               order=question.get('order', 0),
                               tags=', '.join(normalize_tags(question.get('tags', []))),
                               add_hidden='hidden')

    section_option, before, after = get_group(content, 'section_option')
    for sectionid, section in sections.items():
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
                                   guessinput_code=question['guessinputcode'].replace('"', '\\"'),
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    if question['id'] == '-1':
        id = '0' if (len(questions.keys()) == 0) else str(max(map(int, questions.keys())) + 1)
        question['id'] = id
    else:
        id = question['id']
    if 'order' not in question:
        if id in questions:
            question['order'] = questions[id].get('order', 0)
        else:
            same = [q.get('order', 0) for q in questions.values()
                    if q.get('section') == question.get('section')]
            question['order'] = (max(same) + 1) if same else 0
    question['tags'] = normalize_tags(question.get('tags', []))
    questions[id] = question

    if question['type'] == 'codegolf' and not question['title'].endswith('🚩'):
        question['title'] += ' 🚩'
    if question['type'] == 'guessinput' and not question['title'].endswith('🔍'):
        question['title'] += ' 🔍'

    save_questions()
    return JSONResponse(content={'success': True}, status_code=200)


@app.post('/samplerun')
def samplerun(request: Request, sample: Sample):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    if user != 'admin':
        try:
            parsed = ast.parse(sample.solution)
            for node in ast.walk(parsed):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    return JSONResponse({'error': 'Import statements are not allowed'})
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"open", "eval", "exec"}:
                        return JSONResponse({'error': f'{node.func.id} statements are not allowed'})
        except Exception:
            pass

    if not os.path.exists(f'tmp/{user}'):
        os.makedirs(f'tmp/{user}')

    # clear directory
    for _tmp_file in os.listdir(f'tmp/{user}'):
        _tmp_path = os.path.join(f'tmp/{user}', _tmp_file)
        if os.path.isfile(_tmp_path):
            os.remove(_tmp_path)
    with open(f'tmp/{user}/solution.py', 'w') as f:
        f.write(sample.solution)
    if sample.generator:
        with open(f'tmp/{user}/generator.py', 'w') as f:
            f.write(sample.generator)
        result = os.system(f'timeout 5s python3 tmp/{user}/generator.py > tmp/{user}/input.txt 2> tmp/{user}/generator_error.txt')
        if result:
            if result == 31744:
                ret = {'error': 'Took too long to execute'}
            else:
                with open(f'tmp/{user}/input.txt') as f:
                    _gen_input = f.read()
                with open(f'tmp/{user}/generator_error.txt') as f:
                    _gen_error = f.read()
                ret = {
                    'input': '',
                    'output': _gen_input,
                    'error': _gen_error
                    }
            return JSONResponse(content=ret)
    else:
        with open(f'tmp/{user}/input.txt', 'w') as f:
            f.write(sample.input)

    result = os.system(f'timeout 1s python3 tmp/{user}/solution.py < tmp/{user}/input.txt > tmp/{user}/output.txt 2> tmp/{user}/error.txt')
    if result == 31744:
        ret = {'error': 'Took too long to execute'}
    else:
        with open(f'tmp/{user}/input.txt') as f:
            _run_input = f.read()
        with open(f'tmp/{user}/output.txt') as f:
            _run_output = f.read()
        with open(f'tmp/{user}/error.txt') as f:
            _run_error = f.read()
        ret = {
            'input': _run_input,
            'output': _run_output,
            'error': _run_error
            }
    return JSONResponse(content=ret)

@app.get('/listquestions')
def listquestions(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/listquestions.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    question_template, before, after = get_group(content, 'question')

    def section_key(item):
        sid, section = item
        return (section.get('order', 0), sid)

    real_sections = sorted(
        list(sections.items()),
        key=section_key,
    )

    grouped = {sid: [] for sid, _ in real_sections}
    ungrouped = []
    for qid, question in questions.items():
        sid = question.get('section', '-')
        if sid in grouped:
            grouped[sid].append((qid, question))
        else:
            ungrouped.append((qid, question))

    body = ''
    for sid, section in real_sections:
        body += (
            f'<div class="section-group" data-section-id="{sid}">'
            f'<div class="round section-header"><span class="collapse-arrow">▼</span><b>{section["title"]}</b></div>'
        )
        for qid, question in sorted(grouped[sid], key=lambda x: (x[1].get('order', 0), x[0])):
            tags = normalize_tags(question.get('tags', []))
            body += replace_keywords(question_template,
                                     id=qid,
                                     title=question['title'],
                                     section_id=sid,
                                     order=question.get('order', 0),
                                     tags=', '.join(tags),
                                     tags_attr=', '.join(tags))
        body += '</div>'
    if ungrouped:
        body += (
            '<div class="section-group" data-section-id="-">'
            '<div class="round section-header"><span class="collapse-arrow">▼</span><b>No section</b></div>'
        )
        for qid, question in sorted(ungrouped, key=lambda x: (x[1].get('order', 0), x[0])):
            tags = normalize_tags(question.get('tags', []))
            body += replace_keywords(question_template,
                                     id=qid,
                                     title=question['title'],
                                     section_id='-',
                                     order=question.get('order', 0),
                                     tags=', '.join(tags),
                                     tags_attr=', '.join(tags))
        body += '</div>'
    content = before + body + after
    return HTMLResponse(content=content)

@app.post('/savequestionsorder')
def savequestionsorder(request: Request, body: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if not isinstance(body, dict):
        body = {}
    if 'groups' in body and isinstance(body['groups'], list):
        for group in body['groups']:
            sid = group.get('section', '-')
            ids = group.get('ids', [])
            for index, qid in enumerate(ids):
                if qid in questions:
                    if sid in sections:
                        questions[qid]['section'] = sid
                    questions[qid]['order'] = index
    else:
        order = body.get('order', [])
        for index, qid in enumerate(order):
            if qid in questions:
                questions[qid]['order'] = index
    save_questions()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/saveresourcesorder')
def saveresourcesorder(request: Request, body: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    order = body.get('order', []) if isinstance(body, dict) else []
    for index, rid in enumerate(order):
        if rid in resources:
            resources[rid]['order'] = index
    save_resources()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/deletequestion/{question_id}')
def deletequestion(request: Request, question_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if question_id not in questions:
        return JSONResponse(content={'error': 'Question not found'}, status_code=404)
    del questions[question_id]
    save_questions()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/addresource')
def addresource(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/addresource.html') as f:
        content = f.read()
    content = replace_keywords(content,
                               current_user=user,
                               order=0,
                               save_hidden="hidden")
    content = remove_templates(content)
    return HTMLResponse(content=content)

@app.get('/editresource/{resource_id}')
def editresource(request: Request, resource_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
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
                               order=resource.get('order', 0),
                               tags=', '.join(normalize_tags(resource.get('tags', []))),
                               add_hidden='hidden')

    content = remove_templates(content)

    return HTMLResponse(content=content)


@app.post('/addresource')
def addresourcepost(request: Request, resource: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    if resource['id'] == '-1':
        id = '0' if (len(resources.keys()) == 0) else str(max(map(int, resources.keys())) + 1)
        resource['id'] = id
    else:
        id = resource['id']
    if 'order' not in resource:
        if id in resources:
            resource['order'] = resources[id].get('order', 0)
        else:
            resource['order'] = max([r.get('order', 0) for r in resources.values()], default=-1) + 1
    else:
        try:
            resource['order'] = int(resource.get('order', 0))
        except (ValueError, TypeError):
            resource['order'] = 0
    resource['tags'] = normalize_tags(resource.get('tags', []))
    resources[id] = resource

    save_resources()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/listresources')
def listresources(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    with open('templates/listresources.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    resource_template, before, after = get_group(content, 'resource')
    sorted_resources = sorted(resources.items(), key=lambda x: (x[1].get('order', 0), x[0]))
    for id, resource in sorted_resources:
        tags = normalize_tags(resource.get('tags', []))
        resource_content = replace_keywords(resource_template,
                                            id=id,
                                            title=resource['title'],
                                            order=resource.get('order', 0),
                                            tags=', '.join(tags),
                                            tags_attr=', '.join(tags))
        before += resource_content
    content = before + after
    return HTMLResponse(content=content)

@app.post('/deleteresource/{resource_id}')
def deleteresource(request: Request, resource_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if resource_id not in resources:
        return JSONResponse(content={'error': 'Resource not found'}, status_code=404)
    del resources[resource_id]
    save_resources()
    return JSONResponse(content={'success': True}, status_code=200)

@app.get('/resource/{resource_id}')
def get_resource(request: Request, resource_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    if resource_id not in resources:
        return RedirectResponse('/resources')
    resource = resources[resource_id]

    with open('templates/resource.html') as f:
        content = f.read()

    text = render_resource_text(resource['text'])

    content = replace_keywords(content,
                               current_user=user,
                               title=resource['title'],
                               text=text)

    return HTMLResponse(content=content)

@app.post('/previewresource')
def previewresource(request: Request, body: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return JSONResponse({'error': 'Not allowed'}, status_code=403)
    text = body.get('text', '') if isinstance(body, dict) else ''
    return JSONResponse(content={'html': render_resource_text(text)})

def render_resource_text(text):
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

    return text

@app.get('/listsections')
def listsections(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')

    with open('templates/listsections.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)
    section_template, before, after = get_group(content, 'section')
    sorted_sections = sorted(sections.items(), key=lambda x: (x[1].get('order', 0), x[0]))
    for id, section in sorted_sections:
        section_content = replace_keywords(section_template,
                                           id=id,
                                           title=section['title'],
                                           visible='checked' if section['visible'] else '',
                                           active='checked' if section['active'] else '',
                                           points='checked' if section['points'] else '')
        before += section_content
    content = before + after
    return HTMLResponse(content=content)

@app.post('/addsection')
def addsection(request: Request):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    id = str(max(map(int, sections.keys())) + 1) if sections.keys() else '0'
    max_order = max([s.get('order', 0) for s in sections.values()], default=-1)
    sections[id] = {'title': 'New Section', 'visible': False, 'active': False, 'points': False, 'order': max_order + 1}
    save_sections()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/savesections')
def savesections(request: Request, new_sections: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    global sections
    if not isinstance(new_sections, dict):
        new_sections = {}
    for sid, s in new_sections.items():
        if 'order' not in s and sid in sections:
            s['order'] = sections[sid].get('order', 0)
        try:
            s['order'] = int(s.get('order', 0))
        except (ValueError, TypeError):
            s['order'] = 0
    sections = new_sections
    save_sections()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/savesectionsorder')
def savesectionsorder(request: Request, body: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    order = body.get('order', []) if isinstance(body, dict) else []
    for index, sid in enumerate(order):
        if sid in sections:
            sections[sid]['order'] = index
    save_sections()
    return JSONResponse(content={'success': True}, status_code=200)

@app.post('/deletesection/{id}')
def deletesection(request: Request, id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if id not in sections:
        return JSONResponse(content={'error': 'Section not found'})
    for question_id in questions:
        if questions[question_id].get('section') == id:
            break
    else:
        del sections[id]
        save_sections()
        return JSONResponse(content={'success': True}, status_code=200)
    return JSONResponse(content={'error': 'The section has questions'})

@app.get('/section/{section_id}')
def getsection(request: Request, section_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    with open('templates/section.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    if section_id not in sections or sections[section_id]['active'] == False or sections[section_id]['visible'] == False:
        if user != 'admin':
            return RedirectResponse('/')
    content = replace_keywords(content, type='question')

    question_template, before, after = get_group(content, 'question')

    sorted_questions = sorted(questions.items(), key=lambda x: x[1].get('order', 0))
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if question_id not in questions:
        return RedirectResponse(url='/')
    question = questions[question_id]
    section = sections.get(question.get('section'), {})
    if not section.get('active') or not section.get('visible'):
        if user != 'admin':
            return RedirectResponse('/')

    with open('templates/question.html') as f:
        content = f.read()
    
    solution = ''
    if ((question_id in users[user]['solves'] and \
       users[user]['solves'][question_id]['points'] == questions[question_id]['points']) or \
       user == 'admin') and \
       'solution' in questions[question_id] and \
        questions[question_id]['solution'] != '':
       solution = f'<a style="color: #102d4e; text-decoration: none;" href="/viewcode/solution/{question_id}">Solution</a>'
    
    success_link = ''
    if 'solution' in questions[question_id] and questions[question_id]['solution'] != '':
        success_link = '/viewcode/solution/' + question_id
    
    content = replace_keywords(content,
                               current_user=user,
                               qname=question['title'],
                               statement=question['question'],
                               success_link=success_link,
                               question_id=question_id,
                               solution=solution,
                               codegolfscoring=f'<b>Scoring:</b> {question["points"]} * ({question["score"]})' if question['type'] == 'codegolf' else '',
                               presolution=question['presolution'].replace('\n', '\\n').replace('"', '\\"'),
                               tmpsolution=question['tmpsolution'].replace('\n', '\\n').replace('"', '\\"'),
                               postsolution=question['postsolution'].replace('\n', '\\n').replace('"', '\\"'),
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
            if 'show' not in testcase or testcase['show']:
                before += replace_keywords(sample_template, input=testcase['input'], output=testcase['output'])
    content = before + after

    return HTMLResponse(content=content)


@app.post('/question/{question_id}')
def evaluate(request: Request, question_id: str, answer: Answer):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if question_id not in questions:
        return RedirectResponse(url='/')
    question = questions[question_id]
    section = sections.get(question.get('section'), {})
    if not section.get('active') or not section.get('visible'):
        if user != 'admin':
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
                if question['type'] in ['outputonly', 'checker', 'codegolf'] and node.func.id == 'input':
                    return JSONResponse({'error': f'Do not use input'})

    except Exception:
        pass

    def get(filename):
        with open(workdir + '/' + filename) as f:
            data = f.read()
        return data

    points = 0
    msg = ''
    workdir = f'tmp/{user}'
    os.makedirs(workdir, exist_ok=True)
    for _tmp_file in os.listdir(workdir):
        _tmp_path = os.path.join(workdir, _tmp_file)
        if os.path.isfile(_tmp_path):
            os.remove(_tmp_path)
    for envfile in question['envfiles'].split(','):
        if envfile:
            _env_name = os.path.basename(envfile.strip())
            _env_src = os.path.join('files', _env_name)
            if os.path.isfile(_env_src):
                shutil.copy(_env_src, os.path.join(workdir, _env_name))

    if question['type'] == 'solution':
        with open(workdir + '/solution.py', 'w') as f:
            f.write(question['solution'])
        with open(workdir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(workdir + '/generator.py', 'w') as f:
            f.write(question['generator'])

        def checking_stream():
            for i in range(100):
                yield json.dumps({'checking': i+1}) + '\n'
                result = os.system(f'cd {workdir}; python3 generator.py > input.txt 2> generator_error.txt')
                if result:
                    yield json.dumps({'error': 'An error occurred when generating input: ' + get('generator_error.txt')}) + '\n'
                    return

                with open(f'{workdir}/output.txt', 'w') as f:
                    f.write('No output is generated')
                with open(f'{workdir}/error.txt', 'w') as f:
                    f.write('No error is generated')
                result = os.system(f'cd {workdir}; timeout 1s python3 code.py < input.txt > output.txt 2> error.txt')
                if result:
                    if result == 31744:
                        yield json.dumps({'error': 'Took too long to execute', 'input': get('input.txt')}) + '\n'
                        return
                    else:
                        yield json.dumps({'error': get('error.txt'), 'input': get('input.txt')}) + '\n'
                        return

                result = os.system(f'cd {workdir}; python3 solution.py < input.txt > expected.txt 2> solution_error.txt')
                if result:
                    yield json.dumps({'error': 'An error occurred when generating solution: ' + get('solution_error.txt')}) + '\n'
                    return

                if os.system(f'diff -w {workdir}/output.txt {workdir}/expected.txt > /dev/null'):
                    yield json.dumps({'input': get('input.txt'), 'output': get('output.txt'), 'expected': get('expected.txt')})  + '\n'
                    return

            if section['points']:
                users[user]['solves'][question_id]['points'] = questions[question_id]['points']
                users[user]['solves'][question_id]['best_solution'] = {'time': time, 'code': answer.input}
                save_users()
            
            yield json.dumps({'result': 'success'}) + '\n'
        return StreamingResponse(checking_stream(), media_type="application/json", headers={"stream": "true"})

    elif question['type'] == 'checker':
        with open(workdir + '/checker.py', 'w') as f:
            f.write(question['checker'])
        with open(workdir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{workdir}/output.txt', 'w') as f:
            f.write('No output is generated')

        result = os.system(f'cd {workdir}; python3 checker.py > output.txt 2> error.txt')
        if result:
            error = get('error.txt')
            output = get('output.txt')
            if error:
                return JSONResponse({'error': error})
            else:
                return JSONResponse({'error': output})
        elif result == 0:
            if get('output.txt') == '':
                points = 1
            else:
                try:
                    points, msg = get('output.txt').split('|')
                    points = float(points)
                except Exception:
                    return JSONResponse({'error': ''})
    elif question['type'] == 'outputonly':
        with open(workdir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{workdir}/output.txt', 'w') as f:
            f.write('No output is generated')
        error_code = os.system(f'cd {workdir}; python3 code.py > output.txt 2> error.txt')

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
        with open(workdir + '/code.py', 'w') as f:
            f.write(answer.input)
        if answer.input.strip() == question['input'].strip():
            points = 1
        else:
            points = 0
    elif question['type'] == 'testcaseonly':
        with open(workdir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])

        for testcase in question['testcases']:
            with open(f'{workdir}/output.txt', 'w') as f:
                f.write('No output is generated')
            with open(f'{workdir}/error.txt', 'w') as f:
                f.write('No error is generated')
            with open(f'{workdir}/input.txt', 'w') as f:
                f.write(testcase['input'])

            result = os.system(f'cd {workdir}; timeout 1s python3 code.py < input.txt > output.txt 2> error.txt')
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
        with open(workdir + '/code.py', 'w') as f:
            f.write(question['presolution'] + '\n')
            f.write(answer.input + '\n')
            f.write(question['postsolution'])
        with open(f'{workdir}/output.txt', 'w') as f:
            f.write('No output is generated')
        error_code = os.system(f'cd {workdir}; python3 code.py > output.txt 2> error.txt')

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
                      f"Score: {points * questions[question_id]['points']:.2f}/{questions[question_id]['points']}"
    elif question['type'] == 'manual':
        if section['points']:
            users[user]['solves'][question_id]['waiting'] = True
            save_users()
        return JSONResponse({'result': 'submitted', 'error': 'Your solution is submitted and will be evaluated'})

    if section['points']:
        users[user]['solves'][question_id]['points'] = round(points * questions[question_id]['points'], 2)
    else:
        users[user]['solves'][question_id]['points'] = 0.1
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return JSONResponse({'error': 'Not allowed'})
    
    if body['points'] == True:
        body['points'] = questions[body['question_id']]['points']
    elif body['points'] == False:
        body['points'] = 0

    if body['question_id'] not in users[body['username']]['solves']:
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    with open('templates/scoreboard.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    active_questions = []
    sorted_sections = []
    for section_id in sections:
        section = sections[section_id]
        if section['visible']:
            sorted_sections.append((section.get('order', 0), section_id))
    sorted_sections.sort()

    section_sides = []
    for _, section_id in sorted_sections:
        sorted_questions = sorted(questions.items(), key=lambda q: (q[1].get('order', 0), q[0]))
        for question_id, question in sorted_questions:
            if question['section'] == section_id:
                active_questions.append(question_id)
        section_sides.append(len(active_questions))
    
    active_questions.reverse()
    section_sides = [len(active_questions) - x for x in section_sides][:-1]

    question_template, before, after = get_group(content, 'question')
    for i, question_id in enumerate(active_questions):
        before += replace_keywords(question_template,
                                   onclick=f"window.location.href = '/question/{question_id}'",
                                   name=questions[question_id]['title'],
                                   classes='section_side' if i in section_sides else '')

    content = before + after

    user_template, before, after = get_group(content, 'user')
    user_strings = []
    for username in users:
        if users[username]['visible'] == False:
            continue
        solved_template, user_before, user_after = get_group(user_template, 'solved')
        user_before = replace_keywords(user_before, name=users[username]['name'])

        total_point = 0
        for i, question_id in enumerate(active_questions):
            point = 0 if question_id not in users[username]['solves'] else users[username]['solves'][question_id]['points']
            user_point = 0 if question_id not in users[user]['solves'] else users[user]['solves'][question_id]['points']
            expected = questions[question_id]['points']

            classes = ''

            if question_id in users[username]['solves'] and 'waiting' in users[username]['solves'][question_id] and users[username]['solves'][question_id]['waiting'] == True: classes = 'waiting'
            elif point <= 0:        classes = 'unsolved'
            elif point < expected:  classes = 'partially_solved'
            else:                   classes = 'solved'

            total_point += point

            if questions[question_id]['type'] == 'codegolf' and question_id in users[username]['solves'] and users[username]['solves'][question_id]['best_solution'] != None:
                point = f'{point}\n<p style="font-size: 12px; margin: 0px;">({len(users[username]['solves'][question_id]['best_solution']['code'])})</p>'

            if i in section_sides:
                classes += ' section_side'

            state = replace_keywords(solved_template, classes=classes)

            if user_point >= expected or user == 'admin':
                onclick = f"location.href='/viewcode/{username}/{question_id}'"
                cursor = "pointer"
            else:
                onclick = ""
                cursor = "default"
            user_before += replace_keywords(state, onclick=onclick, point=point, cursor=cursor)

        user_before += replace_keywords(solved_template, solved="unsolved", onclick="", point=round(total_point, 2), classes='section_side')
        user_strings.append((total_point, user_before + user_after))

    user_strings.sort(reverse=True)
    for _, user_string in user_strings:
        before += user_string

    content = before + after

    return HTMLResponse(content=content)

@app.get('/viewcode/{username}/{question_id}')
def viewcode(request: Request, username: str, question_id: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    if question_id not in questions:
        return RedirectResponse('/scoreboard')
    if username != 'solution' and username not in users:
        return RedirectResponse('/scoreboard')
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
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
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')

    if not is_safe_filename(filename):
        return RedirectResponse(url='/files')
    with open('templates/editfile.html') as f:
        content = f.read()
    content = replace_keywords(content, current_user=user)

    with open(os.path.join('files', filename)) as f:
        file_content = f.read()
    content = replace_keywords(content, filename=filename, file_content=file_content)
    
    return HTMLResponse(content=content)

@app.post('/editfile/{filename}')
def newfile(request: Request, filename: str, body: Any = Body(None)):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if not is_safe_filename(filename):
        return JSONResponse(content={'error': 'Invalid filename'}, status_code=400)
    with open(os.path.join('files', filename), 'w') as f:
        f.write(body['content'])
    return JSONResponse(content='{}')

@app.post('/deletefile/{filename}')
def deletefile(request: Request, filename: str):
    auth_response = handle_user(request)
    if auth_response:
        return auth_response
    user = request.cookies.get('username')
    if user != 'admin':
        return RedirectResponse(url='/')
    if not is_safe_filename(filename):
        return JSONResponse(content={'error': 'Invalid filename'}, status_code=400)
    _delete_path = os.path.join('files', filename)
    if os.path.isfile(_delete_path):
        os.remove(_delete_path)
    return JSONResponse(content='{}')