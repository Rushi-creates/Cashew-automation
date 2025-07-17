# GPay Screenshot Share App

A Flutter app that allows users to share GPay screenshots directly to the app without opening it, and automatically uploads the images to a backend server.

## Features

- **Direct Share Integration**: Share screenshots from GPay directly to this app
- **Automatic Upload**: Images are automatically uploaded to the backend server
- **Multiple Image Support**: Handle both single and multiple image shares
- **Modern UI**: Clean and intuitive user interface
- **Real-time Feedback**: Toast notifications for upload status

## How to Use

1. **Install the app** on your Android device
2. **Open GPay** and navigate to the screen you want to capture
3. **Take a screenshot** using your device's screenshot function
4. **Tap the share button** that appears after taking the screenshot
5. **Select this app** from the share menu
6. **Images are automatically uploaded** to the backend server

## Setup

### Backend Configuration

1. Update the backend URL in `lib/services/backend_service.dart`:
   ```dart
   static const String baseUrl = 'https://your-backend-url.com/api';
   ```

2. Ensure your backend has the following endpoints:
   - `POST /api/upload-image` - for single image upload
   - `POST /api/upload-multiple-images` - for multiple image upload

### Backend API Endpoints

#### Single Image Upload
```
POST /api/upload-image
Content-Type: multipart/form-data

Parameters:
- image: File (the image file)
```

#### Multiple Images Upload
```
POST /api/upload-multiple-images
Content-Type: multipart/form-data

Parameters:
- images: File[] (array of image files)
```

## Technical Details

### Android Share Intent Integration

The app uses Android's share intent system to receive images from other apps:

- **Intent Filters**: Configured in `android/app/src/main/AndroidManifest.xml`
- **Platform Channel**: Communication between Flutter and native Android code
- **File Handling**: Processes shared image URIs and converts them to file paths

### Permissions

The app requests the following permissions:
- `INTERNET` - for backend communication
- `READ_EXTERNAL_STORAGE` - for accessing shared images
- `WRITE_EXTERNAL_STORAGE` - for file operations
- `READ_MEDIA_IMAGES` - for accessing images on newer Android versions

### Architecture

- **ShareService**: Handles platform channel communication
- **BackendService**: Manages HTTP requests to the backend
- **MainActivity**: Android native code for intent handling

## Development

### Prerequisites

- Flutter SDK
- Android Studio / VS Code
- Android device or emulator

### Running the App

1. Clone the repository
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Update the backend URL in `lib/services/backend_service.dart`
4. Run the app:
   ```bash
   flutter run
   ```

### Building for Production

```bash
flutter build apk --release
```

## Troubleshooting

### Common Issues

1. **Images not being received**: Check that the app has the necessary permissions
2. **Upload failures**: Verify the backend URL and network connectivity
3. **App not appearing in share menu**: Ensure the app is properly installed and the intent filters are configured

### Debug Mode

Enable debug logging by checking the console output for:
- Shared image paths
- Upload status messages
- Error details

## License

This project is licensed under the MIT License.
# Cashew-automation
