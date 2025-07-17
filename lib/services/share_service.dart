import 'package:flutter/services.dart';
import 'package:share_gpay_ss/services/backend_service.dart';

class ShareService {
  static const MethodChannel _channel = MethodChannel('com.example.share_gpay_ss/share');
  
  /// Initialize the share service and set up method call handlers
  static void initialize() {
    _channel.setMethodCallHandler((call) async {
      switch (call.method) {
        case 'onImageShared':
          final String? imagePath = call.arguments as String?;
          if (imagePath != null) {
            await _handleSingleImageShared(imagePath);
          }
          break;
        case 'onMultipleImagesShared':
          final List<dynamic> imagePaths = call.arguments as List<dynamic>;
          final List<String> paths = imagePaths.cast<String>();
          await _handleMultipleImagesShared(paths);
          break;
      }
    });
  }

  /// Get any shared images that were passed to the app
  static Future<List<String>> getSharedImages() async {
    try {
      final List<dynamic> result = await _channel.invokeMethod('getSharedImages');
      return result.cast<String>();
    } on PlatformException catch (e) {
      print('Error getting shared images: $e');
      return [];
    }
  }

  /// Handle a single shared image
  static Future<void> _handleSingleImageShared(String imagePath) async {
    print('Received single image: $imagePath');
    await BackendService.uploadImage(imagePath);
  }

  /// Handle multiple shared images
  static Future<void> _handleMultipleImagesShared(List<String> imagePaths) async {
    print('Received multiple images: $imagePaths');
    await BackendService.uploadMultipleImages(imagePaths);
  }
} 