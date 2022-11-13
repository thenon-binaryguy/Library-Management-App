from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import main ,oauth2

router = APIRouter()

@router.get("/myprofile",response_class=HTMLResponse)
def myprof(request:Request , user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    main.cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    data  = main.cursor.fetchone()
    print(data)

    return main.templates.TemplateResponse("myprofile.html",{"request": request ,"data":data,"id":id})

@router.post("/myprofile",response_class=HTMLResponse)
def myprof(request:Request ,user_id: int = Depends(oauth2.get_current_user)):
    print(id)
    main.cursor.execute("""select * from users where id = %s ; """, (str(user_id)))
    data  = main.cursor.fetchone()
    print(data)

    return main.templates.TemplateResponse("myprofile.html",{"request": request ,"data":data,"id":id})