from fastapi import FastAPI, Response,Depends, status ,HTTPException,Request ,File,UploadFile,Form ,APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
import main ,oauth2

router = APIRouter()

#creating a user
@router.post("/users",status_code=status.HTTP_201_CREATED)
def create_user(email:str=Form(...),username : str=Form(...),password : str=Form(...) , age : int=Form(...)):
    
    main.cursor.execute("""INSERT INTO users (name,email,password,age) values (%s,%s,%s,%s) returning *"""
    ,(username, email, password, age))
    new_user = main.cursor.fetchone()    
    print(new_user)
    main.conn.commit()
    return RedirectResponse("http://127.0.0.1:8000/login")


#deleting a user
@router.delete("/users/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deleteu(id:int,user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("DELETE from users where id = %s returning *",(str(id)))
    del_post = main.cursor.fetchone() 
    if del_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Id not found")
    main.conn.commit()
    return({"Post successfully deleted " : del_post})

#updating a user
@router.post("/usersupdate")
def update_book(email:str=Form(...),username : str=Form(...),password : str=Form(...) , age : int=Form(...),user_id: int = Depends(oauth2.get_current_user)):
    main.cursor.execute("""UPDATE users SET email = %s , name = %s, password =%s, age=%s  WHERE id = %s RETURNING *""",
                    (email , username,password , age, str(user_id)))

    updated_post = main.cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    main.conn.commit()
    url = ("""myprofile""")
    return RedirectResponse(url)

    #return updated_post