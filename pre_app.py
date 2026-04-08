import streamlit as st
import pandas as pd

# Hide Streamlit menu + deploy button
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.set_page_config(layout="wide")

current_time:int = 0 # current time in the timeline, should be updated by the timeline slider and the play button, sync with the setpoints displayed in the live output and the sensors displayed in the input
play:bool = False # see if we should be counting forward in the timeline, should be toggled by the play button, if True, current_time should automatically step forward by 1 unit every second, if False, current_time should not change

sensor_log_df:pd.DataFrame = None # this will be the dataframe that is generated from the log CSV, it will have columns "Time", "Sensor1", "Sensor2", etc. where each sensor is a column and the values are the sensor readings at that time
processed_setpoints_df:pd.DataFrame = None # this will be the dataframe that is generated from the log_df and the current_time, it will have columns "Time", "FL_Setpoint", "FR_Setpoint", "BL_Setpoint", and "BR_Setpoint"

max_time:int = 1000 # this will be the maximum time in the timeline, it should be the maximum value in the "Time" column of the sensor_log_df, it should also be the maximum value of the timeline slider

with st.container():
    log_col, timing_col, download_col, logo_col = st.columns([4, 3, 4, 4])

    with log_col:
        # st.markdown('<div style="background-color:#FADBD8; padding:20px; border-radius:10px"></div>', unsafe_allow_html=True)
        log_col_selector, log_col_link = st.columns([5, 1])
        with log_col_selector:
            # select log from dropdown, then load log_df with the selected log's CSV
            options = ["Option 1", "Option 2", "Option 3"] # this will be the paths in the ./logs folder
            selected_option = st.selectbox("Select Log:", options, label_visibility="collapsed")

            # also max time should be updated to be the maximum value in the "Time" column of the selected log's CSV

        with log_col_link:
            # button to open log CSV in new tab, link should be the path to the selected log's CSV
            open_link = st.link_button('', 'https://example.com', icon="↗️", help="Open log CSV in new tab")

    with timing_col :
        timing_col_reset, timing_col_backstep, timing_col_play, timing_col_frontstep = st.columns([1, 1, 1, 1])

        with timing_col_reset :
            # button to reset timeline to 0, should also set play to False and current_time to 0
            reset = st.button('', icon="🔃")

        with timing_col_backstep:
            # step back in timeline by 1 unit, should also set play to False
            backstep = st.button('', icon="⬅️")
        
        with timing_col_play:
            # toggle play/pause, if play is True, timeline should automatically step forward by 1 unit every second, if False, timeline should not change
            # "▶️" or "⏸️"
            play = st.button("⏸️", callable)

        with timing_col_frontstep:
            # step forward in timeline by 1 unit, should also set play to False
            frontstep = st.button('', icon="➡️")

        # timeline slider, should be disabled if play is True, should update current_time when changed
        curret_time = st.slider("Timeline", 0, max_time, current_time + frontstep - backstep, label_visibility="collapsed", width="stretch")

    st.divider()

    with logo_col :
        st.subheader("CWRU Baja - [cwru-baja](https://github.com/cwru-baja)", divider="red")
        pass


with st.container():

    input_col, output_col = st.columns(2)
    with input_col :
        st.subheader("Input", divider="green")
        sensors_tab, code_tab, docs_tab = st.tabs(["Sensors", "Code", "Docs"])

        with sensors_tab :
            # show the sensors in a dataframe, should be the sensors from the log_df at the current_time (ie one row of the log_df), should have columns "ID", "Name", and "Value"
            # each sensor is a column in the dataframe so it will need to be rotated and have the columns renamed to "ID", "Name", and "Value"
            sensors_df = pd.DataFrame({ 'ID':[], 'Name': [], 'value': [] })

            sensors_df.loc[len(sensors_df)] = [0, "Test", 67.6]
            st.dataframe(sensors_df, hide_index=True)

            # display curret time, should NOT update current_time, do not allow changes on this slider
            st.slider("Sensor_Timeline", 0, max_time, curret_time, label_visibility="collapsed", width="stretch", disabled=True)

        
        with code_tab :
            # save the processed setpoints to a CSV, should be the processed_setpoints_df, should have columns "Time", "FL_Setpoint", "FR_Setpoint", "BL_Setpoint", and "BR_Setpoint"
            st.button("Save")
            code_text = st.text_area("Code Area", label_visibility="collapsed", height="stretch", placeholder="set(0.8)")

            # the code in the code_text area should be executed and the setpoints should be updated based on the code, the code should be able to access the current_time and the sensor_log_df, and it should be able to update the processed_setpoints_df based on the code, for example, if the code is "set(0.8)", it should set all the setpoints in the processed_setpoints_df at the current_time to 0.8
            # make it easy for this to be given new funcatialy later

        with docs_tab :
            st.subheader("Documentation")
            st.text("There are no docs, y'all cooked.")


    with output_col:
        st.subheader("Output", divider="orange")

        _, live_output, car_img, _ = st.columns([2, 2, 2, 2])

        with live_output :

            # get the setpoints from the processed_setpoints_df at the current_time, should be the row of the processed_setpoints_df where "Time" is equal to current_time, should have columns "FL_Setpoint", "FR_Setpoint", "BL_Setpoint", and "BR_Setpoint"
            FL_setpoint = 1
            FR_setpoint = 2
            BL_setpoint = 3
            BR_setpoint = 4

            # set delta to be the difference between the current setpoint and the previous setpoint, should be the value in the processed_setpoints_df at the current_time - 1, should have columns "FL_Setpoint", "FR_Setpoint", "BL_Setpoint", and "BR_Setpoint"

            FL_cell, FR_cell = st.columns(2, vertical_alignment="center")
            BL_cell, BR_cell = st.columns(2)

            with FL_cell:
                st.metric(label="FL", value=round(FL_setpoint, 2), delta=10)

            with FR_cell:
                st.metric(label="FR", value=round(FR_setpoint, 2), delta=10)

            with BL_cell:
                st.metric(label="BL", value=round(BL_setpoint, 2), delta=10)

            with BR_cell:
                st.metric(label="BR", value=round(BR_setpoint, 2), delta=10)

        # just a fun image of a car, should be the same width as the live_output above, should be centered in the column
        with car_img:
            st.space(20)
            st.image("https://png.pngtree.com/png-vector/20230110/ourmid/pngtree-car-top-view-image-png-image_6557068.png", width="stretch")

         # display curret time, should NOT update current_time, do not allow changes on this slider
        st.slider("Suspension_Timeline", 0, max_time, curret_time, label_visibility="collapsed", width="stretch", disabled=True)