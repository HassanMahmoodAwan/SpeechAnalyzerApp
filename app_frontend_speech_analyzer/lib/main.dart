// ignore_for_file: prefer_const_constructors, prefer_final_fields, unused_element, avoid_print, no_leading_underscores_for_local_identifiers, prefer_const_literals_to_create_immutables, use_key_in_widget_constructors, library_private_types_in_public_api, deprecated_member_use

import 'package:app_frontend_speech_analyzer/components/app_bar.dart';
import 'package:app_frontend_speech_analyzer/pages/analysis.dart';
import 'package:app_frontend_speech_analyzer/pages/file_upload.dart';
import 'package:app_frontend_speech_analyzer/pages/test.dart';
import 'package:app_frontend_speech_analyzer/utils/theme.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool _isLoading = true;
  List<dynamic> _data = [];
  List<dynamic> _filteredData = [];
  String _searchQuery = "";
  int _rowsPerPage = PaginatedDataTable.defaultRowsPerPage;

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
          _filteredData = _data;
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

  @override
  void initState() {
    super.initState();
    _fetchAllRecords();
  }

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double threshold = 900;
    return Scaffold(
      appBar: PreferredSize(
          preferredSize: Size.fromHeight(70),
          child: CustomAppBar(title: "", userMsg: "Welcome!  Hassan  Mahmood")),
      body: Container(
        color: const Color.fromARGB(255, 251, 253, 255),
        child: ListView(
          padding: EdgeInsets.only(bottom: 50),
          children: [
            SizedBox(height: 45),
            if (_isLoading)
              Center(child: CircularProgressIndicator())
            else
              Align(
                alignment: Alignment.center,
                child: SizedBox(
                  width: screenWidth > threshold
                      ? MediaQuery.of(context).size.width * 0.89
                      : MediaQuery.of(context).size.width * 0.96,

                  // ======== Data Table ========
                  child: DataTableTheme(
                    data: DataTableThemeData(
                      dataRowColor: WidgetStatePropertyAll(
                          const Color.fromARGB(255, 247, 247, 247)),
                    ),
                    child: PaginatedDataTable(
                      // ===== Heading + Search Query ================
                      header: Padding(
                        padding: EdgeInsets.zero,
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              "Available Call Records",
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
                                      padding:
                                          EdgeInsets.symmetric(horizontal: 13),
                                      iconColor: Colors.white,
                                      backgroundColor:
                                          const Color.fromARGB(255, 4, 39, 91),
                                      foregroundColor: Colors.white,
                                      shape: RoundedRectangleBorder(
                                          borderRadius:
                                              BorderRadius.circular(6))),
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
                                  width: 177,
                                  height: 32,
                                  child: TextField(
                                      onChanged: (value) {
                                        setState(() {
                                          _searchQuery = value;
                                          searchTableResults(_searchQuery);
                                        });
                                      },
                                      decoration: InputDecoration(
                                        hintText: " Search Record...",
                                        hintStyle: TextStyle(
                                            color: Colors.grey, fontSize: 13),
                                        prefixIcon: Icon(Icons.search),
                                        border: OutlineInputBorder(
                                            borderRadius:
                                                BorderRadius.circular(6)),
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
                      // =================================

                      // data table
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
                      source: _DataTableSource(_filteredData, context),
                      actions: [],
                      rowsPerPage: _rowsPerPage,
                      onRowsPerPageChanged: (value) {
                        setState(() {
                          _rowsPerPage = value ?? 10;
                        });
                      },
                      columnSpacing: 0,
                      dataRowHeight: 100,
                      showEmptyRows: false,
                      arrowHeadColor: Colors.blue[700],
                      headingRowColor: MaterialStateProperty.all(
                          Color.fromARGB(255, 4, 39, 91)),
                    ),
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

class _DataTableSource extends DataTableSource {
  final List<dynamic> _data;
  final BuildContext context;

  _DataTableSource(this._data, this.context);

  @override
  DataRow getRow(int index) {
    final record = _data[index];

    // Make sure to handle potential null values for each field
    return DataRow(
      cells: [
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 80),
            child: Text("0${record['id'].toString()}"),
          ),
        ),
        DataCell(
          Container(
            padding: EdgeInsets.fromLTRB(0, 0, 20, 0),
            constraints: BoxConstraints(maxWidth: 128),
            child: Text(record['filename']),
          ),
        ),
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 100),
            child: Text(
                "${record['file_duration'].split(" ").length >= 2 ? record['file_duration'].split(" ")[1] : " "}\n${record['file_duration'].split(" ").length >= 3 ? record['file_duration'].split(" ")[2] : " "}"),
          ),
        ),
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 100),
            child: Text("${record['file_duration'].split(" ")[0]} mins"),
          ),
        ),
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 175),
            child: Text(analysisFormat(record['sentiment'].toString()).trim()),
          ),
        ),
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 175),
            child: Text(analysisFormat(record['emotion'].toString()).trim()),
          ),
        ),
        DataCell(
          Container(
            constraints: BoxConstraints(maxWidth: 170),
            child: Text(record['category'].toString().trim()),
          ),
        ),
        DataCell(
          GestureDetector(
            onTap: () {
              Navigator.pushNamed(context, '/analysis?index=${record['id']}');
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
  }

  @override
  bool get isRowCountApproximate => false;

  @override
  int get rowCount => _data.length;

  @override
  int get selectedRowCount => 0;
}

// Helper function to format analysis results
String analysisFormat(var input) {
  if (input == null || input.isEmpty) {
    return "No data available"; // Handle null or empty input
  }

  String resultString = "";
  input = input.replaceAll("'", "\"");
  input = input.replaceAll("\n", "");
  input = input.replaceAll("json", "");
  input = input.replaceAll("```", "");

  try {
    var inputJson = jsonDecode(input);
    inputJson.forEach((key, value) {
      resultString += '$key: $value\n';
    });
  } catch (e) {
    print("Error parsing JSON: $e");
    resultString = "Error parsing data"; // Handle JSON parsing errors
  }

  return resultString;
}
