🥔 Potato Leaf Disease Detection using CNN (Deep Learning)
📌 Project Summary

This project implements a Convolutional Neural Network (CNN) to automatically detect potato leaf diseases from images.
The model classifies images into Early Blight, Late Blight, and Healthy categories, helping in early disease detection for smart agriculture.

🎯 Problem Statement

Manual identification of crop diseases is time-consuming, error-prone, and requires expertise.
This project leverages Deep Learning and Computer Vision to provide an automated and scalable solution for plant disease classification.

📂 Dataset Description

Type: Image dataset

Classes: 3

Early Blight

Late Blight

Healthy

Input Size: 224 × 224 RGB images

Directory Structure:

aiml/
 ├── Early_Blight/
 ├── Late_Blight/
 └── Healthy/

🛠️ Tech Stack

Programming Language: Python

Deep Learning: TensorFlow, Keras

Image Processing: OpenCV

Data Handling: NumPy

Visualization: Matplotlib

Platform: Google Colab

🔄 Project Pipeline
1️⃣ Data Access & Setup

Mounted Google Drive for dataset access and model storage

Installed required deep learning and computer vision libraries

2️⃣ Data Preprocessing

Resized images to 224×224

Normalized pixel values (0–1 range)

Applied data augmentation:

Rotation

Zoom

Horizontal flipping

Split dataset into 80% training and 20% validation

3️⃣ Model Architecture (CNN)

Multiple Conv2D + MaxPooling layers for feature extraction

Flatten layer to convert features into vectors

Fully Connected Dense layers for classification

Dropout (0.5) to reduce overfitting

Softmax activation for multi-class prediction

4️⃣ Model Training

Optimizer: Adam

Loss Function: Categorical Crossentropy

Metric: Accuracy

Epochs: 15

5️⃣ Model Evaluation

Plotted training vs validation accuracy

Ensured stable learning and controlled overfitting

6️⃣ Prediction

Tested model on unseen potato leaf images

Returned disease label with highest probability

📊 Results

Successfully classified potato leaf images into 3 disease categories

Demonstrated effective feature extraction using CNN

Achieved consistent accuracy on validation data

💾 Model Output

Trained model saved as:

potato_disease_cnn.h5

🧠 Key Learnings

Practical understanding of CNN architecture

Image preprocessing and augmentation techniques

End-to-end deep learning workflow

Handling real-world image datasets

🚀 Future Improvements

Apply Transfer Learning (MobileNet, ResNet)

Increase dataset size for higher accuracy

Deploy model using Flask / Streamlit

Add real-time image prediction support

▶️ How to Run

Upload dataset to Google Drive

Open the notebook in Google Colab

Mount Drive

Install dependencies

Train the model

Test with new leaf images


👤 Author

Nirali Vala
Aspiring Machine Learning Engineer
