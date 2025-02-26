#  Romanian Language Learning App

A Streamlit application for learning Romanian language, featuring translation and image text recognition capabilities.

## Features

### 1. Learning Interface (000_Learn_Romanian.py)
- Browse vocabulary by difficulty levels:
  - Beginner
  - Intermediate
  - Advanced
- Words organized by practical categories
- Expandable sections for easy reference
- Bilingual display (Romanian - English)

### 2. Image Translation 🆕
- Upload images containing Romanian text for translation
- Supports PNG, JPG, and JPEG formats
- Uses OpenAI's Vision API for accurate text recognition
- Rate limited to 4 requests per 60 seconds
- High-detail mode for better text recognition

#### Example Screenshots:
- [Writting Practice Homepage](images/writing-practice_homepage.png)
- [Text Recognition Example](images/text-in-Romana.png)
- [Successful Writting](images/practice-writing_success.png)
- [Unsucessful Writing Practice Feedback](images/writing-practice_error1.png)
- [Helpful Feedback](images/writing-practice_error2.png)
- [Image Translation Interface](images/Image-translation.png)

## Technical Details

### Environment Setup
- Uses `.env` file for API key configuration
- Requires OpenAI API key with GPT-4 Vision access
- Rate limiting implemented for API usage control

### Vision API Features
- High-detail mode for better text recognition
- System role prompting for accurate translations
- Error handling for model availability and billing issues
- Automatic model selection from available vision models

### Dependencies
```
Pillow==11.0.0
streamlit==1.40.2
python-certifi-win32==1.6.1
openai>=1.12.0
python-dotenv==1.0.1
httpx>=0.24.1
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kana--streamlit-app.git
cd kana--streamlit-app
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```plaintext
OPENAI_API_KEY=your_api_key_here
PROJECT_ID=your_project_id_here
ORG_ID=your_org_id_here (optional)
```

5. Run the application:
```bash
streamlit run init_streamlit_app.py
```

## Usage

### Image Translation
1. Navigate to the "Image Translation" page
2. Upload an image containing Romanian text
3. Click "Translate Text"
4. View the original Romanian text and English translation

### Rate Limits
- Maximum 4 requests per 60 seconds
- Sidebar displays current request count
- Wait time shown when limit is reached

## Error Handling
- Checks for API key availability
- Verifies GPT-4 Vision model access
- Provides clear error messages for troubleshooting

## Future Improvements
- Support for additional file formats
- Batch image processing
- OCR pre-processing for better text recognition
- Multi-language support
