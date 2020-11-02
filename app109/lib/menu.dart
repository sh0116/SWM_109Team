import 'package:flutter/material.dart';
import 'package:app109/initialSetUp/userInfo.dart';
import 'package:app109/initialSetUp/ssh.dart';
import 'package:app109/webView/selectUser.dart';
import 'package:app109/medicine/selectMedicineUser.dart';

class menu extends StatefulWidget {
  menu({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _menuState createState() => _menuState();
}

class _menuState extends State<menu> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
          title: Text('메뉴'),
          automaticallyImplyLeading: false,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            RaisedButton(
              child: Text('초기 설정'),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return userInfo();
                })
                );
              },
            ),
            SizedBox(height: 20),
            RaisedButton(
              child: Text('사용자 상태 모니터링'),
              //child: Icon(Icons.watch_later_sharp),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return selectUser();
                })
                );
              },
            ),
            SizedBox(height: 20),
            RaisedButton(
              child: Text('약 정보'),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return selectMedicineUser();
                })
                );
              },
            )
          ],
        )
      )
    );
  }
}