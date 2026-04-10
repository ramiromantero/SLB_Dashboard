import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import plotly.graph_objects as go
from app import get_price, build_sparkline, build_chart


# ── get_price ──────────────────────────────────────────────────────────────────

def test_get_price_returns_float_values():
    """Precio y cambio deben ser floats para tickers válidos."""
    price, change = get_price("SLB")
    assert price is not None
    assert change is not None
    assert isinstance(price, float)
    assert isinstance(change, float)

def test_get_price_returns_positive_price():
    """El precio nunca puede ser negativo."""
    price, _ = get_price("CL=F")
    if price is not None:
        assert price > 0

def test_get_price_invalid_ticker_returns_none():
    """Un ticker inexistente no debe crashear — retorna None, None."""
    price, change = get_price("TICKER_INVALIDO_XYZ_123")
    assert price is None
    assert change is None

def test_get_price_returns_tuple():
    """La función siempre retorna exactamente dos valores."""
    result = get_price("XOM")
    assert len(result) == 2


# ── build_sparkline ────────────────────────────────────────────────────────────

def test_build_sparkline_returns_figure():
    """Debe retornar un objeto Figure de Plotly."""
    fig = build_sparkline("SLB", 1.5)
    assert isinstance(fig, go.Figure)

def test_build_sparkline_invalid_ticker_returns_empty_figure():
    """Un ticker inválido no debe crashear — retorna figura vacía."""
    fig = build_sparkline("INVALIDO_XYZ", 0)
    assert isinstance(fig, go.Figure)

def test_build_sparkline_positive_change():
    """Con cambio positivo la función no debe crashear."""
    fig = build_sparkline("XOM", 2.3)
    assert fig is not None

def test_build_sparkline_negative_change():
    """Con cambio negativo la función no debe crashear."""
    fig = build_sparkline("XOM", -1.8)
    assert fig is not None

def test_build_sparkline_zero_change():
    """Con cambio cero la función no debe crashear."""
    fig = build_sparkline("SLB", 0)
    assert fig is not None


# ── build_chart ────────────────────────────────────────────────────────────────

def test_build_chart_returns_figure():
    """Debe retornar un objeto Figure de Plotly."""
    fig = build_chart("SLB", "1mo")
    assert isinstance(fig, go.Figure)

def test_build_chart_invalid_ticker_returns_empty_figure():
    """Un ticker inválido no debe crashear — retorna figura vacía."""
    fig = build_chart("INVALIDO_XYZ", "1mo")
    assert isinstance(fig, go.Figure)

def test_build_chart_all_periods():
    """Todos los períodos válidos deben funcionar sin errores."""
    periods = ["5d", "1mo", "3mo", "6mo", "1y", "2y"]
    for period in periods:
        fig = build_chart("SLB", period)
        assert isinstance(fig, go.Figure), f"Falló con período: {period}"