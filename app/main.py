import asyncio
import json
import streamlit as st

from app.services.document_parser import parse_document
from app.services.architecture_service import (
    generate_initial_architecture,
    generate_final_architecture,
)
from app.utils.formatting import render_architecture


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Architecture Copilot",
    page_icon="🏗️",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🏗️ Architecture Copilot")

st.subheader(
    "AI-powered Solution Architecture Assistant"
)

st.write(
    "Upload a BRD or describe your project."
)

st.markdown(
    """
The Architecture Copilot will:

- Analyze business requirements
- Design a high-level architecture
- Recommend technologies
- Provide alternatives and rationale
- Validate the architecture
- Generate a professional architecture diagram
- Accept developer feedback
- Refine the architecture
- Allow the final architecture to be downloaded
"""
)


# ============================================================
# SESSION STATE
# ============================================================

if "input_mode" not in st.session_state:

    st.session_state.input_mode = None


if "initial_result" not in st.session_state:

    st.session_state.initial_result = None


if "final_result" not in st.session_state:

    st.session_state.final_result = None


# ============================================================
# INPUT MODE
# ============================================================

st.markdown("## Start Your Architecture")

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "📄 Upload BRD",
        use_container_width=True,
    ):

        st.session_state.input_mode = "upload"


with col2:

    if st.button(
        "✍️ Describe Project",
        use_container_width=True,
    ):

        st.session_state.input_mode = "describe"


# ============================================================
# UPLOAD MODE
# ============================================================

project_input = None


if st.session_state.input_mode == "upload":

    st.markdown("### Upload BRD")

    uploaded_file = st.file_uploader(
        "Choose your BRD",
        type=[
            "pdf",
            "docx",
            "txt",
        ],
    )

    if uploaded_file:

        st.success(
            f"Selected: {uploaded_file.name}"
        )

        try:

            project_input = parse_document(
                uploaded_file.name,
                uploaded_file.getvalue(),
            )

        except Exception as exc:

            st.error(
                f"Unable to parse document: {exc}"
            )

            st.stop()


# ============================================================
# DESCRIBE MODE
# ============================================================

elif st.session_state.input_mode == "describe":

    st.markdown("### Describe Your Project")

    project_description = st.text_area(
        "Project Description",
        height=250,
        placeholder=(
            "Example:\n\n"
            "I need to build a travel website for "
            "renting bikes in metro cities in Maharashtra.\n\n"
            "Users should be able to search bikes by city, "
            "view bike details, check availability, "
            "select rental dates, make bookings and "
            "pay online.\n\n"
            "An admin should be able to manage bikes, "
            "locations, pricing and bookings."
        ),
    )

    if project_description.strip():

        project_input = project_description


# ============================================================
# GENERATE BUTTON
# ============================================================

if st.session_state.input_mode:

    st.divider()

    generate_button = st.button(
        "🚀 Generate High-Level Architecture",
        type="primary",
        use_container_width=True,
    )

    if generate_button:

        if not project_input:

            st.warning(
                "Please provide a BRD or project description."
            )

            st.stop()

        with st.spinner(
            "Architecture Copilot is designing the solution..."
        ):

            try:

                result = asyncio.run(
                    generate_initial_architecture(
                        project_input
                    )
                )

                st.session_state.initial_result = result

                st.session_state.final_result = None

                st.success(
                    "Initial architecture generated successfully."
                )

            except Exception as exc:

                st.error(
                    "Architecture generation failed."
                )

                st.exception(exc)

                st.stop()


# ============================================================
# INITIAL ARCHITECTURE
# ============================================================

if st.session_state.initial_result:

    result = st.session_state.initial_result

    st.divider()

    st.header(
        "🏗️ Proposed High-Level Architecture"
    )

    st.markdown(
        render_architecture(
            result
        )
    )

    st.divider()

    st.header(
        "👨‍💻 Developer / Technical Lead Feedback"
    )

    st.write(
        "Review the proposed architecture and "
        "request changes if required."
    )

    feedback = st.text_area(
        "Architecture Feedback",
        height=180,
        placeholder=(
            "Examples:\n\n"
            "- Use FastAPI instead of NestJS.\n"
            "- We already use Azure.\n"
            "- Do not use RabbitMQ for the POC.\n"
            "- Add Microsoft Entra ID.\n"
            "- We need support for Pune, Mumbai and Nagpur.\n"
            "- Add Redis for bike availability caching."
        ),
    )

    col1, col2 = st.columns(2)

    with col1:

        refine_button = st.button(
            "🔄 Refine Architecture",
            type="primary",
            use_container_width=True,
        )

    with col2:

        approve_button = st.button(
            "✅ Approve Architecture",
            use_container_width=True,
        )


    # ========================================================
    # REFINE
    # ========================================================

    if refine_button:

        if not feedback.strip():

            st.warning(
                "Please provide feedback before refining."
            )

        else:

            with st.spinner(
                "Refining architecture based on your feedback..."
            ):

                try:

                    final_result = asyncio.run(
                        generate_final_architecture(
                            result,
                            feedback,
                        )
                    )

                    st.session_state.final_result = (
                        final_result
                    )

                    st.success(
                        "Architecture refined successfully."
                    )

                except Exception as exc:

                    st.error(
                        "Architecture refinement failed."
                    )

                    st.exception(exc)


    # ========================================================
    # APPROVE
    # ========================================================

    if approve_button:

        st.session_state.final_result = result

        st.success(
            "Architecture approved."
        )


# ============================================================
# FINAL ARCHITECTURE
# ============================================================

if st.session_state.final_result:

    st.divider()

    st.header(
        "🎯 Final Architecture"
    )

    final_result = (
        st.session_state.final_result
    )

    st.markdown(
        render_architecture(
            final_result
        )
    )

    st.divider()

    st.subheader(
        "Download Architecture"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(
                final_result,
                indent=2,
            ),
            file_name=(
                "architecture_copilot_final.json"
            ),
            mime="application/json",
            use_container_width=True,
        )

    with col2:

        st.info(
            "PPTX export should be added next so "
            "the architecture can be directly used "
            "in client presentations."
        )
