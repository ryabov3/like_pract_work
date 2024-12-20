import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from concurrent.futures import ProcessPoolExecutor
from math import factorial

BOT_TOKEN = ...

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
executor_pool = ProcessPoolExecutor()


def calculate_factorial_sum():
    result = sum(factorial(i) for i in range(1, 5001))
    return result % 10


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Запуск бота. Всё ок")


@router.message(Command("calculate"))
async def calculate_handler(message: types.Message):
    await message.answer(
        "Вычисление факториала..."
    )

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor_pool, calculate_factorial_sum)

    await message.answer(
        f"Последняя цифра суммы факториалов первых 5000 чисел: {result}"
    )


@router.message()
async def echo_other(message: types.Message):
    text = message.text
    await message.answer(f"Получено сообщение: {text}")
    await asyncio.sleep(10)
    await message.answer(f'От сообщения с текстом "{text}" прошло 10 секунд')


async def main():
    print("Бот запущен")
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
