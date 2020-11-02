import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:app109/dataCenter.dart';
import 'package:app109/initialSetUp/ssh.dart';
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';

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
      appBar: AppBar(title: Text("사용자 정보")),
      body: SingleChildScrollView(
          child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                SizedBox(height: 40),
                Text('사용자 정보 입력', style: TextStyle(fontSize: 25)),
                SizedBox(height: 40),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    Text('이름'),
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
                    Text('성별'),
                    Container(
                      height: 50,
                      width: 100,
                      child: ListTile(
                        title: Text('여'),
                        leading: Radio(
                          value: '여',
                          groupValue: userGender,
                          onChanged: (value){
                            _userGender = '';
                          },
                        ),
                      ),
                    ),
                    Container(
                      height: 50,
                      width: 100,
                      child: ListTile(
                        title: Text('남'),
                        leading: Radio(
                          value: '남',
                          groupValue: userGender,
                          onChanged: (value){
                            _userGender = '남';
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
                    Text('생년월일'),
                    Container(
                      child: RaisedButton(
                        child: Text(
                          '날짜 선택하기',
                          style: TextStyle(color: Colors.blue),
                        ),
                        onPressed: () {
                          DatePicker.showDatePicker(context,
                              showTitleActions: true,
                              minTime: DateTime(1900, 1, 1),
                              maxTime: DateTime.now(),
                              onChanged: (date) {
                                print('change $date');
                                _userBirthday = date.toString().substring(0,10);
                              },
                              onConfirm: (date) {
                                print('confirm $date');
                                _userBirthday = date.toString().substring(0,10);
                              },
                              currentTime: DateTime.now(), locale: LocaleType.ko);
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
                    Text('도로명 주소'),
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
                    Text('연락처'),
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
                      child: Text('등록'),
                      onPressed: () async {
                        Map<String, dynamic> jsonBody = {'name': "'"+_userName+"'",'gender': "'"+_userGender+"'",'birth': "'"+_userBirthday+"'",'address': "'"+_userAddress+"'",'contact': "'"+_userContact+"'",'prot_id': "'"+getProtId()+"'"};
                        await postData('user_info', jsonBody).then((val) async {
                          await fetchData(http.Client(), "user_info/id", "prot_id", getProtId()).then((fetchId) {
                            //print(fetchId);
                            _userId = fetchId;
                            setUserId(_userId);
                            setUserName(_userName);
                            setUserGender(_userGender);
                            setUserBirthday(_userBirthday);
                            setUserAddress(_userAddress);
                            setUserContact(_userContact);
                            Navigator.push( context, MaterialPageRoute(builder: (context) => ssh()), );
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
