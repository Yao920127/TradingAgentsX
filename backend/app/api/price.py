"""
Live price routes: today's intraday quote for the results page "Live" mode.
"""
import logging
from typing import Literal, Optional

from fastapi import APIRouter, HTTPException, Query  # type: ignore
from starlette.concurrency import run_in_threadpool  # type: ignore

from backend.app.models.schemas import LiveQuoteResponse
from backend.app.services.live_price_service import (
    InvalidTickerError,
    LiveDataUnavailableError,
    get_live_quote,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/price", tags=["Price"])


@router.get("/live", response_model=LiveQuoteResponse)
async def live_price(
    ticker: str = Query(..., min_length=1, max_length=15),
    market_type: Optional[Literal["us", "twse", "tpex"]] = Query(None),
) -> LiveQuoteResponse:
    """Latest price plus today's 1-minute prices and volumes (Yahoo, may be delayed)."""
    try:
        quote = await run_in_threadpool(get_live_quote, ticker, market_type)
    except InvalidTickerError as e:
        raise HTTPException(status_code=400, detail="Invalid ticker or market type") from e
    except LiveDataUnavailableError as e:
        raise HTTPException(status_code=404, detail="No live data for this ticker") from e
    except Exception as e:
        logger.error("Live price fetch failed for %s: %s", ticker, e)
        raise HTTPException(status_code=502, detail="Live price provider unavailable") from e
    return LiveQuoteResponse(**quote)
