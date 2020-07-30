import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'package:test109/menu.dart';

void main() {
  runApp(MaterialApp(
    title: 'test 109',
    home: Scaffold(
      resizeToAvoidBottomPadding: false,
      appBar: AppBar(title: Text('test 109')),
      body: login(),
    ),
  ));
}

class login extends StatefulWidget {
  login({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _loginState createState() => _loginState();
}

Future<String> fetchProt(http.Client client, String contact) async {
  // 해당 URL로 데이터를 요청하고 수신함
  final response = await client.get('http://13.209.4.217:5555/prot_info_post?contact='+contact);
  //print(response.body);
  // parsePhotos 함수를 백그라운도 격리 처리
  return response.body;
}

class _loginState extends State<login> {
  String protName = 'name';
  String protContact = 'contact';
  String delay = ' ';

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[
        Text('Login - protector'),
        SizedBox(height: 20),
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
                  protName = str;
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
            Text('Contact'),
            Container(
              child: TextField(
                controller: TextEditingController(),
                style: TextStyle(fontSize: 21, color: Colors.black),
                textAlign: TextAlign.center,
                onChanged: (String str){
                  protContact = str;
                },
              ),
              width: 170,
              padding: EdgeInsets.only(left: 16),
            )
          ],
        ),
        SizedBox(height: 50),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            RaisedButton(
              child: Text('LOGIN'),
              onPressed: (){
                fetchProt(http.Client(), protContact).then((fetchName) {
                  if(fetchName == protName){
                    Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
                  } else {
                    setState(() { delay = "wrong name or contact"; });
                  }
                });
              },
            ),
            SizedBox(width: 10),
            RaisedButton(
              child: Text('REGISTER'),
              onPressed: (){
                setState(() {});
                final response = http.post('http://13.209.4.217:5555/prot_info_post',
                  body: jsonEncode(
                    {
                      'name': "'"+protName+"'",
                      'contact': "'"+protContact+"'",
                    },
                  ),
                  headers: {'Content-Type': "application/json"},
                );
              },
            ),
          ],
        ),
        SizedBox(height: 20),
        Text(delay)
      ],
    );
  }
}