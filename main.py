from typing import Optional
from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form 
from fastapi.responses import RedirectResponse
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import schemas ,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from routers import getbooks,modifybook ,issue_return ,usermodify ,profile,search

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="views")

try:
    conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres"
    ,password="pass",cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connection Successful")

except Exception as err:
    print("Connection failed coz " + err)



app.include_router(getbooks.router)
app.include_router(modifybook.router)
app.include_router(issue_return.router)
app.include_router(usermodify.router)
app.include_router(profile.router)
app.include_router(search.router)



@app.get("/login",response_class=HTMLResponse)
def login(request:Request):
    error =[]
    return templates.TemplateResponse("index.html",{"request": request,"error":error})



@app.post("/login",response_class=HTMLResponse)
async def login(request:Request,username:str = Form(...),password:str= Form(...)):
    error=[]
    print(username)
    cursor.execute("select * from users where email = '{0}' ; ".format(username))
    user = cursor.fetchone()
    if not user:
        error.append("Invalid Credentials")
        return templates.TemplateResponse("index.html",{"request": request ,"error":error})
    
    if (password != user["password"]):
        error.append("Invalid Credentials")
        return templates.TemplateResponse("index.html",{"request": request ,"error":error})
    
    access_token = oauth2.create_token(data={"user_id": user["id"]})

    #return {"access_token": access_token, "token_type": "bearer"}
    #auth = """Bearer %s""".format(access_token) 
    response = RedirectResponse("http://127.0.0.1:8000/books" )
    response.set_cookie(key="Authorization", value= f"{access_token}", httponly=True)
    return response


@app.middleware("http")
async def create_auth_header(
    request: Request,
    call_next,):
    '''
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    '''
    if ("Authorization" not in request.headers 
        and "Authorization" in request.cookies
        ):
        access_token = request.cookies["Authorization"]
        
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer {access_token}".encode(),
            )
        )
    elif ("Authorization" not in request.headers 
        and "Authorization" not in request.cookies
        ): 
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer 12345".encode(),
            )
        )
        
    
    response = await call_next(request)
    return response  