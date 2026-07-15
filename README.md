# UniHub Project

UniHub is a comprehensive university management and student portal system built with Python, Flet (for the UI), and Firebase (for Authentication and Database).

## Features

- **Student Registration & Authentication**: Secure sign-up and login utilizing Firebase Authentication.
- **Dynamic Dashboards**: Dedicated views for students (and administrators) to manage their profiles and data.
- **Academic Tracking**: Track GPA progression, module attendance, and receive alerts for low attendance.
- **Profile Management**: Update academic details seamlessly through the interactive UI.
- **Real-time Database**: Data is stored and synchronized using Firebase Firestore.

## Technologies Used

- **Frontend / UI**: [Flet](https://flet.dev/) (Python framework based on Flutter)
- **Backend / Services**: Python 3.x
- **Database & Auth**: [Firebase](https://firebase.google.com/) Admin SDK and REST API

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Firebase Project (with Authentication and Firestore enabled)

### 2. Clone the Repository
```bash
git clone https://github.com/Ruchikaupuldeniya/UniHub-Project.git
cd UniHub-Project
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Firebase
1. In the root directory, create a `.env` file and add your Firebase configuration:
```env
FIREBASE_API_KEY="your_api_key"
FIREBASE_AUTH_DOMAIN="your_project_id.firebaseapp.com"
FIREBASE_PROJECT_ID="your_project_id"
FIREBASE_STORAGE_BUCKET="your_project_id.firebasestorage.app"
FIREBASE_MESSAGING_SENDER_ID="your_sender_id"
FIREBASE_APP_ID="your_app_id"
```
2. Download your Firebase Admin SDK Service Account Key (JSON) and place it inside the `config` folder as `config/serviceAccountKey.json`.

### 5. Run the Application
To launch the desktop application, run:
```bash
flet run main.py
```
To run it as a web app, run:
```bash
flet run main.py --web
```

## License
This project is for educational and institutional use.
