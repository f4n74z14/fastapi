from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import DatabaseLang
from models.schema import Lang
from repository import main_repo
from responses import responses

router = APIRouter(prefix="/api/langs")


@router.get("/", response_model=list[Lang])
async def get_langs(session: AsyncSession = Depends(main_repo.get_session)):
    return await main_repo.fetch_all_langs(session)


@router.get("/{lang_id}", response_model=Lang)
async def get_lang(lang_id: int, session: AsyncSession = Depends(main_repo.get_session)):
    lang = main_repo.fetch_lang(session, lang_id)

    if lang is None:
        raise HTTPException(status_code=404, detail=f"Язык c id={lang_id} не найден.")

    return lang


@router.post("/", response_model=Lang)
async def create_lang(lang: Lang, session: AsyncSession = Depends(main_repo.get_session)):
    database_lang = DatabaseLang(
        name=lang.name,
        cyrillic=lang.cyrillic
    )

    await main_repo.create_lang(session, database_lang)

    return database_lang


@router.put("/{lang_id}", response_model=Lang)
async def update_lang(lang_id: int, updated_lang: Lang, session: AsyncSession = Depends(main_repo.get_session)):
    database_lang = await main_repo.fetch_lang(session, lang_id)

    if database_lang is None:
        raise HTTPException(status_code=404, detail=f"Язык c id={lang_id} не найден.")

    await main_repo.update_user(session, database_lang, DatabaseLang(
        namr=updated_lang.name,
        cyrillic=updated_lang.cyrillic,
    ))

    return database_lang


@router.delete("/{lang_id}")
async def delete_lang(lang_id: int, session: AsyncSession = Depends(main_repo.get_session)):
    removed_lang = await main_repo.remove_lang(session, lang_id)

    if removed_lang is None:
        raise HTTPException(status_code=404, detail=f"Язык c id={lang_id} не найден.")

    return responses.LANG_DELETED_SUCCESSFULLY
