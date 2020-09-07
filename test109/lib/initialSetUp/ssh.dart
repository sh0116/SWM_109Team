import 'dart:async';
import 'package:flutter/services.dart';
import 'package:flutter/material.dart';
import 'package:ssh/ssh.dart';

class ssh extends StatefulWidget {
  ssh({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _sshState createState() => _sshState();
}

class _sshState extends State<ssh> {
  String _result = '';
  List _array;

  Future<void> onClickCmd() async {
    var client = new SSHClient(
      host: "172.30.1.8",
      port: 22,
      username: "pi",
      passwordOrKey: "raspberry",
    );

    String result;
    try {
      result = await client.connect();
      if (result == "session_connected") result = await client.execute("ps");
      client.disconnect();
    } on PlatformException catch (e) {
      print('Error: ${e.code}\nError Message: ${e.message}');
    }

    setState(() {
      _result = result;
      _array = null;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        children: <Widget> [
          RaisedButton(
              child: Text("test ps"),
              onPressed: onClickCmd,
              color: Colors.blue
          ),
          SizedBox(height: 50),
          Text(_result)
        ]
      )
    );
  }
}