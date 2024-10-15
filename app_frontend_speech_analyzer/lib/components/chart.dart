import 'package:flutter/material.dart';
import 'package:pie_chart/pie_chart.dart';
import 'dart:convert';

// ignore: must_be_immutable
class Piechart extends StatelessWidget {
  String title = "sentiment";
  bool flag = false;
  Color legendColor;
  String data = "";
  Map<String, double> dataMap = {};

  Piechart(
      {super.key, required this.title, required this.flag, required this.data})
      : legendColor = flag ? Colors.white : Colors.black {
    jsonConverter();
  }

  Map<String, double> dataMaps = {
    "Neutral": 10.0,
    "Positive": 13.1,
    "Negative": 50.7,
  };

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
    print(dataMap);
  }

  List<Color> colorList = [
    const Color(0xff3398F6),
    const Color.fromARGB(255, 217, 4, 4),
    const Color.fromARGB(255, 0, 221, 118),
    const Color.fromARGB(255, 233, 103, 11),
  ];

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
