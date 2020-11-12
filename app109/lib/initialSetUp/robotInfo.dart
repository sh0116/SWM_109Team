import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:app109/dataCenter.dart';
import 'package:app109/initialSetUp/ssh.dart';

class robotInfo extends StatefulWidget {
  robotInfo({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _robotInfoState createState() => _robotInfoState();
}

class _robotInfoState extends State<robotInfo> {
  String _robotName = 'name';
  String _robotId = 'id';

  @override
  Widget build(BuildContext context){
    return Scaffold(
        appBar: AppBar(title: Text("로봇 정보")),
        body: SingleChildScrollView(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  SizedBox(height: 50),
                  Text('로봇 정보 입력', style: TextStyle(fontSize: 25)),
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
                            _robotName = str;
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
                    children: <Widget>[
                      Text('시리얼번호'),
                      Container(
                        child: TextField(
                          controller: TextEditingController(),
                          style: TextStyle(fontSize: 21, color: Colors.black),
                          textAlign: TextAlign.center,
                          onChanged: (String str){
                            _robotId = str;
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
                          setState(() {});
                          Map<String, dynamic> jsonBody = {'name': "'"+_robotName+"'",'robot_id': "'"+_robotId+"'",'user_id': "'"+getUserId()+"'"};
                          await postData('robot_info', jsonBody).then((val) async {
                            setRobotName(_robotName);
                            setRobotId(_robotId);
                            Navigator.push( context, MaterialPageRoute(builder: (context) => ssh()), );
                          });
                        }
                    ),
                  ),
                ]
            )
        )
    );
  }
}
