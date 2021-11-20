from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, database,  schemas, oath2


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# @router.get("/", response_model=schemas.PostOut)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(database.get_db),
              current_user: int = Depends(oath2.get_current_user),
              limit: int = 5,
              skip: int = 0,
              search: Optional[str] = ""):
    # cursor.execute("""select * from post""")
    # posts = cursor.fetchall()

    # get all post for spesific user
    # post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # return post

    # get all post for all user
    # post = db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # get all post for all user with joint table alchemy
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result)
    return result


@router.get("/{id}", response_model=schemas.PostOut)
def get_postbyId(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""select * from post where id = %s """, (str(id),)
    #               )  # coma behind str(id) is prevention of some random error
    # post = cursor.fetchone()

    # get all post for spesific user
    # post = db.query(models.Post).filter(models.Post.id == id).all()
    # if post.owner_id != current_user.id:
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                        detail=f"Not authorize to perform request action ")
    # return post

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    # get all post for all user with joint table alchemy
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""insert into post(title, content, published) values (%s, %s, %s) RETURNING *""",
    #               (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute(
    #    """delete from post where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform request action ")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, update_post: schemas.PostCreate, db: Session = Depends(database.get_db), current_user: int = Depends(oath2.get_current_user)):
    # cursor.execute("""update post set title = %s, content = %s, published = %s where id=%s returning *""",
    #               (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorize to perform request action ")

    post_query.update(update_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
