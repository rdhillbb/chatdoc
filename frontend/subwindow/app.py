import streamlit as st
import json

# Example JSON list/array
json_data = '''
[
    {"cabinetname": "Cabinet 1", "summary": "Summary of Cabinet 1"},
    {"cabinetname": "Cabinet 2", "summary": "Summary of Cabinet 2"},
    {"cabinetname": "Cabinet 3", "summary": "Summary of Cabinet 3"},
    {"cabinetname": "Cabinet 4", "summary": "Summary of Cabinet 4"},
    {"cabinetname": "Cabinet 5", "summary": "Summary of Cabinet 5"},
    {"cabinetname": "Cabinet 6", "summary": "Summary of Cabinet 6"},
    {"cabinetname": "Cabinet 7", "summary": "Summary of Cabinet 7"},
    {"cabinetname": "Cabinet 8", "summary": "Summary of Cabinet 8"},
    {"cabinetname": "Cabinet 9", "summary": "Summary of Cabinet 9"}
]
'''

# Convert JSON string into Python list of dictionaries
cabinets = json.loads(json_data)

def display_buttons_in_rows(cabinets, buttons_per_row=4):
    # Calculate the number of rows needed
    num_rows = len(cabinets) // buttons_per_row + int(len(cabinets) % buttons_per_row > 0)
    
    for row in range(num_rows):
        # Streamlit columns for buttons
        cols = st.columns(buttons_per_row)
        
        for col in cols:
            # Calculate the index of the cabinet in the list
            index = row * buttons_per_row + cols.index(col)
            if index < len(cabinets):
                cabinet = cabinets[index]
                # Create a button with cabinetname as label and summary as tooltip
                if col.button(cabinet["cabinetname"], help=cabinet["summary"]):
                    # Display the clicked cabinetname
                    st.write(f"You clicked: {cabinet['cabinetname']}")

def main():
    st.title('Cabinet Selection')
    display_buttons_in_rows(cabinets)

if __name__ == '__main__':
    main()

