import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;

class userInfo extends StatefulWidget {
  userInfo({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _userInfoState createState() => _userInfoState();
}

class _userInfoState extends State<userInfo> {
  String userName = 'name';
  String userGender = 'gender';
  DateTime userBirthday = DateTime.now();
  String userAddress = 'address';
  String userContact = 'contact';

  @override
  Widget build(BuildContext context){
    return SingleChildScrollView(
      child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SizedBox(height: 20),
            Text('[ Input user info ]', style: TextStyle(fontSize: 25)),
            SizedBox(height: 40),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Name'),
                Container(
                  child: TextField(
                    controller: TextEditingController(),
                    style: TextStyle(fontSize: 21, color: Colors.black),
                    textAlign: TextAlign.center,
                    onChanged: (String str){
                      userName = str;
                    },
                  ),
                  width: 170,
                  padding: EdgeInsets.only(left: 16),
                )
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Text('Gender'),
                Container(
                  height: 50,
                  width: 100,
                  child: ListTile(
                    title: Text('F'),
                    leading: Radio(
                      value: 'F',
                      groupValue: userGender,
                      onChanged: (value){
                        userGender = 'F';
                      },
                    ),
                  ),
                ),
                Container(
                  height: 50,
                  width: 100,
                  child: ListTile(
                    title: Text('M'),
                    leading: Radio(
                      value: 'M',
                      groupValue: userGender,
                      onChanged: (value){
                        userGender = 'M';
                      },
                    ),
                  ),
                ),
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Birthday'),
                Container(
                  child: RaisedButton(
                    child: Text('show date picker'),
                    onPressed: () {
                      showCupertinoModalPopup(
                        context: context,
                        builder: (BuildContext context) {
                          return Container(
                            height: 150,
                            padding: EdgeInsets.only(top: 6.0),
                            color: CupertinoColors.white,
                            child: DefaultTextStyle(
                              style: const TextStyle(
                                color: CupertinoColors.black,
                                fontSize: 22.0,
                              ),
                              child: GestureDetector(
                                // Blocks taps from propagating to the modal sheet and popping.
                                onTap: () {},
                                child: SafeArea(
                                  top: false,
                                  child: CupertinoDatePicker(
                                    mode: CupertinoDatePickerMode.date,
                                    initialDateTime: DateTime.now(),
                                    onDateTimeChanged: (DateTime newDateTime) {
                                      userBirthday = newDateTime;
                                    },
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                      );
                    },
                  ),
                  height: 40,
                  padding: EdgeInsets.only(left: 16),
                )
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Address'),
                Container(
                  child: TextField(
                    controller: TextEditingController(),
                    style: TextStyle(fontSize: 21, color: Colors.black),
                    textAlign: TextAlign.center,
                    onChanged: (String str){
                      userAddress = str;
                    },
                  ),
                  width: 150,
                  padding: EdgeInsets.only(left: 16),
                )
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Contact'),
                Container(
                  child: TextField(
                    controller: TextEditingController(),
                    style: TextStyle(fontSize: 21, color: Colors.black),
                    textAlign: TextAlign.center,
                    onChanged: (String str){
                      userContact = str;
                    },
                  ),
                  width: 150,
                  padding: EdgeInsets.only(left: 16),
                )
              ],
            ),
            SizedBox(height: 50),
            Container(
              child: RaisedButton(
                  child: Text('submit'),
                  onPressed: () {
                    setState(() {});
                    final response = http.post('http://13.209.4.217:5555/user_info_post',
                      body: jsonEncode(
                        {
                          'name': "'"+userName+"'",
                          'gender': "'"+userGender+"'",
                          'birth': "'"+userBirthday.toString().substring(0,10)+"'",
                          'address': "'"+userAddress+"'",
                          'contact': "'"+userContact+"'"
                        },
                      ),
                      headers: {'Content-Type': "application/json"},
                    );
                  }
              ),
            ),
            SizedBox(height: 50),
            Text(userName),
            SizedBox(height: 20),
            Text(userGender),
            SizedBox(height: 20),
            Text(userBirthday.toString()),
            SizedBox(height: 20),
            Text(userAddress),
            SizedBox(height: 20),
            Text(userContact)
          ]
      )
    );
  }
}
