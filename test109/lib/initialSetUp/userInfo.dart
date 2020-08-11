import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:test109/dataCenter.dart';
import 'package:test109/initialSetUp/robotInfo.dart';

class userInfo extends StatefulWidget {
  userInfo({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _userInfoState createState() => _userInfoState();
}

class _userInfoState extends State<userInfo> {
  String _userId = 'id';
  String _userName = 'name';
  String _userGender = 'g';
  String _userBirthday = 'birthday';
  String _userAddress = 'address';
  String _userContact = 'contact';
  String _protId = getProtId();

  @override
  Widget build(BuildContext context){
    return Scaffold(
      appBar: AppBar(title: Text("user info")),
      body: SingleChildScrollView(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                SizedBox(height: 40),
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
                          _userName = str;
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
                            _userGender = 'F';
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
                            _userGender = 'M';
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
                                          _userBirthday = newDateTime.toString().substring(0,10);
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
                          _userAddress = str;
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
                          _userContact = str;
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
                      child: Text('register'),
                      onPressed: () async {
                        Map<String, dynamic> jsonBody = {'name': "'"+_userName+"'",'gender': "'"+_userGender+"'",'birth': "'"+_userBirthday+"'",'address': "'"+_userAddress+"'",'contact': "'"+_userContact+"'",'prot_id': "'"+getProtId()+"'"};
                        await post('user_info', jsonBody).then((val) async {
                          await fetchData(http.Client(), "user_info/id", "prot_id", getProtId()).then((fetchId) {
                            //print(fetchId);
                            _userId = fetchId;
                            setUserId(_userId);
                            setUserName(_userName);
                            setUserGender(_userGender);
                            setUserBirthday(_userBirthday);
                            setUserAddress(_userAddress);
                            setUserContact(_userContact);
                            Navigator.push( context, MaterialPageRoute(builder: (context) => robotInfo()), );
                          });
                        });
                        //print(_userName + _userContact);
                      }
                  ),
                ),
              ]
          )
      )
    );
  }
}
