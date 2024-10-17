// ignore_for_file: prefer_const_constructors

import 'package:app_frontend_speech_analyzer/pages/home_page.dart';
import 'package:flutter/material.dart';

class CustomAppBar extends StatefulWidget {
  final String title;
  final String userMsg;
  const CustomAppBar({super.key, required this.title, required this.userMsg});

  @override
  State<CustomAppBar> createState() => _CustomAppBarState();
}

class _CustomAppBarState extends State<CustomAppBar> {
  @override
  Widget build(BuildContext context) {
    return AppBar(
        leading: ModalRoute.of(context)?.settings.name != '/'
            ? GestureDetector(
                onTap: () {
                  Navigator.pushNamedAndRemoveUntil(
                    context,
                    '/',
                    (Route<dynamic> route) => false,
                  );
                },
                child: IconButton(
                  icon: Icon(
                    Icons.arrow_back,
                    color: Colors.white,
                  ),
                  onPressed: null,
                ),
              )
            : null,
        toolbarHeight: 70,
        centerTitle: true,
        backgroundColor: const Color.fromARGB(255, 4, 39, 91),
        title: Padding(
          padding: const EdgeInsets.symmetric(vertical: 0, horizontal: 15),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              // Logo
              GestureDetector(
                onTap: () {
                  Navigator.pushNamedAndRemoveUntil(
                    context,
                    '/',
                    (Route<dynamic> route) => false,
                  );
                },
                child: Row(
                  children: [
                    ClipOval(
                      child: Image.asset(
                        'assets/logo.png',
                        height: 60,
                        fit: BoxFit.fill,
                      ),
                    ),
                    const SizedBox(
                      width: 10,
                    ),

                    // Heading
                    const Text(
                      " ABL معاون",
                      style: TextStyle(
                          color: Colors.white, fontWeight: FontWeight.bold),
                    )
                  ],
                ),
              ),

              //  Right-Side Text
              Text(
                widget.userMsg,
                style: const TextStyle(
                    color: Colors.white,
                    fontSize: 13,
                    fontWeight: FontWeight.bold),
              )
            ],
          ),
        ));
  }
}
