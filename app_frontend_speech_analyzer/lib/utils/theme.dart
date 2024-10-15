import 'package:flutter/material.dart';

const Color cardColor = Color.fromARGB(255, 251, 253, 255);

ThemeData customTheme = ThemeData(
  cardTheme: const CardTheme(
      elevation: 0,
      color: cardColor,
      shadowColor: cardColor,
      shape: RoundedRectangleBorder(side: BorderSide.none)
      // margin: EdgeInsets.all(12),
      ),
  textSelectionTheme: TextSelectionThemeData(
    selectionColor:
        Colors.blue.withOpacity(0.5), // Blue selection color with transparency
    selectionHandleColor: Colors.blue[900], // Handle color
  ),
);
