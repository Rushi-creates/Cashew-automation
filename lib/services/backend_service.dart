import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:fluttertoast/fluttertoast.dart';

class BackendService {
  // Replace with your actual backend URL
  static const String baseUrl = 'https://your-backend-url.com/api';
  
  /// Upload a single image to the backend
  static Future<bool> uploadImage(String imagePath) async {
    try {
      final file = File(imagePath);
      if (!await file.exists()) {
        print('File does not exist: $imagePath');
        return false;
      }

      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload-image'),
      );

      request.files.add(
        await http.MultipartFile.fromPath(
          'image',
          imagePath,
        ),
      );

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        Fluttertoast.showToast(
          msg: 'Image uploaded successfully!',
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.BOTTOM,
        );
        return true;
      } else {
        print('Upload failed: ${response.statusCode} - $responseBody');
        Fluttertoast.showToast(
          msg: 'Upload failed: ${response.statusCode}',
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.BOTTOM,
        );
        return false;
      }
    } catch (e) {
      print('Error uploading image: $e');
      Fluttertoast.showToast(
        msg: 'Error uploading image: $e',
        toastLength: Toast.LENGTH_SHORT,
        gravity: ToastGravity.BOTTOM,
      );
      return false;
    }
  }

  /// Upload multiple images to the backend
  static Future<bool> uploadMultipleImages(List<String> imagePaths) async {
    try {
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/upload-multiple-images'),
      );

      for (String imagePath in imagePaths) {
        final file = File(imagePath);
        if (await file.exists()) {
          request.files.add(
            await http.MultipartFile.fromPath(
              'images',
              imagePath,
            ),
          );
        }
      }

      final response = await request.send();
      final responseBody = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        Fluttertoast.showToast(
          msg: '${imagePaths.length} images uploaded successfully!',
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.BOTTOM,
        );
        return true;
      } else {
        print('Upload failed: ${response.statusCode} - $responseBody');
        Fluttertoast.showToast(
          msg: 'Upload failed: ${response.statusCode}',
          toastLength: Toast.LENGTH_SHORT,
          gravity: ToastGravity.BOTTOM,
        );
        return false;
      }
    } catch (e) {
      print('Error uploading images: $e');
      Fluttertoast.showToast(
        msg: 'Error uploading images: $e',
        toastLength: Toast.LENGTH_SHORT,
        gravity: ToastGravity.BOTTOM,
      );
      return false;
    }
  }
} 