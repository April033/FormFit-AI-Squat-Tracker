# FormFit 🏋️‍♂️🤖📊
### *AI-Powered Squat Tracker & Radial Biometrics Analyzer*

**FormFit** is a real-time computer vision and sports analytics application that tracks human pose landmarks to evaluate exercise form, log workout metrics, and export stunning, high-resolution radial biometrics dashboards.

Designed to replace traditional workout logging, the system automatically evaluates movement depth, logs training velocity to a CSV ledger, and generates 1080x1080 Instagram-ready radar plots of your session pace, fatigue curve, and squat consistency.

---

## 🚀 Key Features

* **Real-Time Body Pose Estimation:** Tracks left hip, left knee, and left ankle landmarks dynamically using MediaPipe's modern vision pipeline.
* **Dynamic Depth Progress Bar & HUD:** Features a vertical depth percentage bar that changes color (orange to neon green) once a valid squat depth (below 100°) is achieved.
* **Automatic Session Logging:** Writes every repetition to `session_data.csv` with precise timestamps, exact knee angles, and pace latency (seconds elapsed since the last rep).
* **HQ Radial Analytics Engine:** Generates a stunning 1080x1080 dark-mode radial chart (`session_radial.png`) showcasing:
  * **The Pace Circle:** Mapped angular progression (angle = rep number) with radial depth (distance = pace latency).
  * **Neon Glow Connections:** Point connections styled with multiple overlapping translucent orange paths.
  * **Gradient Speed Grading:** Points color-graded from bright green (fast/strong) to deep red (slow/fatigued).
  * **Dynamic Joint Depth Plotting:** Joint coordinates mapped to dot size (deeper squats = larger dots).
  * **Zone Annotations:** Automatic calculation and highlighting of "Rest Spikes" and "Fatigue Zones" on the outer rings.
  * **Session Statistics Box:** Overlay card rendering Total Reps, Average Pace, Fast and Slow Extremes, and a calculated Pace Consistency Score.

---

## 🛠️ Technology Stack

* **Python**
* **OpenCV** (Real-time video processing, skeletal rendering, and graphical UI overlays)
* **MediaPipe** (Modern Pose Landmarker Tasks API)
* **Matplotlib** (HQ polar coordinate biometric rendering)
* **NumPy** (Mathematical array manipulations)

---

## 📂 Project Structure

```text
Form Fit-main/
│
├── main.py                 # The live AI webcam squat tracker and logger
├── visualize_radial.py     # The polar fatigue visualization engine (1080x1080 exporter)
├── visualize_session.py    # The standard dark-mode linear pace graph generator
├── README.md               # Project documentation
├── requirements.txt        # Library dependencies list
└── models/
    └── pose_landmarker_full.task   # Local 15MB Pose Landmarker model file