// ignore_for_file: prefer_const_constructors, prefer_final_fields, unused_element, avoid_print, no_leading_underscores_for_local_identifiers, prefer_const_literals_to_create_immutables, use_key_in_widget_constructors, library_private_types_in_public_api

import 'package:app_frontend_speech_analyzer/components/app_bar.dart';
import 'package:app_frontend_speech_analyzer/pages/analysis.dart';
import 'package:app_frontend_speech_analyzer/pages/file_upload.dart';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class Testing extends StatelessWidget {
  const Testing({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        debugShowCheckedModeBanner: false,
        home: TestPage(),
        title: "ABL Muawin",
        routes: {
          '/fileupload': (context) => FileUploadPage(),
          // '/test': (context) => Testing(),
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
        });
  }
}

class TestPage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<TestPage> {
  bool _isLoading = true;
  List<dynamic> _data = [];
  List<dynamic> _filteredData = [];
  String _searchQuery = "";

  String analysisFormat(var input) {
    String resultString = "";
    input = input.replaceAll("'", "\"");
    input = input.replaceAll("\n", "");
    input = input.replaceAll("json", "");
    input = input.replaceAll("```", "");
    var inputJson = jsonDecode(input);

    inputJson.forEach((key, value) {
      resultString += '$key: $value\n';
    });

    return resultString;
  }

  void showCustomToast(BuildContext context) {
    OverlayEntry overlayEntry = OverlayEntry(
      builder: (context) => Positioned(
        top: 50.0,
        right: 20.0,
        child: Material(
          color: Colors.transparent,
          child: Container(
            padding: EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(8.0),
              boxShadow: [
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
                Icon(Icons.check_circle, color: Colors.green),
                SizedBox(width: 12.0),
                Text(
                  'File Deleted Successfully',
                  style: TextStyle(color: Colors.black),
                ),
              ],
            ),
          ),
        ),
      ),
    );
    Overlay.of(context).insert(overlayEntry);

    Future.delayed(Duration(seconds: 2), () {
      overlayEntry.remove();
    });
  }

  // Fetching all Data
  Future<void> _fetchAllRecords() async {
    try {
      final response =
          await http.get(Uri.parse('http://localhost:8000/api/all-records'));

      if (response.statusCode == 200) {
        setState(() {
          final List<dynamic> jsonResponse =
              json.decode(utf8.decode(response.bodyBytes));
          _data = jsonResponse;
          _isLoading = false;
        });
      } else {
        setState(() {
          print("No data fetched");
          _isLoading = false;
        });
      }
    } catch (e) {
      print("Error fetching data: $e");
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _deleteRecord(int id) async {
    try {
      print(id);
      final response = await http.delete(
          Uri.parse('http://localhost:8000/api/delete-record-by-id/$id'));
      _fetchAllRecords();

      // ignore: use_build_context_synchronously
      showCustomToast(context);

      if (response.statusCode == 200) {
        print('Record deleted successfully');
      } else {
        print('Failed to delete record');
      }
    } catch (e) {
      print('Error deleting record: $e');
    }
  }

  // Function to filter the data based on the search query
  void searchTableResults(String keyword) {
    if (keyword.isEmpty) {
      setState(() {
        _filteredData = _data;
      });
    } else {
      setState(() {
        _filteredData = _data.where((record) {
          return record['id']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase()) ||
              record['filename']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase()) ||
              record['sentiment']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase()) ||
              record['emotion']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase()) ||
              record['category']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase()) ||
              record['file_duration']
                  .toString()
                  .toLowerCase()
                  .contains(keyword.toLowerCase());
        }).toList();
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _fetchAllRecords();
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _fetchAllRecords();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
          preferredSize: Size.fromHeight(70),
          child: CustomAppBar(title: "", userMsg: "Welcome!  Hassan  Mahmood")),

      // ======Body========
      body: Container(
        color: const Color.fromARGB(255, 251, 253, 255),
        child: ListView(
          padding: EdgeInsets.only(bottom: 50),
          children: [
            SizedBox(height: 70),

            if (_isLoading && _data.isNotEmpty)
              Center(child: CircularProgressIndicator())
            else
              Align(
                alignment: Alignment.center,
                child: SizedBox(
                  width: MediaQuery.of(context).size.width * 0.88,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "Available Call Records Records",
                        style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Row(
                        children: [
                          ElevatedButton(
                            onPressed: () {
                              Navigator.pushNamed(context, '/fileupload');
                            },
                            style: ElevatedButton.styleFrom(
                                padding: EdgeInsets.symmetric(horizontal: 13),
                                backgroundColor:
                                    const Color.fromARGB(255, 4, 39, 91),
                                foregroundColor: Colors.white,
                                shape: RoundedRectangleBorder(
                                    borderRadius: BorderRadius.circular(6))),
                            child: Row(
                              children: [
                                Icon(
                                  Icons.add,
                                  size: 16,
                                  color: Colors.white,
                                ),
                                SizedBox(width: 2),
                                Text("Upload Folder"),
                              ],
                            ),
                          ),
                          SizedBox(width: 7),

                          // ==== Search Bar ====
                          SizedBox(
                            width: 190,
                            height: 32,
                            child: TextField(
                                onChanged: (value) {
                                  setState(() {
                                    _searchQuery = value;

                                    searchTableResults(
                                        _searchQuery); // Call the search function
                                  });
                                },
                                decoration: InputDecoration(
                                  hintText: " Search Record...",
                                  hintStyle: TextStyle(
                                      color: Colors.grey, fontSize: 13),
                                  prefixIcon: Icon(Icons.search),
                                  border: OutlineInputBorder(
                                      borderRadius: BorderRadius.circular(6)),
                                  contentPadding:
                                      EdgeInsets.symmetric(vertical: 3),
                                )),
                          ),
                          // ====================
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            SizedBox(height: 20),

            // Table to show records
            Align(
              alignment: Alignment.center,
              child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(5),
                    color: const Color.fromARGB(255, 247, 247, 247),
                  ),
                  width: MediaQuery.of(context).size.width * 0.89,
                  child: SingleChildScrollView(
                    scrollDirection: Axis.horizontal,
                    child: DataTable(
                      headingRowColor: WidgetStateProperty.all(
                          const Color.fromARGB(255, 4, 39, 91)),
                      columnSpacing: 0, // Adjust the spacing between columns
                      // dataRowHeight: 60.0,

                      dataRowMaxHeight: 90.0, // Adjust the height of each row
                      columns: [
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth: MediaQuery.of(context).size.width *
                                    0.05), // Set max width for content
                            child: Text("File ID",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.12),
                            child: Text("File Name",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.10),
                            child: Text("Creation Time",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.10),
                            child: Text("Time Duration",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.14),
                            child: Text("Sentiment Analysis",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.14),
                            child: Text("Emotion Analysis",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.12),
                            child: Text("Category",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                        DataColumn(
                          label: Container(
                            constraints: BoxConstraints(
                                minWidth:
                                    MediaQuery.of(context).size.width * 0.09),
                            child: Text("Show Analysis",
                                style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 15,
                                    fontWeight: FontWeight.bold)),
                          ),
                        ),
                      ],
                      rows: (_searchQuery.isEmpty ? _data : _filteredData)
                          .map((record) {
                        return DataRow(
                          cells: [
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 80),
                                child: Text(
                                  "0${record['id'].toString()}",
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                padding: EdgeInsets.fromLTRB(0, 0, 20, 0),
                                constraints: BoxConstraints(maxWidth: 128),
                                child: Text(
                                  record['filename'],
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 100),
                                child: Text(
                                  "${record['file_duration'].split(" ").length >= 2 ? record['file_duration'].split(" ")[1] : " "}\n${record['file_duration'].split(" ").length >= 3 ? record['file_duration'].split(" ")[2] : " "}",
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 100),
                                child: Text(
                                  "${record['file_duration'].split(" ")[0]} mins",
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 175),
                                child: Text(
                                  analysisFormat(record['sentiment'].toString())
                                      .trim(),
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 175),
                                child: Text(
                                  analysisFormat(record['emotion'].toString())
                                      .trim(),
                                ),
                              ),
                            ),
                            DataCell(
                              Container(
                                constraints: BoxConstraints(maxWidth: 170),
                                child: Text(
                                  record['category'].toString().trim(),
                                ),
                              ),
                            ),
                            DataCell(
                              GestureDetector(
                                onTap: () {
                                  Navigator.pushNamed(context,
                                      '/analysis?index=${record['id']}');
                                },
                                child: MouseRegion(
                                  cursor: SystemMouseCursors.click,
                                  child: Container(
                                    constraints: BoxConstraints(
                                      maxWidth: 140,
                                    ),
                                    alignment: Alignment.centerLeft,
                                    child: Text(
                                      "Show Analysis",
                                      style: TextStyle(color: Colors.blue[800]),
                                    ),
                                  ),
                                ),
                              ),
                            ),
                          ],
                        );
                      }).toList(),
                    ),
                  )),
            ),
          ],
        ),
      ),
    );
  }
}
