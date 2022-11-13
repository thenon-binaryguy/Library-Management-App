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
import os 
import shutil

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

#retrieving available books
@app.get("/books",response_class=HTMLResponse)
def get_books(request:Request):
    cursor.execute("select * from books where issued=false;")
    data = cursor.fetchall()

    return templates.TemplateResponse("home.html",{"request": request,"data":data  })

#retrieving available books
@app.post("/books",response_class=HTMLResponse)
def get_books(response: Response,request:Request,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    userdata  = cursor.fetchone()
    cursor.execute("select * from books where issued=false;")
    data = cursor.fetchall()
    return templates.TemplateResponse("home.html",{"request": request,"data":data ,"userdata":userdata })



@app.get("/addbook",response_class=HTMLResponse)
def goto_book(request:Request,user_id: int = Depends(oauth2.get_current_user) ):
    return templates.TemplateResponse("newbook.html",{"request":request})

#adding a book to database
@app.post("/addbook",status_code=status.HTTP_201_CREATED)
def create_book(username:str=Form(...),author:str=Form(...),genre:str=Form(...),publication:str=Form(...),user_id: int = Depends(oauth2.get_current_user) ):
    cursor.execute("""INSERT INTO books (name,author,genre,publication) values (%s,%s,%s,%s) returning *"""
    ,(username, author, genre, publication))
    new_book = cursor.fetchone()
    conn.commit()
    print(new_book)
    return RedirectResponse("http://127.0.0.1:8000/books")

#creating a user
@app.post("/users",status_code=status.HTTP_201_CREATED)
def create_user(email:str=Form(...),username : str=Form(...),password : str=Form(...) , age : int=Form(...)):
    
    cursor.execute("""INSERT INTO users (name,email,password,age) values (%s,%s,%s,%s) returning *"""
    ,(username, email, password, age))
    new_user = cursor.fetchone()    
    print(new_user)
    conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/login")

#issuing a book
@app.get("/books/issue",response_class=HTMLResponse)
def issue_book(request:Request ,id:int,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""update books set issued = true ,issued_by = %s where id = %s""" , ((str(user_id)),(str(id))))
    conn.commit()
    cursor.execute("""update users set issue_left = issue_left - 1  where id = %s""" , ((str(user_id))))
    conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/books")

#returning a book
@app.get("/userbooks",response_class=HTMLResponse)
def get_posts(request:Request,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""select * from books where issued_by= %s;""",((str(user_id))))
    data = cursor.fetchall()
    return templates.TemplateResponse("returnbook.html",{"request": request,"data":data  })


@app.get("/books/return",response_class=HTMLResponse)
def issue_book(id:int,request:Request,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""update books set issued = false ,issued_by=0 where id = %s""" , (str(id)))
    conn.commit()
    cursor.execute("""update users set issue_left = issue_left + 1  where id = %s""" , ((str(user_id))))
    conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/userbooks")

#deleting a book
@app.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleteb(id:int,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("DELETE from books where id = %s returning *",(str(id)))
    del_post = cursor.fetchone() 
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")
    conn.commit()
    return({"Post successfully deleted " : del_post})


#deleting a user
@app.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleteu(id:int,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("DELETE from users where id = %s returning *",(str(id)))
    del_post = cursor.fetchone() 
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")
    conn.commit()
    return({"Post successfully deleted " : del_post})

#updating a book
@app.put("/books/{id}")
def update_book(id:int , book :schemas.Book,user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""UPDATE posts SET name = %s, author = %s  WHERE id = %s RETURNING *""",
                    (book.name, book.author, str(id)))

    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    conn.commit()

    return updated_post

#updating a user
@app.post("/usersupdate")
def update_book(email:str=Form(...),username : str=Form(...),password : str=Form(...) , age : int=Form(...),user_id: int = Depends(oauth2.get_current_user)):
    cursor.execute("""UPDATE users SET email = %s , name = %s, password =%s, age=%s  WHERE id = %s RETURNING *""",
                    (email , username,password , age, str(user_id)))

    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    conn.commit()
    url = ("""myprofile""")
    return RedirectResponse(url)

    #return updated_post

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

@app.get("/myprofile",response_class=HTMLResponse)
def myprof(request:Request , user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    data  = cursor.fetchone()
    print(data)

    return templates.TemplateResponse("myprofile.html",{"request": request ,"data":data,"id":id})

@app.post("/myprofile",response_class=HTMLResponse)
def myprof(request:Request ,user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    data  = cursor.fetchone()
    print(data)

    return templates.TemplateResponse("myprofile.html",{"request": request ,"data":data,"id":id})


@app.get("/search",response_class=HTMLResponse)
def get_searchres(request:Request,q:str ,page_num: int = 1):
    qq = str(q)
    print(qq)
    cursor.execute("""select *,
	            ts_rank(search, websearch_to_tsquery('simple',%s)) 
                as rank from ytdata
                where (search @@ websearch_to_tsquery('simple',%s))
                order by rank desc ; """ , (q,q))
    data = cursor.fetchall()
    return templates.TemplateResponse("home.html",{"request": request,"data":data  })


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