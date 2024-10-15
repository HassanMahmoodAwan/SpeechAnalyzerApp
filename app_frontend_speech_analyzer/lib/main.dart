// ignore_for_file: prefer_const_constructors, prefer_final_fields, unused_element, avoid_print, no_leading_underscores_for_local_identifiers, prefer_const_literals_to_create_immutables, use_key_in_widget_constructors, library_private_types_in_public_api, deprecated_member_use

import 'package:app_frontend_speech_analyzer/pages/analysis.dart';
import 'package:app_frontend_speech_analyzer/pages/file_upload.dart';
import 'package:app_frontend_speech_analyzer/pages/test.dart';
import 'package:app_frontend_speech_analyzer/utils/theme.dart';
import 'package:flutter/material.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: customTheme,
      debugShowCheckedModeBanner: false,
      home: HomePage(),
      routes: {
        '/fileupload': (context) => FileUploadPage(),
        '/test': (context) => Testing(),
      },
      onGenerateRoute: (settings) {
        if (settings.name!.startsWith('/analysis')) {
          Uri uri = Uri.parse(settings.name!);
          final index = uri.queryParameters['index'];
          return MaterialPageRoute(
            builder: (context) => SpeechDetail(index: index),
          );
        }
        return null;
      },
    );
  }
}
