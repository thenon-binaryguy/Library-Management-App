from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import main ,oauth2

router = APIRouter()

#retrieving available books
@router.get("/books",response_class=HTMLResponse)
def get_books(request:Request):
    main.cursor.execute("select * from books where issued=false;")
    #print(request.headers)
    data = main.cursor.fetchall()
    return main.templates.TemplateResponse("home.html",{"request": request,"data":data  })

#retrieving available books
@router.post("/books",response_class=HTMLResponse)
def get_books(response: Response,request:Request,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    userdata  = main.cursor.fetchone()
    main.cursor.execute("select * from books where issued=false;")
    data = main.cursor.fetchall()
    return main.templates.TemplateResponse("home.html",{"request": request,"data":data ,"userdata":userdata })