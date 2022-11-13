from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import main , oauth2, schemas

router=APIRouter()

@router.get("/addbook",response_class=HTMLResponse)
def goto_book(request:Request,user_id: int = Depends(oauth2.get_current_user) ):
    return main.templates.TemplateResponse("newbook.html",{"request":request})

#adding a book to database
@router.post("/addbook",status_code=status.HTTP_201_CREATED)
def create_book(username:str=Form(...),author:str=Form(...),genre:str=Form(...),publication:str=Form(...),user_id: int = Depends(oauth2.get_current_user) ):
    main.cursor.execute("""INSERT INTO books (name,author,genre,publication) values (%s,%s,%s,%s) returning *"""
    ,(username, author, genre, publication))
    new_book = main.cursor.fetchone()
    main.conn.commit()
    print(new_book)
    return RedirectResponse("http://127.0.0.1:8000/books")


#deleting a book
@router.delete("/books/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleteb(id:int,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("DELETE from books where id = %s returning *",(str(id)))
    del_post = main.cursor.fetchone() 
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")
    main.conn.commit()
    return({"Post successfully deleted " : del_post})


#updating a book
@router.put("/books/{id}")
def update_book(id:int , book :schemas.Book,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""UPDATE posts SET name = %s, author = %s  WHERE id = %s RETURNING *""",
                    (book.name, book.author, str(id)))

    updated_post = main.cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    main.conn.commit()

    return updated_post