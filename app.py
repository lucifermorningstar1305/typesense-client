from typing import Dict
import streamlit as st
import traceback
import typesense
import json
import dotenv
import os

dotenv.load_dotenv()


@st.dialog("Update Document")
def update_doc(collection: str, doc_id: str, document: Dict):
    with st.form(f"update-form-{doc_id}", clear_on_submit=False):
        updated_json_str = st.text_area(
            "Edit JSON",
            value=json.dumps(document, indent=4),
            height=600,
            key=f"textarea-{doc_id}",
        )

        if st.form_submit_button("Update"):
            try:
                updated_doc = json.loads(updated_json_str)
                client.collections[collection].documents[doc_id].update(updated_doc)
                st.success(f"Updated {doc_id}")
                st.rerun()
            except Exception as e:
                traceback.print_exc()
                st.error(f"Update Failed: {e}")


@st.dialog("Delete Document")
def delete_doc(collection: str, doc_id: str):
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Delete", key=f"delete_{doc_id}"):
            try:
                client.collections[collection].documents[doc_id].delete()
                st.success(f"Deleted {doc_id}")
                st.rerun()
            except Exception as e:
                traceback.print_exc()
                st.error(f"Delete Failed: {e}")
    with col2:
        if st.button("Cancel", key=f"cancel_delete_{doc_id}"):
            st.rerun()


def validate_filter(filter_by: str) -> bool:
    return filter_by.endswith(":") or filter_by == ""


if __name__ == "__main__":

    form_placeholder = st.empty()

    if "form_data" not in st.session_state:
        with form_placeholder.form("typesense_connection_form"):
            st.header("Typesense Client")
            host = st.text_input(
                "Host",
                value=(os.getenv("TYPESENSE_HOST", "localhost")),
            )
            port = st.text_input(
                "Port",
                value=(os.getenv("TYPESENSE_PORT", "8108")),
            )
            api_key = st.text_input(
                "API-Key",
                value=(os.getenv("TYPESENSE_API_KEY", "")),
            )

            submitted = st.form_submit_button("Submit")
            if submitted:
                st.session_state["form_data"] = {
                    "host": host,
                    "port": port,
                    "api_key": api_key,
                }
                form_placeholder.empty()

    if st.session_state.get("form_data"):
        form_data = st.session_state.get("form_data")
        client = typesense.Client(
            {
                "nodes": [
                    {
                        "host": form_data["host"],
                        "port": form_data["port"],
                        "protocol": os.getenv("TYPESENSE_PROTOCOL", "http"),
                    }
                ],
                "api_key": form_data["api_key"],
                "connection_timeout_seconds": 2,
            }
        )
        collections = list()

        for collection in client.collections.retrieve():
            collections.append(collection["name"])

        with st.container(border=4):
            st.header("Collections")
            selected_collection = st.selectbox("Collections", collections)
            page = st.number_input(label="Page", min_value=1)
            page_size = st.selectbox("Page Size", [10, 25, 50, 100])
            filter_by = st.text_input("Filter", value="")
        if selected_collection:
            # st.markdown(f"Your selected collection is {selected_collection}")
            search_parameters = (
                {"q": "*", "page": page, "limit": page_size}
                if validate_filter(filter_by)
                else {
                    "q": "*",
                    "page": page,
                    "limit": page_size,
                    "filter_by": filter_by,
                }
            )

            searches = client.collections[selected_collection].documents.search(
                search_parameters
            )
            for hit in searches["hits"]:
                doc = hit["document"]
                doc_id = doc["id"]

                with st.expander(f"Document {doc_id}", expanded=True):
                    st.json(doc)

                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("Delete", key=f"delete_doc_{doc_id}"):
                            delete_doc(collection=selected_collection, doc_id=doc_id)

                    with col2:
                        if st.button("Update", key=f"update_doc_{doc_id}"):
                            update_doc(
                                collection=selected_collection,
                                doc_id=doc_id,
                                document=doc,
                            )
