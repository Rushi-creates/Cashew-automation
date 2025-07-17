package com.example.share_gpay_ss

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.annotation.NonNull
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.example.share_gpay_ss/share"
    private var methodChannel: MethodChannel? = null

    override fun configureFlutterEngine(@NonNull flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        methodChannel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
        methodChannel?.setMethodCallHandler { call, result ->
            when (call.method) {
                "getSharedImages" -> {
                    val sharedImages = getSharedImages()
                    result.success(sharedImages)
                }
                else -> {
                    result.notImplemented()
                }
            }
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        handleIntent(intent)
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        handleIntent(intent)
    }

    override fun onResume() {
        super.onResume()
        // No intent parameter here; use the activity's intent
        handleIntent(intent)
    }

    private fun handleIntent(intent: Intent?) {
        if (intent == null) return

        val action = intent.action
        val type = intent.type

        if (Intent.ACTION_SEND == action && type != null && type.startsWith("image/")) {
            val imageUri = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
            if (imageUri != null) {
                val imagePath = getRealPathFromURI(imageUri)
                methodChannel?.invokeMethod("onImageShared", imagePath)
            }
        } else if (Intent.ACTION_SEND_MULTIPLE == action && type != null && type.startsWith("image/")) {
            val imageUris = intent.getParcelableArrayListExtra<Uri>(Intent.EXTRA_STREAM)
            if (imageUris != null) {
                val imagePaths = imageUris.mapNotNull { uri -> getRealPathFromURI(uri) }
                methodChannel?.invokeMethod("onMultipleImagesShared", imagePaths)
            }
        }
    }

    private fun getSharedImages(): List<String> {
        val sharedImages = mutableListOf<String>()
        val intent = intent
        val action = intent?.action
        val type = intent?.type

        if (Intent.ACTION_SEND == action && type != null && type.startsWith("image/")) {
            val imageUri = intent.getParcelableExtra<Uri>(Intent.EXTRA_STREAM)
            if (imageUri != null) {
                val imagePath = getRealPathFromURI(imageUri)
                if (imagePath != null) {
                    sharedImages.add(imagePath)
                }
            }
        } else if (Intent.ACTION_SEND_MULTIPLE == action && type != null && type.startsWith("image/")) {
            val imageUris = intent.getParcelableArrayListExtra<Uri>(Intent.EXTRA_STREAM)
            if (imageUris != null) {
                for (uri in imageUris) {
                    val imagePath = getRealPathFromURI(uri)
                    if (imagePath != null) {
                        sharedImages.add(imagePath)
                    }
                }
            }
        }
        return sharedImages
    }

    private fun getRealPathFromURI(uri: Uri): String? {
        return try {
            val cursor = contentResolver.query(uri, null, null, null, null)
            if (cursor != null) {
                cursor.use {
                    if (it.moveToFirst()) {
                        val columnIndex = it.getColumnIndex(android.provider.MediaStore.Images.Media.DATA)
                        if (columnIndex != -1) {
                            it.getString(columnIndex)
                        } else {
                            uri.path
                        }
                    } else {
                        uri.path
                    }
                }
            } else {
                uri.path
            }
        } catch (e: Exception) {
            uri.path
        }
    }
}
