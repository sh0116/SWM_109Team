import 'package:flutter/material.dart';
import 'package:app109/dataCenter.dart';
import 'package:http/http.dart' as http;

class nowUserInfo extends StatefulWidget {
  nowUserInfo({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _nowUserInfoState createState() => _nowUserInfoState();
}

class _nowUserInfoState extends State<nowUserInfo> {

  @override
  initState() {
    super.initState();

//    await fetchData(http.Client(), "user_info/name", "prot_id", getProtId()).then((fetchName) {
//      //print(fetchName);
//      setUserName(fetchName);
//    });
//    await fetchData(http.Client(), "user_info/gender", "prot_id", getProtId()).then((fetchGender) {
//      //print(fetchGender);
//      setUserGender(fetchGender);
//    });
//    await fetchData(http.Client(), "user_info/birth", "prot_id", getProtId()).then((fetchBirthday) {
//      //print(fetchBirthday);
//      setUserBirthday(fetchBirthday);
//    });
//    await fetchData(http.Client(), "user_info/address", "prot_id", getProtId()).then((fetchAddress) {
//      //print(fetchAddress);
//      setUserAddress(fetchAddress);
//    });
//    await fetchData(http.Client(), "user_info/contact", "prot_id", getProtId()).then((fetchContact) {
//      //print(fetchContact);
//      setUserContact(fetchContact);
//    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('check now user')
      ),
      body: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            SizedBox(height:20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Name:'),
                SizedBox(width:20),
                Text(getUserName())
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Gender:'),
                SizedBox(width:20),
                Text(getUserGender())
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Birthday:'),
                SizedBox(width:20),
                Text(getUserBirthday())
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Address:'),
                SizedBox(width:20),
                Text(getUserAddress())
              ],
            ),
            SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                Text('Contact:'),
                SizedBox(width:20),
                Text(getUserContact())
              ],
            )
          ],
        )
      )
    );
  }
}