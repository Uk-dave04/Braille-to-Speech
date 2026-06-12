# Chapter 3 Methodology Reference

This file is a factual source document for Chapter Three of the Braille-to-Speech project report. It is intentionally written as project information rather than polished report prose, so it can be adapted into the final report format required by the department.

Important note:
- This reference avoids deceptive wording.
- It describes the local Braille CNN/OpenCV work as part of the research and experimentation pipeline.
- It describes the implemented live prototype separately from the earlier local recognition pipeline.

## 1. Project overview

Project title:
- Braille-to-Speech Assistive System

Project goal:
- To build an assistive web-based system that accepts an image containing Braille text, extracts the text content, translates the recognized text into Yoruba, and generates speech output for users.

Target users:
- Visually impaired users
- Demonstration/research audience for a final year project

Main user workflow:
1. User uploads a Braille image through the web interface.
2. The system processes the image and extracts English text.
3. The system translates the English text into Yoruba.
4. The system generates audio output from the Yoruba text.
5. The user views the text results and plays the generated audio.

## 2. Development approach

Development style used:
- Iterative prototyping

Reason:
- The project combined image processing, machine learning, translation, speech synthesis, and web deployment.
- Several parts had to be refined through repeated testing, especially image recognition on real Braille photographs.

Main development phases:
1. Problem definition and requirement analysis
2. Initial system architecture design
3. Development of local image preprocessing and Braille segmentation pipeline
4. Development of local CNN model for Braille cell classification
5. Integration of web app upload and result flow
6. Integration of recognition, translation, and speech modules
7. Testing, debugging, optimization, and deployment

## 3. Functional requirements

The system is designed to:
1. Accept uploaded image files containing Braille.
2. Validate supported file types.
3. Process the uploaded image.
4. Extract Braille content as text.
5. Produce readable English text output.
6. Translate the English text into Yoruba.
7. Generate speech audio from the Yoruba text.
8. Display results in a web page.
9. Display meaningful error messages when processing fails.

Supported image formats in the app:
- `.png`
- `.jpg`
- `.jpeg`
- `.bmp`
- `.webp`

## 4. Non-functional requirements

Key non-functional goals:
- Usability
- Reliability
- Maintainability
- Modularity
- Portability
- Reasonable response time

Usability considerations:
- Simple upload process
- Clear result display
- Inline error feedback
- Loading state during processing

Maintainability considerations:
- Modular Python package structure
- Separation of web, recognition, translation, speech, and utility code
- Automated tests for key modules

## 5. Tools and technologies used

### 5.1 Programming language
- Python

Why it was used:
- Strong support for computer vision
- Strong support for machine learning
- Large ecosystem for web development and API integration

### 5.2 Web framework
- Flask

Used for:
- Routing
- File upload handling
- Template rendering
- Returning result and error pages

### 5.3 Frontend technologies
- HTML
- CSS
- Minimal JavaScript

Used for:
- Upload page
- Result page
- Loading state overlay
- Inline error display

### 5.4 Image processing libraries
- OpenCV
- Pillow

Used for:
- Local preprocessing research pipeline
- Image enhancement
- Thresholding
- Segmentation experiments
- Lightweight image preparation before recognition

### 5.5 Machine learning framework
- TensorFlow / Keras

Used for:
- CNN model design
- Training
- Evaluation
- Local Braille cell classification experiments

### 5.6 Data and scientific libraries
- NumPy
- scikit-learn
- matplotlib
- seaborn

Used for:
- Numeric operations
- Dataset handling
- Evaluation
- Visualization such as confusion matrix generation

### 5.7 Translation and recognition services in implemented prototype
- Multimodal image-to-text service for Braille recognition
- Language generation service for English-to-Yoruba translation

Used for:
- Practical live recognition of difficult Braille images
- Yoruba text generation in the deployed prototype

### 5.8 Speech synthesis
- Spitch

Used for:
- Yoruba audio generation

### 5.9 Deployment and version control
- Git
- GitHub
- Render

Used for:
- Version control
- Remote repository hosting
- Live deployment

## 6. System architecture

High-level live system flow:

`Image upload -> image enhancement -> Braille recognition -> English text -> Yoruba translation -> Yoruba speech synthesis -> web output`

The system is modular and consists of:
1. Input module
2. Runtime file handling module
3. Image enhancement module
4. Recognition module
5. Translation module
6. Text-to-speech module
7. Web presentation module

## 7. Module-by-module description

### 7.1 Input module

Main responsibility:
- Receive uploaded image from the user

Implementation notes:
- The upload route is defined in `app.py`
- File extension is validated before processing
- Uploaded files are saved to a runtime directory before recognition

Current runtime storage behavior:
- In the deployed app, runtime uploads and generated audio are written to a temp-backed runtime directory instead of the repository directory

Relevant files:
- `C:\Users\User\Desktop\braille_dev\app.py`
- `C:\Users\User\Desktop\braille_dev\config.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\io.py`

### 7.2 Image enhancement module

Main responsibility:
- Improve the uploaded image before recognition

Local research pipeline behavior:
- Grayscale conversion
- Blur
- Contrast normalization
- Histogram equalization
- Adaptive thresholding
- Morphological cleanup

Implemented live prototype behavior:
- Lightweight enhancement with Pillow
- Grayscale conversion
- Auto-contrast
- Upscaling before recognition request

Reason for simplified production enhancement:
- The deployed system no longer runs the heavy local CNN recognition path in production
- A lighter image preparation path reduced deployment complexity and kept the live app focused on the recognition/translation/speech workflow

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\preprocess.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\gemini_fallback.py`

### 7.3 Local Braille recognition research pipeline

This was part of the experimental/research pipeline and is retained in the codebase for local training and experimentation.

Pipeline stages explored:
1. Image preprocessing
2. Dot detection
3. Line grouping
4. Cell grouping
5. Braille cell cropping
6. CNN classification
7. Text reconstruction

Initial segmentation approach:
- Contour-based extraction of candidate Braille cells

Observed problem:
- This was too fragile for dense, full-page Braille photographs
- Dots were often merged or split incorrectly

Improved segmentation approach:
- Dot-first segmentation
- Detect individual embossed dot candidates
- Group dots into lines
- Estimate spacing
- Infer Braille cell boundaries from dot geometry

Reason local pipeline performance was limited:
- Real images contained skew, uneven lighting, blur, background noise, and varying embossing patterns
- Domain mismatch existed between training crops and real camera-acquired Braille photos

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\segment.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\reconstruct.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\pipeline.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\inference.py`

### 7.4 CNN model module

Purpose:
- Classify cropped Braille cell images into one of the possible six-dot Braille patterns

Recognition strategy used:
- Pattern-based classification instead of direct letter classification

Why pattern-based classification was chosen:
- Braille is fundamentally a structured dot encoding system
- Pattern-level classification separates visual recognition from text decoding
- It is easier to extend and debug than direct character classification

Output class structure:
- 64 possible six-dot Braille patterns

General model structure:
1. Input layer
2. Convolution layers
3. ReLU activations
4. Pooling layers
5. Dropout layers
6. Flatten layer
7. Dense output layer with softmax

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\model.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\train.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\evaluate.py`

### 7.5 Recognition module in implemented prototype

Purpose:
- Extract English text from Braille image in the live deployed system

Behavior:
- The uploaded image is sent through the production recognition path
- The returned text is normalized before further processing

Important implementation distinction:
- The local OpenCV/CNN pipeline remains part of the research codebase
- The deployed prototype uses an external recognition path for stronger real-world reliability

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\gemini_fallback.py`
- `C:\Users\User\Desktop\braille_dev\app.py`

### 7.6 Translation module

Purpose:
- Convert recognized English text to Yoruba

Behavior:
- English text is cleaned and normalized
- Yoruba translation is requested
- Result is normalized for speech use

Output object contains:
- source text
- translated text
- translation usage status
- fallback or error information when relevant

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\translation.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\utils.py`

### 7.7 Text-to-speech module

Purpose:
- Generate Yoruba audio from translated text

Behavior:
- The synthesized audio is written as a `.wav` file
- The result page exposes an audio player to play the generated file

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\tts.py`
- `C:\Users\User\Desktop\braille_dev\app.py`

### 7.8 Web presentation module

Purpose:
- Present the user interface and results

Current UI screens:
1. Upload page
2. Loading state overlay
3. Result page
4. Inline error card on the upload page

Displayed result information:
- Recognized English text
- Yoruba translated text
- Speech status
- Audio playback control

Relevant files:
- `C:\Users\User\Desktop\braille_dev\templates\index.html`
- `C:\Users\User\Desktop\braille_dev\templates\result.html`
- `C:\Users\User\Desktop\braille_dev\static\style.css`

## 8. Dataset and training information

### 8.1 Dataset format used for local model training

Prepared dataset format:
- Folder-per-class structure
- Each folder name represents a six-dot Braille pattern
- Each folder contains cropped single-cell images

Example structure:

```text
data/processed/
  100000/
    sample_001.png
  110000/
    sample_002.png
```

### 8.2 Datasets used or explored

Baseline cropped character dataset:
- `braille_segment_character_natural`

Additional dataset used for training expansion:
- DSBI dataset

Other dataset considered for realism:
- Angelina Braille dataset

### 8.3 Dataset preparation

Custom preparation scripts were written to:
- Process character dataset into class folders
- Process DSBI annotations into class-folder crops
- Support multi-dataset loading for training

Relevant files:
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\prepare_character_dataset.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\prepare_dsbi_dataset.py`
- `C:\Users\User\Desktop\braille_dev\src\braille_system\modeling\dataset.py`

### 8.4 Training procedure

General local model training procedure:
1. Load image paths and labels
2. Resize images to model input size
3. Normalize image values
4. Split into training and validation sets
5. Train the CNN
6. Save model artifact
7. Save label file
8. Evaluate model on validation data

### 8.5 Model evaluation

Metrics used:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

Observed result:
- Local model performance on curated cell crops was much better than on difficult real-world page photographs

Reason:
- Domain mismatch between training data and real image conditions

## 9. Live application workflow

Operational flow in the current live web app:
1. User opens the upload page
2. User uploads a supported image file
3. File is saved to the runtime upload directory
4. Image enhancement is applied
5. Braille is recognized as English text
6. English text is normalized
7. English text is translated into Yoruba
8. Yoruba text is synthesized into audio
9. Result page displays English text, Yoruba text, and audio

## 10. Error handling and reliability work

The app was designed to handle common failure points without crashing.

Handled failure cases:
- Missing image upload
- Unsupported file extension
- Upload storage failure
- Recognition failure
- Translation failure
- Speech synthesis failure

UI behavior on failure:
- Returns to upload page with inline error message

Deployment reliability fixes implemented:
- Runtime file writes moved to temporary storage
- Production dependencies split from heavy local research dependencies
- Gunicorn timeout increased on Render because recognition, translation, and speech requests can take much longer than the default worker timeout

## 11. Testing strategy

### 11.1 Automated tests

Automated tests were written for:
- Flask routes
- Upload validation
- Recognition service wrapper behavior
- Translation service wrapper behavior
- Text-to-speech wrapper behavior
- Error rendering paths
- Dataset preparation logic
- Model-side helper functions

Relevant test files:
- `C:\Users\User\Desktop\braille_dev\tests\test_app.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_gemini_service.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_translation.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_tts.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_dataset.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_pipeline.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_segment.py`
- `C:\Users\User\Desktop\braille_dev\tests\test_preprocess.py`

### 11.2 Manual tests

Manual testing covered:
- Close-up Braille images
- Full-page Braille images
- Images with skew and lighting differences
- Error cases during recognition, translation, and TTS
- Deployed app behavior on Render

## 12. Deployment methodology

### 12.1 Source control
- Git was used for local version control
- GitHub was used as the remote repository

Repository:
- `https://github.com/Uk-dave04/Braille-to-Speech`

### 12.2 Hosting platform
- Render

Live deployment URL:
- `https://braille-to-speech-assistive.onrender.com`

### 12.3 Production deployment adjustments

Production deployment required:
- a lightweight production dependency file
- runtime temp storage
- higher Gunicorn timeout
- environment variables for external services

Deployment-related files:
- `C:\Users\User\Desktop\braille_dev\render.yaml`
- `C:\Users\User\Desktop\braille_dev\requirements-render.txt`

## 13. Key implementation limitations

These points are important for the report discussion section:

1. Local Braille recognition with traditional CV/CNN methods was sensitive to real-world image quality.
2. Full-page Braille photographs were much harder than cropped cell images.
3. Recognition quality depended heavily on lighting, angle, blur, and spacing.
4. Translation and speech in the implemented prototype depend on external services and internet connectivity.
5. End-to-end response time in deployment can be noticeable because the app performs recognition, translation, and speech generation sequentially.

## 14. Good points to mention in your actual Chapter 3 write-up

If you are turning this into report prose later, useful emphasis points are:
- The project was developed iteratively.
- A local CV/CNN pipeline was designed and evaluated as part of the research work.
- Real-world testing revealed limits of local Braille page recognition under unconstrained conditions.
- The final live prototype was organized as a modular recognition-translation-speech web system.
- The modular structure allows future replacement or improvement of any one component.

## 15. Suggested chapter 3 subsection structure

If you want to convert this into formal report headings later, this structure will work well:

1. Introduction
2. Research Design
3. System Requirements Analysis
4. Tools and Technologies Used
5. System Architecture
6. Local Braille Recognition Research Pipeline
7. CNN Model Development
8. Implemented Prototype Workflow
9. User Interface Design
10. Testing Strategy
11. Deployment Method
12. Limitations of the Method
13. Summary
