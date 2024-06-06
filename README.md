# AI Personal Trainer

Welcome to the AI Personal Trainer project! This project leverages MediaPipe for pose detection and OpenCV for video processing to count push-ups in a given video. It uses Streamlit for the front-end interface, making it easy to visualize and interact with the results.

![Personal Trainer AI](https://github.com/christianduhp/christianduhp/assets/85292359/de818d20-5c55-4b39-a610-c877cfa9ac22)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Detailed Code Explanation](#detailed-code-explanation)
  - [PersonalAI Class](#personalaiclass)
  - [Push-Up Logic](#push-up-logic)
  - [Data Processing](#data-processing)
- [Streamlit Interface](#streamlit-interface)

## Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/christianduhp/ai-personal-trainer.git
   cd ai-personal-trainer
   ```

2. **Install the required packages**:
   Make sure you have Python 3.7+ installed. Then install the required dependencies using pip:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application**:

   ```sh
   streamlit run app.py
   ```

2. **Choose a video and a model**:
   Use the Streamlit interface to choose a video and a model.

3. **Adjust settings**:

   - Select frames to skip.
   - Resize video as needed.
   - Enable or disable displaying charts.

4. **Start the analysis**:
   The application will process the video, detect poses, and count push-ups, displaying the results in real-time.

## Project Structure

```
ai-personal-trainer/
│
├── app.py
├── modules/
│   ├── pushup_logic.py
│   └── data_processing.py
├── personal_ai.py
├── requirements.txt
└── README.md
```

- **app.py**: The main file to run the Streamlit interface.
- **modules/**: Contains the logic for push-up detection and data processing.
  - **pushup_logic.py**: Contains the logic for counting push-ups.
  - **data_processing.py**: Functions for processing data and displaying results.
- **personal_ai.py**: Defines the `PersonalAI` class for handling video processing and pose detection.
- **requirements.txt**: Lists the required Python packages.
- **README.md**: This file.

## Detailed Code Explanation

### PersonalAI Class

This class handles video processing and pose detection using MediaPipe and OpenCV.

**Key Methods**:

- **`__init__`**: Initializes the class with video file, model path, and various options.
- **`find_angle`**: Calculates the angle between three landmarks.
- **`_draw_landmarks_on_image`**: Draws pose landmarks on the image.
- **`_process_frame`**: Processes a single video frame, resizing and drawing landmarks.
- **`_process_video`**: Reads and processes the video, frame by frame.
- **`run`**: Starts the video processing in a separate thread.

### Push-Up Logic

The `pushup_logic.py` module contains the logic for counting push-ups based on detected elbow and hip angles.

**Key Functions**:

- **`pushup`**: Determines the status of the push-up (ready, down, up) and counts repetitions.

### Data Processing

The `data_processing.py` module handles the processing of detected pose landmarks and displaying results using Streamlit.

**Key Functions**:

- **`process_df_angles`**: Processes the detected landmarks and appends them to a DataFrame.
- **`display_cols`**: Displays the status, count, frame, and optional charts in the Streamlit interface.

### Streamlit Interface

**app.py**: The main script that runs the Streamlit application.

- Sets up the Streamlit interface.
- Handles user input and video selection.
- Initializes the `PersonalAI` class and starts video processing.
- Continuously updates and displays the processed video frames and push-up count.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
