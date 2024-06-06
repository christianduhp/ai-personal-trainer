import streamlit as st
import pandas as pd
import os
from personal_ai import PersonalAI
from modules.pushup_logic import pushup
from modules.data_processing import process_df_angles, display_cols

import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf")


if __name__ == "__main__":

    # Configuração do Streamlit
    st.set_page_config(layout="wide", page_title="AI Personal Trainer")
    st.sidebar.title("AI Personal Trainer")

    videos = [i for i in (os.listdir("videos"))]
    video = st.sidebar.selectbox("Select a video", (videos))

    models = [i for i in (os.listdir("models"))]
    model = st.sidebar.selectbox("Select a model", (models))

    display_charts = st.sidebar.checkbox("Display charts", value=True)
    
    frame_skip = st.sidebar.select_slider(
        "Select Frames to Skip", options=[i for i in range(1, 11)], value=(2)
    )
    resize_scale = st.sidebar.select_slider(
        "Resize Video", options=[i for i in range(0, 101)], value=(50)
    )
    reset = st.sidebar.button("Reset")
    placeholder = st.empty()

    # Instancia classe
    personal_ai = PersonalAI(
        os.path.join("videos", video),
        os.path.join("models", model),
        resize=True,
        resize_scale=resize_scale / 100,
        streamlit=True,
        frame_skip=frame_skip,
    )
    personal_ai.run()

    # Inicialização de variáveis
    status = "relaxed"
    count = 0
    direction = None
    df_nodes_y = pd.DataFrame()

    # Loop principal
    while True:
        frame, landmarks, ts = personal_ai.image_q.get()
        if ts == "done":
            break

        if len(landmarks.pose_landmarks) > 0:
            frame, elbow_angle, _ = personal_ai.find_angle(frame, landmarks, 12, 14, 16)
            frame, hip_angle, _ = personal_ai.find_angle(frame, landmarks, 11, 23, 25)

            df_nodes_y = process_df_angles(landmarks, df_nodes_y, ts)

            status, count, direction = pushup(
                status, count, elbow_angle, hip_angle, direction
            )

            display_cols(status, count, frame, display_charts, df_nodes_y, placeholder)
