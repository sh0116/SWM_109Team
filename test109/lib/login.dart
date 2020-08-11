import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

import 'package:test109/dataCenter.dart';
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

class _loginState extends State<login> {

  String _protName = 'name';
  String _protContact = 'contact';
  String _protId = 'id';
  String _delay = ' ';

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
                  _protName = str;
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
                  _protContact = str;
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
              onPressed: () async {
                // fetch corresponding name to contact
                await fetchData(http.Client(), "prot_info/name", "contact", _protContact).then((fetchName) async {
                  //print(fetchName);
                  if(fetchName == _protName){
                    await fetchData(http.Client(), "prot_info/id", "contact", protContact).then((fetchId) {
                      //print(fetchId);
                      _protId = fetchId;
                      setState((){
                        setProtName(_protName);
                        setProtContact(_protContact);
                        setProtId(_protId);
                      });
                    });
                    await fetchData(http.Client(), "user_info/id", "prot_id", getProtId()).then((fetchId) {
                      //print(fetchName);
                      setUserName(fetchId);
                    });
                    await fetchData(http.Client(), "user_info/name", "prot_id", getProtId()).then((fetchName) {
                      //print(fetchName);
                      setUserName(fetchName);
                    });
                    await fetchData(http.Client(), "user_info/gender", "prot_id", getProtId()).then((fetchGender) {
                      //print(fetchGender);
                      setUserGender(fetchGender);
                    });
                    await fetchData(http.Client(), "user_info/birth", "prot_id", getProtId()).then((fetchBirthday) {
                      //print(fetchBirthday);
                      setUserBirthday(fetchBirthday);
                    });
                    await fetchData(http.Client(), "user_info/address", "prot_id", getProtId()).then((fetchAddress) {
                      //print(fetchAddress);
                      setUserAddress(fetchAddress);
                    });
                    await fetchData(http.Client(), "user_info/contact", "prot_id", getProtId()).then((fetchContact) {
                      //print(fetchContact);
                      setUserContact(fetchContact);
                      Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
                    });
//                    await fetchAllData(http.Client(), "user_info/*", "prot_id", getProtId()).then((fetchUser){
//                      print(fetchUser);
//                      setUserName(fetchUser[0]);
//                      setUserGender(fetchUser[1]);
//                      setUserBirthday(fetchUser[2]);
//                      setUserAddress(fetchUser[3]);
//                      setUserContact(fetchUser[4]);
//
//                      Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
//                    });
                  } else {
                    setState(() { _delay = "prot info not found"; });
                  }
                });
              },
            ),
            SizedBox(width: 10),
            RaisedButton(
              child: Text('REGISTER'),
              onPressed: () async {
                setState(() {});
                final response = http.post(FlaskURL+'prot_info/register',
                  body: jsonEncode(
                    {
                      'name': "'"+_protName+"'",
                      'contact': "'"+_protContact+"'",
                    },
                  ),
                  headers: {'Content-Type': "application/json"},
                );
                await fetchData(http.Client(), "prot_info/id", "contact", protContact).then((fetchId) {
                  print(fetchId);
                  _protId = fetchId;
                  setProtName(_protName);
                  setProtContact(_protContact);
                  setProtId(_protId);
                });
                Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
              },
            ),
          ],
        ),
        SizedBox(height: 20),
        Text(_delay)
      ],
    );
  }
}