import 'package:app_frontend_speech_analyzer/components/app_bar.dart';
import 'package:app_frontend_speech_analyzer/components/folder_upload.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class FileUploadPage extends StatefulWidget {
  const FileUploadPage({super.key});

  @override
  State<FileUploadPage> createState() => _FileUploadPageState();
}

class _FileUploadPageState extends State<FileUploadPage> {
  bool _isUploaded = false;
  bool _isLoading = false;
  int counter = 0;
  int length = 0;
  bool loadingDone = false;
  String filName = '';
  String? errorMsg;

  void showCustomToast(BuildContext context, String msg, Icon showIcon) {
    OverlayEntry overlayEntry = OverlayEntry(
      builder: (context) => Positioned(
        top: 50.0,
        right: 20.0,
        child: Material(
          color: Colors.transparent,
          child: Container(
            padding:
                const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(8.0),
              boxShadow: const [
                BoxShadow(
                  color: Colors.black26,
                  blurRadius: 10.0,
                  offset: Offset(2, 2),
                ),
              ],
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                showIcon,
                const SizedBox(width: 12.0),
                Text(
                  msg,
                  style: const TextStyle(color: Colors.black),
                ),
              ],
            ),
          ),
        ),
      ),
    );

    Overlay.of(context).insert(overlayEntry);

    Future.delayed(const Duration(seconds: 3), () {
      overlayEntry.remove();
    });
  }

  void _handleUploadStatus(Map<String, dynamic> response) {
    setState(() {
      _isUploaded = response['status'];
      if (_isUploaded) {
        setState(() {
          length = response['Data']['fileNamesList'].length;
        });
        _fetchData(response['Data']['fileNamesList']);
      }
    });
  }

  Future<void> _fetchData(List<String> fileNamesList) async {
    try {
      setState(() {
        counter = 0;
      });
      var uri = Uri.parse('http://localhost:8000/api/upload-and-analyze');
      for (var fileName in fileNamesList) {
        setState(() {
          filName = fileName;
          _isLoading = true;
          counter++;
          errorMsg = null;
        });

        final response = await http.post(uri,
            body: {'InputfileName': fileName},
            headers: {'Content-Type': 'application/x-www-form-urlencoded'});
        if (response.statusCode == 200) {
          if (counter == length) {
            setState(() {
              filName = "All files processed";
              _isLoading = false;
              loadingDone = true;
              showCustomToast(context, 'All Files Processed Successfully',
                  const Icon(Icons.check_circle, color: Colors.green));
            });
            break;
          }
        } else {
          setState(() {
            _isLoading = false;
            errorMsg =
                "Error fetching data: (server Error: ${response.statusCode})";
            showCustomToast(context, 'Error Fetching Data.',
                const Icon(Icons.error, color: Colors.red));
          });
        }
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
        errorMsg = "Error Fetching Data. (Server Error)";
        showCustomToast(context, 'Error Fetching Data. (Server Error)',
            const Icon(Icons.error, color: Colors.red));
      });
    }
  }

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double threshold = 900;
    return Scaffold(
      appBar: const PreferredSize(
          preferredSize: Size.fromHeight(70),
          child: CustomAppBar(title: "", userMsg: '')),
      body: Container(
        color: const Color.fromARGB(255, 251, 253, 255),
        child: ListView(
          padding: const EdgeInsets.only(bottom: 50),
          children: [
            const SizedBox(height: 70), // Add some spacing
            // ==== File Upload ======
            FolderUploadComponent(onUploadStatusChanged: _handleUploadStatus),
            const SizedBox(height: 20),
            // ==== Progress Bar =====

            Align(
              alignment: Alignment.center,
              child: Column(
                children: [
                  // Error Message
                  errorMsg != null
                      ? Text(errorMsg!,
                          style:
                              const TextStyle(fontSize: 15, color: Colors.red))
                      : const Text(""),

                  // ===== Progress Bar ======
                  Container(
                      width: screenWidth > threshold
                          ? MediaQuery.of(context).size.width * 0.73
                          : MediaQuery.of(context).size.width * 0.95,
                      decoration: BoxDecoration(
                        color: Colors.blue[800],
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Padding(
                        padding: const EdgeInsets.all(25.0),
                        child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              RichText(
                                  text: TextSpan(children: [
                                if (filName.isNotEmpty)
                                  TextSpan(
                                      text: filName.toString(),
                                      style: const TextStyle(
                                          color: Colors.white, fontSize: 16))
                                else
                                  const TextSpan(
                                      text: "No File in Progress",
                                      style: TextStyle(
                                          color: Colors.white, fontSize: 16)),

                                const WidgetSpan(
                                    child: SizedBox(
                                  width: 14,
                                )),

                                //  ===== File Counter =====
                                if (counter > 0)
                                  TextSpan(
                                      text: "$counter / $length",
                                      style: const TextStyle(
                                          color: Colors.white, fontSize: 15))
                                else
                                  const TextSpan(
                                      text: "",
                                      style: TextStyle(
                                          color: Colors.white, fontSize: 15)),
                              ])),
                              if (_isLoading == true)
                                const Center(
                                    child: CircularProgressIndicator(
                                  color: Colors.white,
                                  strokeWidth: 1.8,
                                ))
                              else if (loadingDone)
                                const Row(
                                  children: [
                                    Icon(
                                      Icons.check_circle,
                                      color: Colors.green,
                                    ),
                                    SizedBox(
                                        width:
                                            8), // Space between the icon and text
                                    Text(
                                      'Done',
                                      style: TextStyle(
                                        fontSize: 17,
                                        color: Colors.white,
                                      ),
                                    ),
                                  ],
                                )
                              else
                                const Text(""),
                            ]),
                      )),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
