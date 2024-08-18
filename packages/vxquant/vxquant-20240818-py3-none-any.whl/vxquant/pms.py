"""组合管理系统"""

import time
import polars as pl
from datetime import datetime
from threading import Lock
from typing import List, Optional
from vxquant.models import VXPosition, VXCashInfo, VXOrder, VXExecRpt


class VXAccount:
    def __init__(
        self,
        account_id: str,
        balance: float,
        positions: Optional[List[VXPosition]] = None,
    ) -> None:
        self._account_id = account_id
        self._balance = balance
        self._lock = Lock()
        if positions is None:

            self._positions = pl.DataFrame(
                {
                    k: [v]
                    for k, v in VXPosition(account_id=account_id, symbol="000001.SH")
                    .model_dump()
                    .items()
                }
            ).filter(pl.col("account_id") != account_id)
        else:
            self._positions = pl.DataFrame(
                [position.model_dump() for position in positions]
            )

    @property
    def account_id(self) -> str:
        return self._account_id

    @property
    def balance(self) -> float:
        with self._lock:
            return self._balance

    @property
    def positions(self) -> pl.DataFrame:
        with self._lock:
            return self._positions

    @property
    def market_value(self) -> float:
        with self._lock:
            if self._positions.is_empty():
                return 0
            return self._positions["market_value"].sum()

    @property
    def nav(self) -> float:
        with self._lock:
            return (
                self._balance
                if self._positions.is_empty()
                else self._balance + self._positions["market_value"].sum()
            )

    def on_execrpt_status(
        self,
        symbol: str,
        filled_volume: int,
        filled_price: float,
        commission: float = 0.0,
    ) -> None:
        """成交状态更新"""
        with self._lock:
            cost = (
                filled_price * filled_volume + commission
                if filled_volume > 0
                else filled_price * filled_volume + commission
            )
            if self._positions.filter(
                pl.col("symbol") == symbol, pl.col("account_id") == self._account_id
            ).is_empty():

                p = VXPosition(
                    account_id=self._account_id,
                    symbol=symbol,
                    volume_today=filled_volume,
                    lasttrade=filled_price,
                    cost=filled_price * filled_volume + commission,
                )
            else:
                self._positions.with_columns(
                    
                )


if __name__ == "__main__":
    account = VXAccount("test", 10000)
    print(account.account_id)
    print(account.positions)
    print(account.nav)
