import pandas as pd


def process_df_angles(landmarks, df_nodes_y, ts):
    df_y = (
        pd.DataFrame([i.y for i in [i for i in landmarks.pose_landmarks[0]]])
        .rename(columns={0: ts})
        .transpose()
    )

    df_nodes_y = pd.concat([df_nodes_y, df_y])

    return df_nodes_y


def display_cols(status, count, frame, display_charts, df_nodes_y, placeholder):
    import streamlit as st

    landmark_names = {
        11: "Left shoulder",
        12: "Right shoulder",
        24: "Right hip",
        23: "Left hip",
        14: "Right elbow",
        13: "Left elbow",
    }

    with placeholder.container():
        col1, col2 = st.columns([0.4, 0.6])
        status_m = f":red[{status}]" if status == "relaxed" else f":green[{status}]"
        col2.markdown("### **Status:** " + status_m)
        col2.markdown(f"### Count: {int(count)}")

        col2.divider()
        col1.image(frame)

        if display_charts:
            col2.line_chart(
                df_nodes_y[[i for i in landmark_names]].rename(columns=landmark_names)
            )
