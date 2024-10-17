import 'package:flutter/material.dart';
import 'package:pie_chart/pie_chart.dart';
import 'dart:convert';

// ignore: must_be_immutable
class Piechart extends StatelessWidget {
  String? title;
  bool flag;
  Color legendColor;
  String data;
  Map<String, double> dataMap = {};

  Piechart(
      {super.key, required this.title, required this.flag, required this.data})
      : legendColor = flag ? Colors.white : Colors.black {
    jsonConverter();
  }

  Map<String, double> dataMaps = {};

  Map<String, Color> tagColors = {
    "neutral": const Color(0xff3398F6),
    "negative": const Color.fromARGB(255, 217, 4, 4),
    "positive": const Color.fromARGB(255, 0, 221, 118),
    "happy": const Color.fromARGB(255, 0, 221, 118),
    "surprise": const Color.fromARGB(255, 247, 255, 7),
    "joy": const Color.fromARGB(255, 8, 251, 190),
    "fear": const Color.fromARGB(255, 217, 4, 4),
    "frustrated": const Color.fromARGB(255, 255, 85, 0),
    "sad": const Color.fromARGB(255, 255, 107, 21),
    "angry": const Color.fromARGB(255, 255, 132, 0),
  };
  List<Color> colorList = [];

  void jsonConverter() {
    try {
      String validJson = data.replaceAll("'", '"');
      Map<String, dynamic> jsonData = jsonDecode(validJson);
      jsonData.forEach((key, value) {
        dataMap[key] = value.toDouble();
      });
    } catch (e) {
      print("Error parsing JSON: $e"); // Handle parsing errors
    }

    dataMap.forEach((key, value) {
      if (tagColors.containsKey(key.toLowerCase())) {
        colorList.add(tagColors[key.toLowerCase()]!);
      }
    });
    colorList.add(const Color.fromARGB(255, 8, 96, 238));
  }

  @override
  Widget build(BuildContext context) {
    return PieChart(
      dataMap: dataMap,
      colorList: colorList,
      centerText: title,
      chartLegendSpacing: 16,
      centerTextStyle:
          const TextStyle(fontSize: 7, fontWeight: FontWeight.bold),
      ringStrokeWidth: 10,
      animationDuration: const Duration(seconds: 2),
      chartValuesOptions: const ChartValuesOptions(
          showChartValues: true,
          showChartValuesOutside: false,
          showChartValuesInPercentage: true,
          chartValueStyle: TextStyle(
            fontSize: 7,
            color: Colors.black,
            fontWeight: FontWeight.bold,
          ),
          showChartValueBackground: true),
      legendOptions: LegendOptions(
          showLegends: true,
          legendShape: BoxShape.circle,
          legendTextStyle: TextStyle(fontSize: 11, color: legendColor),
          legendPosition: LegendPosition.bottom,
          showLegendsInRow: true),
    );
  }
}
