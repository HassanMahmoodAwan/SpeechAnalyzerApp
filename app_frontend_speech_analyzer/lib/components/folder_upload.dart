// ignore_for_file: prefer_const_constructors, prefer_interpolation_to_compose_strings, avoid_print

import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:http/http.dart' as http;
import 'dart:async';

class FolderUploadComponent extends StatefulWidget {
  final ValueChanged<Map<String, dynamic>> onUploadStatusChanged;
  const FolderUploadComponent({
    super.key,
    required this.onUploadStatusChanged,
  });

  @override
  State<FolderUploadComponent> createState() => _FolderUploadState();
}

class _FolderUploadState extends State<FolderUploadComponent> {
  // Variables
  String? fileName;
  String? errorMessage;
  bool isLoading = false;
  PlatformFile? selectedFile;
  String uploadStatus = '';

  // Function to pick and upload zip file
  Future<void> pickAndUploadZipFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['wav', 'mp3', 'flac', 'zip'], // Include all formats
      );

      if (result != null) {
        setState(() {
          selectedFile = result.files.single;
          fileName = selectedFile!.name;
          isLoading = true;
          uploadStatus = "";
        });

        print(fileName);
        if (selectedFile != null) {
          String? fileExtension = fileName?.split('.').last.toLowerCase();

          // Check the file extension and run different logic
          if (['wav', 'mp3', 'flac'].contains(fileExtension)) {
            uploadAudioFile(selectedFile!);
          } else if (fileExtension == 'zip') {
            uploadZipFile(selectedFile!);
          } else {
            setState(() {
              fileName = null;
              errorMessage =
                  'Invalid file format. Please upload an audio or zip file.';
              isLoading = false;
            });
          }
        } else {
          setState(() {
            errorMessage = "No file Selected";
          });
          print("No file is Selected");
        }
      } else {
        print("No file Selected");
      }
    } catch (e) {
      print("Error picking file: $e");
      setState(() {
        errorMessage = "Error picking File";
      });
    }
  }

  // Function to upload the zip file to the backend
  Future<void> uploadAudioFile(PlatformFile file) async {
    var uri = Uri.parse('http://localhost:8000/api/upload-audio');
    var request = http.MultipartRequest('POST', uri);

    if (file.bytes == null) return;

    setState(() {
      errorMessage = null;
      isLoading = true;
    });

    if (file.bytes != null) {
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          file.bytes!,
          filename: file.name,
        ),
      );
    }

    var Response = await request.send();

    if (Response.statusCode == 200) {
      print("Hello");
      var responseBody = await Response.stream.bytesToString();
      print(responseBody);

      setState(() {
        final Map<String, dynamic> jsonResponse =
            json.decode(responseBody) as Map<String, dynamic>;
        jsonResponse['fileNamesList'] =
            (jsonResponse['fileNamesList'] as List).cast<String>();
        widget.onUploadStatusChanged({'status': true, 'Data': jsonResponse});
        isLoading = false;
      });
    } else {
      setState(() {
        isLoading = false;
      });
    }
  }

  // upload zip-ile to backend
  Future<void> uploadZipFile(PlatformFile file) async {
    var uri = Uri.parse('http://localhost:8000/api/upload-multiple-files');
    var request = http.MultipartRequest('POST', uri);

    if (file.bytes != null) {
      request.files.add(
        http.MultipartFile.fromBytes(
          'file',
          file.bytes!,
          filename: file.name,
        ),
      );
    }

    var Response = await request.send();
    setState(() {
      isLoading = true;
    });

    if (Response.statusCode == 200) {
      var responseBody = await Response.stream.bytesToString();
      print(responseBody);

      setState(() {
        final Map<String, dynamic> jsonResponse =
            json.decode(responseBody) as Map<String, dynamic>;
        jsonResponse['fileNamesList'] =
            (jsonResponse['fileNamesList'] as List).cast<String>();
        widget.onUploadStatusChanged({'status': true, 'Data': jsonResponse});
        isLoading = false;
      });
    } else {
      setState(() {
        isLoading = false;
        errorMessage = "File Upload failed";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double threshold = 900;
    return Center(
      child: SizedBox(
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4.0, vertical: 6),
            child: Text(' Upload Zip Folder or (MP3, WAV) file',
                style: TextStyle(
                    fontSize: 12,
                    color: const Color.fromARGB(255, 117, 117, 117))),
          ),
          Container(
            width: screenWidth > threshold
                ? MediaQuery.of(context).size.width * 0.43
                : MediaQuery.of(context).size.width * 0.65,
            padding: EdgeInsets.symmetric(vertical: 25.0, horizontal: 17),
            decoration: BoxDecoration(
              color: const Color.fromARGB(255, 239, 239, 239),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      fileName ?? 'No file uploaded',
                      style: TextStyle(fontSize: 16),
                    ),
                    ElevatedButton(
                      onPressed: pickAndUploadZipFile,
                      style: ElevatedButton.styleFrom(
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8)),
                        foregroundColor: Colors.white,
                        backgroundColor: const Color.fromARGB(
                            255, 4, 39, 91), // Button color
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: const [
                          Icon(Icons.upload, size: 17),
                          SizedBox(width: 5),
                          Text('Upload Folder'),
                        ],
                      ),
                    ),
                  ],
                ),
                if (errorMessage != null)
                  Padding(
                    padding: const EdgeInsets.only(top: 10.0),
                    child: Text(
                      errorMessage!,
                      style: TextStyle(color: Colors.red, fontSize: 14),
                      textAlign: TextAlign.center,
                    ),
                  ),
              ],
            ),
          ),
          SizedBox(height: 20),
          if (isLoading) CircularProgressIndicator(),
          SizedBox(height: 20),
        ]),
      ),
    );
  }
}
