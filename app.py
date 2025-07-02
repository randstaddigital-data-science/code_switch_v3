import streamlit as st
from code_switch.functions import convert_code, generate_documentation, check_syntax
from code_switch.language_detection import detect_language

def main():
    st.title("Code Language Converter: Switch Code Fast")

    # with header_col2:
    st.markdown(
    """
    <p style='font-size: 20px;'>The Code Language Converter is your personal coding assistant, simplifying how you adapt code to fit different systems or languages.</p>

    <h4 style='font-size: 22px;'>Why Use It?</h4>
    <ul style='font-size: 22px;'>
        <li style="font-size: 20px; line-height: 1.1; margin-bottom: 28px;"><strong>Automatic Language Detection:</strong> Automatically identifies programming languages for seamless processing.</li>
        <li style="font-size: 20px; line-height: 1.1; margin-bottom: 28px;"><strong>Rapid Development:</strong> Simplifies development and achieves up to 70% faster delivery.</li>
        <li style="font-size: 20px; line-height: 1.1; margin-bottom: 28px;"><strong>Ensures Quality:</strong> Ensures accurate and reliable transformation of code with clear business logic explanations.</li>
        <li style="font-size: 20px; line-height: 1.1; margin-bottom: 28px;"><strong>Helps You Learn:</strong> Provides clear explanations so you can understand the code better.</li>
    </ul>

    <h4 style='font-size: 22px;'>How It Helps</h4>
    <p style='font-size: 20px;'>Great for developers, students, or anyone managing diverse systems.</p>
    """,
    unsafe_allow_html=True
)

    # Add a separator
    st.markdown("---")

    st.subheader("Upload Source Code and Select Target Language:")
    uploaded_file = st.file_uploader("Upload Source Code", type=["txt"])
    target_language = st.selectbox(
        "Select Target Language", ["Python", "Java", "C++", "COBOL"]
    )
    source_code = st.text_area(
        "Or paste your source code here",
        height=300,
        placeholder="Paste your source code here...",
    )

    if uploaded_file is not None:
        source_code = uploaded_file.read().decode("utf-8")

    if "converted_code" not in st.session_state:
        st.session_state.converted_code = ""
    if "documentation" not in st.session_state:
        st.session_state.documentation = ""
    if "syntax_result" not in st.session_state:
        st.session_state.syntax_result = ""

    if source_code:
        detected_language = detect_language(source_code)
        st.info(f"Detected Source Language: {detected_language}")

        if st.button("Convert Code"):
            if detected_language != "Unknown":
                with st.spinner("Converting..."):
                    converted_code = convert_code(
                        source_code, detected_language, target_language
                    )
                    st.session_state.converted_code = converted_code
                    st.session_state.documentation = ""
                    st.session_state.syntax_result = ""

        # Use containers for better spacing
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original Code:")
                st.markdown(f"```{detected_language.lower()}\n{source_code}\n```")

            with col2:
                st.subheader("Converted Code:")
                if st.session_state.converted_code:
                    st.markdown(
                        f"```{target_language.lower()}\n{st.session_state.converted_code}\n```"
                    )

        if st.session_state.converted_code:
            st.markdown("###")

            # Syntax check button
            if st.button("Evaluate Code (Python & Java only)"):
                with st.spinner("Checking Syntax....."):
                    syntax_output = check_syntax(
                        st.session_state.converted_code, target_language
                    )
                    st.session_state.syntax_result = (
                        f"Syntax Check Output:\n{syntax_output}"
                    )

            # Display Syntax Check Result
            if st.session_state.syntax_result:
                st.subheader("Syntax Check Result:")
                st.write(st.session_state.syntax_result)

                # Generate Explanation button appears after syntax result
                if st.button("Generate Explanation"):
                    with st.spinner("Generating..."):
                        documentation = generate_documentation(
                            st.session_state.converted_code, target_language
                        )
                        st.session_state.documentation = documentation

        # Display Code Explanation
        if st.session_state.documentation:
            st.subheader("Code Explanation:")
            st.markdown(
                f"<div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>{st.session_state.documentation}</div>",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()
