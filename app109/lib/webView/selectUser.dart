import 'dart:io';

import 'package:flutter/material.dart';
import 'package:app109/dataCenter.dart';
import 'package:app109/webView/webView.dart';

class selectUser extends StatefulWidget {
  selectUser({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _selectUserState createState() => _selectUserState();
}

class _selectUserState extends State<selectUser> {
  var namesList = new List<String>();
  var idsList = new List<String>();

  @override
  void initState() {
    super.initState();
    namesList = userNameList;
    idsList = userIdList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('사용자 선택', style: TextStyle(fontSize: 20)),
      ),
      body: ListView.separated(
        padding: const EdgeInsets.all(15.0),
        itemCount: namesList.length,
        separatorBuilder: (BuildContext context, int index) => Divider(),
        itemBuilder: (BuildContext context, int index) {
          return Container(
            height: 80,
            //color: Colors.amber,
            child: RaisedButton(
              //padding: EdgeInsets.all(10),
              child: Center(
                child: Text(
                  '${namesList[index]}',
                  style: TextStyle(color: Colors.black, fontSize: 25)
                )
              ),
              onPressed: (){
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => webView(userId: idsList[index]),
                  ),
                );
              },
              shape: RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(50.0)
              ),
              color: Colors.white54,
            )
          );
        }
      )
    );
  }
}