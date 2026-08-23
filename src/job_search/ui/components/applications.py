"""Application tracker table and add/edit form."""

from __future__ import annotations

import streamlit as st

from job_search.models.schemas import TrackedApplication, TrackerChannel, TrackerStatus
from job_search.tools.tracker import TrackerStore

CHANNEL_OPTIONS = [item.value for item in TrackerChannel]


def render_applications_table(store: TrackerStore, items: list[TrackedApplication]) -> None:
    st.subheader("Applications")
    editing_id = st.session_state.get("edit_id")
    editing = store.get(editing_id) if editing_id else None

    with st.form("application_form", clear_on_submit=not editing):
        c1, c2, c3, c4, c5, c6 = st.columns([1.2, 1.2, 1.0, 1.1, 1.1, 0.8])
        with c1:
            company = st.text_input(
                "Company",
                value=editing.company if editing else "",
            )
        with c2:
            role = st.text_input(
                "Role",
                value=editing.role if editing else "",
            )
        with c3:
            sector = st.text_input(
                "Sector",
                value=editing.sector if editing else "",
                placeholder="Data & AI",
            )
        with c4:
            status_options = [item.value for item in TrackerStatus]
            default_status = editing.status.value if editing else TrackerStatus.ACTIVE.value
            status = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(default_status),
            )
        with c5:
            default_channel = editing.channel.value if editing else TrackerChannel.ONLINE.value
            channel = st.selectbox(
                "Channel",
                CHANNEL_OPTIONS,
                index=CHANNEL_OPTIONS.index(default_channel),
            )
        with c6:
            st.write("")
            st.write("")
            label = "Save changes" if editing else "Add / update"
            submitted = st.form_submit_button(label, type="primary", use_container_width=True)

    if submitted:
        if not company.strip() or not role.strip():
            st.warning("Company and role are required.")
        elif editing:
            store.update(
                editing.id,
                company=company.strip(),
                role=role.strip(),
                sector=sector.strip(),
                status=TrackerStatus(status),
                channel=TrackerChannel(channel),
            )
            st.session_state.edit_id = None
            st.success("Application updated.")
            st.rerun()
        else:
            store.add(
                company,
                role,
                sector,
                TrackerStatus(status),
                channel=TrackerChannel(channel),
            )
            st.success("Application added.")
            st.rerun()

    if editing and st.button("Cancel edit"):
        st.session_state.edit_id = None
        st.rerun()

    if not items:
        st.info("No applications yet. Add one above.")
        return

    header = st.columns([1, 1.3, 1.4, 1.1, 1.3, 1.2, 0.6, 0.6])
    for col, title in zip(
        header,
        ["Date", "Company", "Role", "Sector", "Status", "Channel", "Edit", "Delete"],
        strict=True,
    ):
        col.markdown(f"**{title}**")

    for item in items:
        row = st.columns([1, 1.3, 1.4, 1.1, 1.3, 1.2, 0.6, 0.6])
        row[0].write(item.date)
        row[1].write(item.company)
        row[2].write(item.role)
        row[3].write(item.sector or "—")
        new_status = row[4].selectbox(
            "status",
            [status.value for status in TrackerStatus],
            index=[status.value for status in TrackerStatus].index(item.status.value),
            key=f"status-{item.id}",
            label_visibility="collapsed",
        )
        if new_status != item.status.value:
            store.update(item.id, status=TrackerStatus(new_status))
            st.rerun()
        new_channel = row[5].selectbox(
            "channel",
            CHANNEL_OPTIONS,
            index=CHANNEL_OPTIONS.index(item.channel.value),
            key=f"channel-{item.id}",
            label_visibility="collapsed",
        )
        if new_channel != item.channel.value:
            store.update(item.id, channel=TrackerChannel(new_channel))
            st.rerun()
        if row[6].button("Edit", key=f"edit-{item.id}", use_container_width=True):
            st.session_state.edit_id = item.id
            st.rerun()
        if row[7].button("Delete", key=f"delete-{item.id}", use_container_width=True):
            store.delete(item.id)
            if st.session_state.get("edit_id") == item.id:
                st.session_state.edit_id = None
            st.rerun()
