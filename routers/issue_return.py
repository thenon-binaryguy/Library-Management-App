from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import main ,oauth2


router = APIRouter()

#issuing a book
@router.get("/books/issue",response_class=HTMLResponse)
def issue_book(request:Request ,id:int,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""update books set issued = true ,issued_by = %s where id = %s""" , ((str(user_id)),(str(id))))
    main.conn.commit()
    main.cursor.execute("""update users set issue_left = issue_left - 1  where id = %s""" , ((str(user_id))))
    main.conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/books")

#returning a book
@router.get("/userbooks",response_class=HTMLResponse)
def get_posts(request:Request,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""select * from books where issued_by= %s;""",((str(user_id))))
    data = main.cursor.fetchall()
    return main.templates.TemplateResponse("returnbook.html",{"request": request,"data":data  })


@router.get("/books/return",response_class=HTMLResponse)
def issue_book(id:int,request:Request,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""update books set issued = false ,issued_by=0 where id = %s""" , (str(id)))
    main.conn.commit()
    main.cursor.execute("""update users set issue_left = issue_left + 1  where id = %s""" , ((str(user_id))))
    main.conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/userbooks")