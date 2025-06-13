# ImageFX Generator

A web application for generating images using the ImageFX API. This application provides a user-friendly interface and a RESTful API for generating images with various customization options.

## Features

- Generate images using text prompts
- Customize image generation with parameters like count, aspect ratio, and seed
- Random prompt generation for creative inspiration
- RESTful API for programmatic access
- Settings management for API authentication
- Modern and responsive web interface
- Beautiful lightbox image preview with navigation
- Image download functionality
- Prompt history tracking
- Keyboard navigation support
- Responsive grid layout for generated images

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/imagefx-generator.git
cd imagefx-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your ImageFX auth token:
```
IMAGEFX_AUTH_TOKEN=your_auth_token_here
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Configure your settings:
   - Go to the Settings page
   - Enter your ImageFX auth token
   - Set your preferred default number of images

4. Generate images:
   - Enter a prompt in the text area
   - Choose the number of images to generate
   - Select the aspect ratio
   - Click "Generate"

5. View and interact with generated images:
   - Click any image to open it in the lightbox
   - Use arrow keys or navigation buttons to browse images
   - Download images using the download button
   - View your prompt history for quick reuse

## API Documentation

The application provides a RESTful API for programmatic access. Visit the API Documentation page at `/api` for detailed information about available endpoints and usage examples.

### Available Endpoints

- `GET /api/generate` - Generate images
- `POST /api/random-prompt` - Generate a random prompt
- `GET /api/settings` - Get current settings
- `POST /api/settings` - Update settings

## Development

### Project Structure

```
imagefx-generator/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── settings.json      # Application settings
└── templates/         # HTML templates
    ├── base.html      # Base template
    ├── index.html     # Main page
    ├── settings.html  # Settings page
    ├── api.html       # API documentation
    └── api_test.html  # API test tool
```

### Running Tests

The application includes an API test tool at `/api/test` for testing endpoints directly from the browser.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Icons
- [ImageFX](https://labs.google/) - Image generation API 