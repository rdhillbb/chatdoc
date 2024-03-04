import streamlit as st
import json

# Example JSON structure
json_data = """
{
    "SKELETONOFTHOURHT": ["2307.15337"],
    "USAIDPOLICY": ["PA00K7SH"],
    "FIFDOCUMENT": ["FSD_BackOffice_LouiseV2-06012022", "User Manual Guide Produktif v.1.0", "FD Microfinance App_v1.2", "chroma_db"],
    "CHAINOFTHOUGHT": ["2201.11903"],
    "GARLIC": ["Garlic_ Proven health benefits and uses"],
    "OFTHOUGHTSK": ["2307.15337"]
}
"""

data = json.loads(json_data)

def main():
    if 'selections' not in st.session_state:
        st.session_state['selections'] = {}

    items = list(data.items())
    for i in range(0, len(items), 4):
        row_items = items[i:i+4]
        cols = st.columns(len(row_items))
        
        for col, item in zip(cols, row_items):
            label, options = item
            with col:
                selected_option = st.selectbox(label, ["Select an option..."] + options, key=label)
                # Update the session state upon selection
                if selected_option != "Select an option...":
                    st.session_state['selections'][label] = selected_option

    # Button to manually trigger the display of selections
    if st.button("Display Selections"):
        for label, selected in st.session_state['selections'].items():
            st.write(f"{label}: {selected}")

if __name__ == "__main__":
    main()

