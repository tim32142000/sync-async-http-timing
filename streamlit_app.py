import asyncio

import streamlit as st

from async_check import run_checks as run_async_checks
from sync_check import run_checks as run_sync_checks


def display_name(url: str) -> str:
    return (
        url.removeprefix("https://")
        .removeprefix("http://")
        .removeprefix("www")
        .rstrip("/")
    )


st.title("Async Service Monitor")

if st.button("Run Check"):
    results, elapsed = asyncio.run(run_async_checks())

    st.metric("Total execution time", f"{elapsed:.3f} s")

    col1, col2 = st.columns([5, 1])

    col1.markdown("**URL**")
    col2.markdown("**LATENCY**")

    for url, status, latency in results:
        col1, col2 = st.columns([5, 1])

        col1.write(url)

        if status == "TIMEOUT":
            col2.write("Timeout")
        else:
            col2.write(f"{latency * 1000:.0f} ms")
