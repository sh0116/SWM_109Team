import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:test109/dataCenter.dart';

class webView extends StatelessWidget {
  webView({Key key, this.userId}) : super(key: key);
  final String userId;

  @override
  Widget build(BuildContext context) {
    String url = 'http://www.109center.com:5000/userapp?prot_id='+getProtId()+'&user_id='+userId;
    //print(url);
    return Scaffold(
        appBar: AppBar(
            title: Text('대시보드')
        ),
        body: WebView(
          //initialUrl: 'http://youtube.com',
          initialUrl: url,
          javascriptMode: JavascriptMode.unrestricted,
        )
    );
  }
}