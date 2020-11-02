import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

import 'package:app109/dataCenter.dart';
import 'package:app109/menu.dart';

void main() {
  runApp(MaterialApp(
    title: '돌봄로봇 백구',
    home: new SplashScreen(),
      routes: <String, WidgetBuilder>{
        '/login': (BuildContext context) => new login()
      },
    theme: ThemeData(fontFamily: 'SC'),
    /*home: Scaffold(
      resizeToAvoidBottomPadding: false,
      appBar: AppBar(title: Text('돌봄로봇 백구')),
      body: login(),
    ),*/
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
    return Scaffold(
      appBar: AppBar(title: Text("돌봄로봇 백구")),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          SizedBox(height: 60),
          Image.asset("images/logo2.png", width: 250),
          SizedBox(height: 80),
          Text('보호자 로그인', style: TextStyle(fontSize: 25, fontWeight: FontWeight.w700)),
          SizedBox(height: 40),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text('이름', style: TextStyle(fontSize: 20)),
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
              Text('연락처', style: TextStyle(fontSize: 20)),
              Container(
                child: TextField(
                  controller: TextEditingController(),
                  style: TextStyle(fontSize: 21, color: Colors.black),
                  textAlign: TextAlign.center,
                  onChanged: (String str){
                    _protContact = str;
                  },
                  decoration: InputDecoration(
                    //border: InputBorder.,
                    hintText: '숫자만 입력하세요',
                    hintStyle: TextStyle(fontSize: 15.0),
                  ),
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
                child: Text('로그인', style: TextStyle(color: Colors.white)),
                onPressed: () async {
                  // fetch corresponding name to contact
                  await fetchData(http.Client(), "prot_info/name", "contact", _protContact).then((fetchName) async {
                    String nowProtName = StrToList(fetchName)[0];
                    print(fetchName + " " + _protContact);
                    if(nowProtName == _protName){
                      print("--login success");
                      await fetchData(http.Client(), "prot_info/id", "contact", _protContact).then((fetchId) async {
                        print(fetchId);
                        String nowProtId = StrToList(fetchId)[0];
                        _protId = nowProtId;
                        setProtName(_protName);
                        setProtContact(_protContact);
                        setProtId(_protId);
                        await fetchData(http.Client(), "user_info/id", "prot_id", getProtId()).then((fetchUserId) async {
                          print(fetchUserId);
                          //setUserId(fetchUserId);
                          userIdList = StrToList(fetchUserId);
                          await fetchData(http.Client(), "user_info/name", "prot_id", getProtId()).then((fetchUserName) async {
                            //print(fetchName);
                            //setUserName(fetchUserName);
                            userNameList = StrToList(fetchUserName);
                            print(userIdList);
                            print(userNameList);
                            //print(getProtId() + " " + getProtName() + " " + getProtContact());
                            //print(getUserId() + " " + getUserName() + " " + getUserContact());
                            print("--fetch user info success");
                            Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
                          });
                        });
                      });
                    } else {
                      setState(() { _delay = "prot info not found"; });
                    }
                  });
                },
                padding: EdgeInsets.all(15),
                shape: RoundedRectangleBorder(
                    borderRadius: new BorderRadius.circular(50.0)
                ),
                color: Colors.blue,
              ),
              SizedBox(width: 30),
              RaisedButton(
                child: Text('등록', style: TextStyle(color: Colors.white)),
                onPressed: () async {
                  setState(() {});
                  Map<String, dynamic> jsonBody = {'name': "'"+_protName+"'", 'contact': "'"+_protContact+"'",};
                  await postData('prot_info',jsonBody).then((val) async {
                    await fetchData(http.Client(), "prot_info/id", "contact", _protContact).then((fetchId) {
                      print(fetchId);
                      _protId = fetchId;
                      setProtName(_protName);
                      setProtContact(_protContact);
                      setProtId(_protId);
                      Navigator.push( context, MaterialPageRoute(builder: (context) => menu()), );
                    });
                  });
                },
                padding: EdgeInsets.all(15),
                shape: RoundedRectangleBorder(
                    borderRadius: new BorderRadius.circular(50.0)
                ),
                color: Colors.blue,
              ),
            ],
          ),
          SizedBox(height: 20),
          Text(_delay)
        ],
      )
    );
  }
}

class SplashScreen extends StatefulWidget {
  @override
  _SplashScreenState createState() => new _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  startTime() async {
    var _duration = new Duration(seconds: 2);
    return new Timer(_duration, navigationPage);
  }

  void navigationPage() {
    Navigator.of(context).pushReplacementNamed('/login');
  }

  @override
  void initState() {
    super.initState();
    startTime();
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      body: new Center(
        child: new Image.asset('images/logo4.png', width: 350),
      ),
    );
  }
}