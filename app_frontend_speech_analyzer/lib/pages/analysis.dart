// ignore_for_file: prefer_const_constructors, prefer_const_literals_to_create_immutables, avoid_unnecessary_containers, sized_box_for_whitespace, unused_element, avoid_print, prefer_adjacent_string_concatenation

import 'dart:convert';
import 'package:app_frontend_speech_analyzer/components/app_bar.dart';
import 'package:app_frontend_speech_analyzer/components/chart.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as https;

class SpeechDetail extends StatefulWidget {
  final String? index;

  const SpeechDetail({super.key, this.index});

  @override
  State<SpeechDetail> createState() => _SpeechDetailState();
}

class _SpeechDetailState extends State<SpeechDetail> {
  bool _isLoading = true;
  dynamic _data;

  get http => null;

  // ========= Fetching Data from API =========
  Future<void> _fetchAllRecords() async {
    try {
      final response = await https.get(
          Uri.parse('http://localhost:8000/api/record-by-id/${widget.index}'));

      if (response.statusCode == 200) {
        setState(() {
          final dynamic jsonResponse =
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

  @override
  void initState() {
    super.initState();
    _fetchAllRecords();
  }

  Map<String, dynamic> _parseJsonString(String inputString) {
    inputString = inputString.replaceAll("\n", "");
    inputString = inputString.replaceAll("'", "\"");
    inputString = inputString.replaceAll("json", "");
    inputString = inputString.replaceAll("```", "");

    return json.decode(inputString);
  }

  // ==========================================

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double threshold = 1100;
    return Scaffold(
        appBar: PreferredSize(
            preferredSize: Size.fromHeight(70),
            child: CustomAppBar(title: "", userMsg: "")),

        // ===== Body Start =======
        body: Container(
          color: const Color.fromARGB(255, 251, 253, 255),
          child: Center(
            child: Container(
                child: Center(
                    child: ListView(
                        padding: screenWidth > threshold
                            ? EdgeInsets.fromLTRB(100, 0, 100, 12)
                            : EdgeInsets.fromLTRB(20, 0, 20, 12),
                        children: [
                  // ======== Check Loading =======
                  if (_isLoading)
                    Center(child: CircularProgressIndicator())
                  else

                  // ==== Analysis Container ======
                  if (!_isLoading)
                    Column(
                      children: [
                        SizedBox(height: 20),
                        Container(
                          width: MediaQuery.of(context).size.width,
                          child: Wrap(
                            alignment: WrapAlignment.spaceBetween,
                            children: [
                              Container(
                                  padding: EdgeInsets.fromLTRB(0, 12, 0, 0),
                                  height: 185,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      RichText(
                                        text: TextSpan(
                                          children: [
                                            TextSpan(
                                              text: "File ID   :  ",
                                              style: TextStyle(
                                                  fontSize: 15,
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.black),
                                            ),
                                            TextSpan(
                                              text: _data['id'].toString(),
                                              style: TextStyle(
                                                  fontSize: 15,
                                                  color: const Color.fromARGB(
                                                      255, 79, 79, 79)),
                                            ),
                                          ],
                                        ),
                                      ),
                                      SizedBox(height: 25),
                                      RichText(
                                        text: TextSpan(
                                          children: [
                                            TextSpan(
                                              text: "File Name   :  ",
                                              style: TextStyle(
                                                  fontSize: 15,
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.black),
                                            ),
                                            TextSpan(
                                              text: _data['filename'] ?? '',
                                              style: TextStyle(
                                                  fontSize: 15,
                                                  color: const Color.fromARGB(
                                                      255, 79, 79, 79)),
                                            ),
                                          ],
                                        ),
                                      ),
                                      SizedBox(height: 25),
                                      RichText(
                                          text: TextSpan(children: [
                                        TextSpan(
                                          text: "Call Duration : ",
                                          style: TextStyle(
                                            fontSize: 15,
                                            fontWeight: FontWeight.bold,
                                            color: Colors.black,
                                          ),
                                        ),
                                        TextSpan(
                                          text:
                                              " ${_data['file_duration'].split(" ")[0]} mins",
                                          style: TextStyle(
                                            fontSize: 15,
                                            color: const Color.fromARGB(
                                                255, 79, 79, 79),
                                          ),
                                        )
                                      ])),
                                    ],
                                  )),

                              //  ===== Analysis CHARTs ====
                              Container(
                                  padding: EdgeInsets.fromLTRB(0, 10, 0, 0),
                                  width: 570,
                                  decoration: BoxDecoration(
                                    borderRadius: BorderRadius.circular(6),
                                  ),
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.end,
                                    children: [
                                      Container(
                                        padding:
                                            EdgeInsets.fromLTRB(0, 10, 0, 0),
                                        decoration: BoxDecoration(
                                            color: Colors.black12,
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Column(
                                          children: [
                                            Text(
                                              "Sentiment Analysis",
                                              style: TextStyle(
                                                  fontSize: 17,
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.black),
                                            ),
                                            SizedBox(height: 1),
                                            Container(
                                              height: 150,
                                              width: 260,
                                              child: Piechart(
                                                  title: "Sentiment",
                                                  flag: false,
                                                  data: _data["sentiment"]),
                                            ),
                                          ],
                                        ),
                                      ),
                                      SizedBox(width: 30),
                                      Container(
                                        padding:
                                            EdgeInsets.fromLTRB(0, 10, 0, 0),
                                        decoration: BoxDecoration(
                                            color: const Color.fromARGB(
                                                255, 5, 60, 155),
                                            borderRadius:
                                                BorderRadius.circular(10)),
                                        child: Column(
                                          children: [
                                            Text(
                                              "Emotion Analysis",
                                              style: TextStyle(
                                                  fontSize: 17,
                                                  fontWeight: FontWeight.bold,
                                                  color: Colors.white),
                                            ),
                                            SizedBox(height: 1),
                                            Container(
                                              height: 150,
                                              width: 260,
                                              child: Piechart(
                                                  title: "Emotions",
                                                  flag: true,
                                                  data: _data["emotion"]),
                                            ),
                                          ],
                                        ),
                                      ),
                                    ],
                                  )),
                            ],
                          ),
                        ),

                        SizedBox(height: 20),

                        // ====== Summary Container ======
                        Container(
                          padding: screenWidth > threshold
                              ? EdgeInsets.fromLTRB(70, 25, 70, 25)
                              : EdgeInsets.fromLTRB(30, 20, 30, 15),
                          width: MediaQuery.of(context).size.width,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 251, 253, 255),
                            borderRadius: BorderRadius.circular(6),
                            border: Border.all(
                              color: const Color.fromARGB(255, 58, 58, 58),
                              width: 1,
                            ),
                          ),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                "Transcript",
                                style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black),
                              ),
                              SizedBox(height: 7),
                              Container(
                                width: 174,
                                child: ElevatedButton(
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor:
                                          const Color.fromARGB(255, 4, 39, 91),
                                      shape: RoundedRectangleBorder(
                                        borderRadius: BorderRadius.circular(
                                            10), // Set the radius here
                                      ),
                                    ),
                                    onPressed: () {
                                      _showDiaglogBlockTranscript(
                                          context,
                                          "Transcript",
                                          _data['diarized_transcript']);
                                    },
                                    child: Row(
                                      children: [
                                        Text(
                                          "Show Transcript",
                                          style: TextStyle(color: Colors.white),
                                        ),
                                        SizedBox(width: 9),
                                        Icon(
                                          Icons.open_in_full,
                                          color: Colors.white,
                                          size: 15,
                                        ),
                                      ],
                                    )),
                              ),
                              SizedBox(height: 15),
                              Text(
                                "Query / Statement",
                                style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black),
                              ),
                              SizedBox(height: 10),
                              SelectableText(
                                _data['topic'],
                                textAlign: TextAlign.justify,
                                style: TextStyle(
                                    fontSize: 15,
                                    color: const Color.fromARGB(
                                        255, 145, 145, 145)),
                              ),
                              SizedBox(height: 15),
                              SelectableText(
                                "Summary",
                                style: TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.black,
                                    wordSpacing: 2),
                              ),
                              SizedBox(height: 10),
                              SelectableText(
                                _data['summary'],
                                textAlign: TextAlign.justify,
                                style: TextStyle(
                                    fontSize: 16,
                                    color: const Color.fromARGB(
                                        255, 145, 145, 145)),
                              ),
                            ],
                          ),
                        )
                      ],
                    ),
                ]))),
          ),
        )
        // ==== End of Body =======
        );
  }
}

void _showDiaglogBlockTranscript(
  BuildContext context,
  String title,
  String value,
) {
  var jsonList = json.decode(value);
  int counter = -1;

  showDialog(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        backgroundColor: Colors.white,
        contentPadding: EdgeInsets.all(7), // Remove default padding
        content: Stack(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                mainAxisSize: MainAxisSize.min, // Make column wrap content
                children: [
                  Text(
                    title,
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  SizedBox(height: 16),
                  Flexible(
                    child: SingleChildScrollView(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: jsonList.map<Widget>((mapItem) {
                          counter++;
                          return Padding(
                            padding: const EdgeInsets.only(bottom: 8.0),
                            child: RichText(
                              text: TextSpan(
                                style: TextStyle(
                                    fontSize: 14, color: Colors.black),
                                children: [
                                  if (counter % 2 == 0 && counter != 0)
                                    TextSpan(text: "\n"),
                                  TextSpan(
                                    text: "${mapItem["speaker"]}: ",
                                    style:
                                        TextStyle(fontWeight: FontWeight.bold),
                                  ),
                                  TextSpan(
                                    text: mapItem["text"].toString(),
                                  ),
                                ],
                              ),
                            ),
                          );
                        }).toList(),
                      ),
                    ),
                  ),
                ],
              ),
            ),
            Positioned(
              top: 0,
              right: 0,
              child: IconButton(
                onPressed: () {
                  Navigator.of(context).pop();
                },
                icon: Icon(Icons.close),
              ),
            ),
          ],
        ),
      );
    },
  );
}
