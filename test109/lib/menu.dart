import 'package:flutter/material.dart';
import 'package:test109/userInfo.dart';

class menu extends StatefulWidget {
  menu({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _menuState createState() => _menuState();
}

class _menuState extends State<menu> {
  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: <Widget>[
        SizedBox(height: 20),
        RaisedButton(
          child: Text('user info'),
          onPressed: (){
            Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
              return userInfo();
            })
            );
          },

        )
      ],
    );
  }
}