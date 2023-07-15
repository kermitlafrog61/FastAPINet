from collections import defaultdict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from core.db import SessionLocal

from ..users.jwt import decode_token
from .models import Post
from .schemas import PostCreate, PostDetail, PostUpdate

router = APIRouter()
# Cache for likes and dislikes
post_likes_cache = defaultdict(set)
post_dislikes_cache = defaultdict(set)


@router.post("/posts")
async def create_post(post_in: PostCreate, token: str = Depends(decode_token)):
    """
    Create a new post, gets token as the url param
    """
    if token:  # Token is already decoded
        post = Post(**post_in.model_dump(), user_id=token["user_id"])
        with SessionLocal() as session:
            session.add(post)
            session.commit()
            data = PostDetail.model_validate(post).model_dump()
        return JSONResponse(data, status_code=201)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.put("/posts/{post_id}")
async def edit_post(post_id: int, post_in: PostUpdate, token: str = Depends(decode_token)):
    """
    Edit a post, same with token
    """
    if token:
        with SessionLocal() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post.user_id == token["user_id"]:
                for field, value in post_in.model_dump(exclude_none=True).items():
                    setattr(post, field, value)
                    session.commit()
            data = PostDetail.model_validate(post).model_dump()
        return JSONResponse(data, status_code=200)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, token: str = Depends(decode_token)):
    """
    Delete a post, additionally deletes likes and dislikes from memory
    """
    if token:
        with SessionLocal() as session:
            post = session.query(Post).filter(Post.id == post_id).first()
            if post.user_id == token["user_id"]:
                session.delete(post)
                session.commit()
        post_likes_cache.pop(post_id, None)
        post_dislikes_cache.pop(post_id, None)
        return JSONResponse({"message": "Post deleted"}, status_code=204)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.get("/posts/{post_id}")
async def view_post(post_id: int):
    """
    View a post, use this to view likes and dislikes
    """
    with SessionLocal() as session:
        post = session.query(Post).filter(Post.id == post_id).first()
        if post:
            data = PostDetail.model_validate(post).model_dump()
            likes_count = len(post_likes_cache[post_id])
            dislikes_count = len(post_dislikes_cache[post_id])
            data['likes_count'] = likes_count
            data['dislikes_count'] = dislikes_count
            return JSONResponse(data, status_code=200)
    return JSONResponse({"message": "Post not found"}, status_code=404)


@router.post("/posts/{post_id}/like")
async def like_post(post_id: int, token: str = Depends(decode_token)):
    """
    Like
    """
    if token:
        post_likes_cache[post_id].add(token["user_id"])
        return JSONResponse({"message": "Post liked"}, status_code=200)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.delete("/posts/{post_id}/like")
async def unlike_post(post_id: int, token: str = Depends(decode_token)):
    """
    Unlike
    """

    if token:
        post_likes_cache[post_id].discard(token["user_id"])
        return JSONResponse({"message": "Post unliked"}, status_code=200)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.post("/posts/{post_id}/dislike")
async def dislike_post(post_id: int, token: str = Depends(decode_token)):
    """
    Dislike
    """

    if token:
        post_dislikes_cache[post_id].add(token["user_id"])
        return JSONResponse({"message": "Post disliked"}, status_code=200)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)


@router.delete("/posts/{post_id}/dislike")
async def undislike_post(post_id: int, token: str = Depends(decode_token)):
    """  
    Undislike
    """
    if token:
        post_dislikes_cache[post_id].discard(token["user_id"])
        return JSONResponse({"message": "Post undisliked"}, status_code=200)
    return JSONResponse({"message": "Unauthorized access"}, status_code=401)
