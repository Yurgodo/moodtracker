from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_marked_section, Bold
from datetime import datetime, timedelta
import database as db

router = Router()

class EventState(StatesGroup):
    description = State()
    emotion = State()
    rating = State()

@router.message(F.text == '📌 Добавить событие дня')
async def cmd_add_event(message: Message, state: FSMContext):
    await state.update_data(edit=False)
    await state.set_state(EventState.description)
    await message.answer('Опишите главное событие дня:')

@router.message(F.text == '✏️ Изменить событие дня')
async def cmd_edit_event(message: Message, state: FSMContext):
    await state.update_data(edit=True)
    await state.set_state(EventState.description)
    await message.answer('Введите новое описание события:')

@router.message(EventState.description)
async def event_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(EventState.emotion)
    await message.answer('Какую эмоцию вы испытали?')

@router.message(EventState.emotion)
async def event_emotion(message: Message, state: FSMContext):
    await state.update_data(emotion=message.text)
    await state.set_state(EventState.rating)
    await message.answer('Оцените эмоцию от 1 до 10:')

@router.message(EventState.rating)
async def event_rating(message: Message, state: FSMContext):
    data = await state.update_data(rating=int(message.text))
    today = datetime.now().date().isoformat()
    if data.get('edit'):
        await db.update_event(
            user_id=message.from_user.id,
            event_date=today,
            description=data['description'],
            emotion=data['emotion'],
            rating=data['rating']
        )
        text = 'Событие обновлено!'
    else:
        await db.add_event(
            user_id=message.from_user.id,
            event_date=today,
            description=data['description'],
            emotion=data['emotion'],
            rating=data['rating']
        )
        text = 'Событие сохранено!'
    await state.clear()
    await message.answer(text)

@router.message(F.text == '📆 Посмотреть события недели')
async def view_week(message: Message):
    end = datetime.now().date()
    start = end - timedelta(days=6)
    rows = await db.get_events_between(message.from_user.id, start.isoformat(), end.isoformat())
    if not rows:
        await message.answer('Событий нет')
        return
    text = as_marked_section(*[
        Bold(r[0]) + f" {r[1]} - {r[2]} ({r[3]}/10)" for r in rows
    ], marker='\n')
    await message.answer(text.as_html())

@router.message(F.text == '🌟 Посмотреть лучшие события недели')
async def best_week(message: Message):
    end = datetime.now().date()
    start = end - timedelta(days=6)
    row = await db.get_best_event(message.from_user.id, start.isoformat(), end.isoformat())
    if not row:
        await message.answer('Событий нет')
        return
    await message.answer(f"{row[0]} {row[1]} - {row[2]} ({row[3]}/10)")

@router.message(F.text == '🏆 Посмотреть лучшие события месяца')
async def best_month(message: Message):
    end = datetime.now().date()
    start = end - timedelta(days=30)
    row = await db.get_best_event(message.from_user.id, start.isoformat(), end.isoformat())
    if not row:
        await message.answer('Событий нет')
        return
    await message.answer(f"{row[0]} {row[1]} - {row[2]} ({row[3]}/10)")

