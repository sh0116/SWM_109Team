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
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            SizedBox(height: 100),
            Image.asset("images/logo2.png", width: 250),
            SizedBox(height: 70),
            RaisedButton(
              child: Text('          초기 설정          ', style: TextStyle(fontSize: 25, color: Colors.white)),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return userInfo();
                })
                );
              },
              padding: EdgeInsets.all(20),
              shape: RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(50.0)
              ),
              color: Colors.blue,
            ),
            SizedBox(height: 50),
            RaisedButton(
              child: Text('  사용자 상태 모니터링  ', style: TextStyle(fontSize: 25, color: Colors.white)),
              //child: Icon(Icons.watch_later_sharp),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return selectUser();
                })
                );
              },
              padding: EdgeInsets.all(20),
              shape: RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(50.0)
              ),
              color: Colors.blue,
            ),
            SizedBox(height: 50),
            RaisedButton(
              child: Text('           약 정보           ', style: TextStyle(fontSize: 25, color: Colors.white)),
              onPressed: (){
                Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
                  return selectMedicineUser();
                })
                );
              },
              padding: EdgeInsets.all(20),
              shape: RoundedRectangleBorder(
                  borderRadius: new BorderRadius.circular(50.0)
              ),
              color: Colors.blue,
            )
          ],
        )
      )
    );
  }
}