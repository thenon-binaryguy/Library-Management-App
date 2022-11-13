from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import main ,oauth2

router= APIRouter()

@router.get("/search",response_class=HTMLResponse)
def get_searchres(q:str,request:Request):
    qq = str(q)
    print(qq)
    main.cursor.execute("""select *,
	            ts_rank(search, websearch_to_tsquery('simple',%s)) 
                as rank from books
                where (search @@ websearch_to_tsquery('simple',%s))
                order by rank desc ; """ , (q,q))
    
    data = main.cursor.fetchall()
    print(data)
    return main.templates.TemplateResponse("home.html",{"request": request,"data":data  })