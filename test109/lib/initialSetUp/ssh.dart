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
      host: "192.168.100.70",
      port: 22,
      username: "pi",
      passwordOrKey: "raspberry",
    );

    String result;
    //try {
    result = await client.connect();
    if (result == "session_connected") {
      result = await client.execute("echo 'network={' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
      result = await client.execute("echo '    ssid=\"hub_sungsoo\"' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
      result = await client.execute("echo '    psk=\"1234567890\"' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
      result = await client.execute("echo '    key_mgmt=WPA-PSK' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
      result = await client.execute("echo '}' | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
      result = await client.execute("reboot | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf");
    }
      client.disconnect();
    //}
    //} on PlatformException catch (e) {
     //print('Error: ${e.code}\nError Message: ${e.message}');
    //}

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