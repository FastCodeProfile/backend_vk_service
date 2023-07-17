from hashlib import md5
from random import randint

from fastapi import APIRouter

router = APIRouter()


@router.get("/pay")
async def get_sign(amount: float):
    shop = 6631
    payment = randint(0000, 9999)
    desc = 'Пополнение'
    secret = 'aab6ac95ac0d5145fe118021efe25fde'
    sign = md5(f'{amount}|{payment}|{shop}|RUB|{desc}|{secret}'.encode('utf-8')).hexdigest()
    return {"url": f"https://payok.io/pay?amount={amount}&payment={payment}&desc={desc}&shop={shop}&sign={sign}"}
