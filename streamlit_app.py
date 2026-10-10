import asyncio

import streamlit as st

from async_check import run_checks as run_async_checks
from sync_check import run_checks as run_sync_checks


def display_name(url: str) -> str:
    return (
        url.removeprefix("https://")
        .removeprefix("http://")
        .removeprefix("www.")
        .rstrip("/")
    )


st.title("Sync Async HTTP Timing")

st.caption("Compare sequential and asynchronous HTTP request performance.")

if st.button("Run Comparison"):
    with st.spinner("Running checks..."):
        sync_results, sync_elapsed = run_sync_checks()

        async_results, async_elapsed = asyncio.run(run_async_checks())

        st.subheader("Running Times of Sync and Async Methods")

        # Header
        col1, col2, col3 = st.columns([4, 1, 1])

        col1.markdown("**Website**")
        col2.markdown("**Sync**")
        col3.markdown("**Async**")

        # Results
        for sync_result, async_result in zip(sync_results, async_results):
            sync_url, sync_status, sync_latency = sync_result
            async_url, async_status, async_latency = async_result

            if sync_status == "TIMEOUT":
                sync_text = "Timeout"
            elif sync_status == "ERROR":
                sync_text = "Error"
            else:
                sync_text = f"{sync_latency * 1000:.0f} ms"

            if async_status == "TIMEOUT":
                async_text = "Timeout"
            elif async_status == "ERROR":
                async_text = "Error"
            else:
                async_text = f"{async_latency * 1000:.0f} ms"

            col1, col2, col3 = st.columns([4, 1, 1])

            col1.write(display_name(sync_url))
            col2.write(sync_text)
            col3.write(async_text)

        st.divider()

        # total
        col1, col2, col3 = st.columns([4, 1, 1])

        col1.markdown("**Total**")
        col2.markdown(f"**{sync_elapsed:.3f} s**")
        col3.markdown(f"**{async_elapsed:.3f} s**")

        st.divider()

        speedup = sync_elapsed / async_elapsed

        max_elapsed = max(sync_elapsed, async_elapsed)

        sync_ratio = sync_elapsed / max_elapsed
        async_ratio = async_elapsed / max_elapsed

        st.subheader("Execution Time")

        col1, col2 = st.columns([1, 5])
        col1.write("Sync")
        col2.progress(sync_ratio, text=f"{sync_elapsed:.3f} s")

        col1, col2 = st.columns([1, 5])
        col1.write("Async")
        col2.progress(async_ratio, text=f"{async_elapsed:.3f} s")

        st.markdown(f"**Speedup: {speedup:.2f}x**")
