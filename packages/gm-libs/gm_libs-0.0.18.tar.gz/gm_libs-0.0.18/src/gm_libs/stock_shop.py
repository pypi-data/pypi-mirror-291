# coding=utf-8
from __future__ import print_function, absolute_import

import datetime

import pandas as pd
from gm.api import *
from logs import log_all


# 卖指定数量的股票
def get_price(stock: str, price: float = 0, offset_price: float = 0):
    if price == 0:
        price_current = current(stock, 'close')
        if len(price_current) == 0:
            log_all("warn", "%s 未能获取到最新价格" % stock, "debug")
            return 0
        price = price_current[0].price + price_current[0].price * 0.03 + offset_price

    return price


# 买指定数量的股票
def buy_count(stock: str, count: int, price: float = 0, offset_price: float = 0):
    return l_buy_count(stock, count, price, offset_price)


# 买指定数量的股票
def l_buy_count(stock: str, count: int, price: float = 0, offset_price: float = 0):
    price = get_price(stock, price, offset_price)
    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Buy,
                        position_effect=PositionEffect_Open)


# 卖指定数量的股票
def sell_count(stock: str, count: int, price: float = 0, offset_price: float = 0):
    return l_sell_count(stock, count, price, offset_price)


# 卖指定数量的股票
def l_sell_count(stock: str, count: int, price: float = 0, offset_price: float = 0):
    price = get_price(stock, price, offset_price)

    return order_volume(symbol=stock, volume=count, price=price, order_type=OrderType_Market, side=OrderSide_Sell,
                        position_effect=PositionEffect_Close)


# 调整仓位（到特定数量）
def order_target_count(stock: str, volume: int, price: float = 0, offset_price: float = 0):
    return l_order_target_count(stock, volume, price, offset_price)


# 调整仓位（到特定数量）
def l_order_target_count(stock: str, volume: int, price: float = 0, offset_price: float = 0):
    price = get_price(stock, price, offset_price)

    order_cancel_all()
    return order_target_volume(symbol=stock, volume=volume, price=price, order_type=OrderType_Market,
                               position_side=PositionSide_Long)


# 调整仓位（到特定价值）
def order_target_money(stock: str, worth: int, price: float = 0, offset_price: float = 0):
    return l_order_target_money(stock, worth, price, offset_price)


# 调整仓位（到特定价值）
def l_order_target_money(stock: str, worth: int, price: float = 0, offset_price: float = 0):
    price = get_price(stock, price, offset_price)

    order_cancel_all()
    return order_target_value(symbol=stock, value=worth, price=price, order_type=OrderType_Market,
                              position_side=PositionSide_Long)


# 获取交易量统计
# 掘金的 cur_volume，完全是按照本地数据取的，就没考虑本地数据缺失
def l_get_one_day_volume(symbol: str, end_time: datetime):
    volumes = history(symbol=symbol, frequency="60s", start_time=end_time.replace(hour=9, minute=20),
                      end_time=end_time,
                      fields="volume", skip_suspended=True, fill_missing=None, adjust=ADJUST_NONE,
                      adjust_end_time='', df=True)
    if len(volumes) == 0:
        return 0
    return volumes["volume"].sum()


# 获取今日价格信息
def l_get_one_day_price(symbol: str, end_time: datetime):
    data = history(symbol=symbol, frequency="60s", start_time=end_time.replace(hour=9, minute=20),
                   end_time=end_time,
                   fields="open, close, low, high", skip_suspended=True, fill_missing=None, adjust=ADJUST_NONE,
                   adjust_end_time='', df=True)
    return {
        "open": data["open"].iloc[0],
        "close": data["close"].iloc[-1],
        "low": data["low"].min(),
        "high": data["high"].max(),
    }


# 获取当前是否实盘
def is_live(c):
    # type: (Context) -> bool
    return c.mode == MODE_LIVE


# 获取历史数据
def l_history_n(c, symbol, count, end_time, frequency='1d', fields='close', df=False):
    # type: (Context, str, int, datetime, str, str, bool) -> pd.DataFrame | list
    if is_live(c) is False:
        end_time = end_time - datetime.timedelta(days=1)

    return history_n(symbol=symbol, count=count, frequency=frequency, fields=fields, end_time=end_time, df=df)
