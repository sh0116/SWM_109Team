import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class webView extends StatefulWidget {
  webView({Key key, this.title}) : super(key: key);
  final String title;

  @override
  _webViewState createState() => _webViewState();
}

class _webViewState extends State<webView> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('대시보드')
        ),
        body: WebView(
          //initialUrl: 'http://youtube.com',
          initialUrl: 'http://www.109center.com:5000/userapp',
          javascriptMode: JavascriptMode.unrestricted,
        )
    );
  }
}