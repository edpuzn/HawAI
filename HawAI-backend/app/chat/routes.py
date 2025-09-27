from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
import httpx
from bson import ObjectId
from app.auth.routes import require_user_id
from app.db.mongo import get_db
from app.config import settings


router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/threads")
async def list_threads(user_id: str = Depends(require_user_id), db=Depends(get_db)):
    cur = db["threads"].find({"user_id": user_id}).sort("updated_at", -1)
    out = []
    async for t in cur:
        out.append({"id": str(t["_id"]), "title": t.get("title"), "updated_at": t.get("updated_at")})
    return out


@router.post("/threads")
async def create_thread(body: Dict[str, Any], user_id: str = Depends(require_user_id), db=Depends(get_db)):
    title = body.get("title") or "Yeni Sohbet"
    doc = {"user_id": user_id, "title": title, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    res = await db["threads"].insert_one(doc)
    return {"id": str(res.inserted_id), "title": title}


@router.delete("/threads/{thread_id}")
async def delete_thread(thread_id: str, user_id: str = Depends(require_user_id), db=Depends(get_db)):
    # Kullanıcının kendi thread'ini sildiğinden emin ol
    try:
        oid = ObjectId(thread_id)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid thread_id")

    thr = await db["threads"].find_one({"_id": oid, "user_id": user_id})
    if not thr:
        raise HTTPException(status_code=404, detail="thread not found")

    await db["threads"].delete_one({"_id": oid})
    await db["messages"].delete_many({"thread_id": thread_id})
    return {"ok": True}


@router.get("/messages/{thread_id}")
async def list_messages(thread_id: str, user_id: str = Depends(require_user_id), db=Depends(get_db)):
    cur = db["messages"].find({"thread_id": thread_id}).sort("created_at", 1)
    out = []
    async for m in cur:
        out.append({
            "id": str(m["_id"]),
            "role": m.get("role"),
            "content": m.get("content"),
            "images": m.get("images", []),
            "edited": m.get("edited", False)
        })
    return out


@router.post("/send")
async def send_message(body: Dict[str, Any], user_id: str = Depends(require_user_id), db=Depends(get_db)):
    thread_id = body.get("thread_id")
    content = body.get("content") or ""
    images: List[str] = body.get("images") or []
    if not thread_id:
        raise HTTPException(status_code=400, detail="thread_id required")

    # save user message
    msg_doc = {
        "thread_id": thread_id,
        "user_id": user_id,
        "role": "user",
        "content": content,
        "images": images,
        "edited": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db["messages"].insert_one(msg_doc)

    # correct ObjectId usage
    try:
        oid = ObjectId(thread_id)
        await db["threads"].update_one({"_id": oid}, {"$set": {"updated_at": datetime.utcnow()}})
    except Exception:
        pass

    # Always use Ollama native generate API (works for both text and image)
    native_base = settings.OAI_BASE_URL.rstrip("/")
    if native_base.endswith("/v1"):
        native_base = native_base[:-3]

    out_images: List[str] = []
    for im in images:
        # Prefer base64 when provided as data URL; otherwise pass-through (URL/path)
        if isinstance(im, str) and im.startswith("data:image"):
            out_images.append(im.split(",", 1)[1])
        elif isinstance(im, str) and im:
            out_images.append(im)

    # Kimlik ve üslup için sistem mesajı
    system_text = (
        "Adın HawAI. Türkçe konuş. Kısa, net ve nazik cevap ver. "
        "Kendinden bahsederken: 'Ben HawAI’yim, bir yapay zeka sağlık asistanıyım.' de. "
        "Ülke/şehir/yaş/kişi kimliği uydurma; insan kimliği olmadığını belirt. "
        "Gerekirse sınırlılıklarını açıkla. Görsel varsa önce gözlemi kısaca özetle, emin olmadıklarını belirt."
    )

    gen_payload: Dict[str, Any] = {
        "model": settings.OAI_MODEL,
        "prompt": content or "",
        "system": system_text,
        "stream": False,
        "options": {"num_ctx": 1024}
    }
    if out_images:
        gen_payload["images"] = out_images

    async with httpx.AsyncClient(base_url=native_base, timeout=180) as ac:
        r = await ac.post("/api/generate", json=gen_payload)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail=f"llava error: {r.text}")
        data = r.json()
        assistant_text = data.get("response") or ""

    # save assistant message
    a_doc = {
        "thread_id": thread_id,
        "user_id": user_id,
        "role": "assistant",
        "content": assistant_text,
        "images": [],
        "edited": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db["messages"].insert_one(a_doc)

    return {"reply": assistant_text}


@router.post("/edit/{message_id}")
async def edit_message(message_id: str, body: Dict[str, Any], user_id: str = Depends(require_user_id), db=Depends(get_db)):
    new_content = body.get("content")
    try:
        mid = ObjectId(message_id)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid message_id")
    await db["messages"].update_one({"_id": mid, "user_id": user_id}, {"$set": {"content": new_content, "edited": True, "updated_at": datetime.utcnow()}})
    return {"ok": True}


