import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;
import 'package:test109/dataCenter.dart';
import 'package:test109/initialSetUp/ssh.dart';
import 'package:flutter_datetime_picker/flutter_datetime_picker.dart';

class medicineInfo extends StatefulWidget {
  medicineInfo({Key key, this.title, this.userId}) : super(key: key);
  final String title;
  final String userId;

  @override
  _medicineInfoState createState() => _medicineInfoState();
}

class _medicineInfoState extends State<medicineInfo> {
  String _medicineName = 'name';
  bool checkedMon = false, checkedTue = false, checkedWed = false, checkedThu = false, checkedFri = false, checkedSat = false, checkedSun = false;
  String _checkedMon = '0', _checkedTue = '0', _checkedWed = '0', _checkedThu = '0', _checkedFri = '0', _checkedSat = '0', _checkedSun = '0';
  //TimeOfDay time1, time2, time3;
  String _time1 = '', _time2 = '', _time3 = '';

  @override
  Widget build(BuildContext context){
    return Scaffold(
        appBar: AppBar(title: Text("약 정보 추가")),
        body: SingleChildScrollView(
            child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: <Widget>[
                  SizedBox(height: 50),
                  Text('약 정보 입력', style: TextStyle(fontSize: 25)),
                  SizedBox(height: 40),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text('이름'),
                      Container(
                        child: TextField(
                          controller: TextEditingController(),
                          style: TextStyle(fontSize: 21, color: Colors.black),
                          textAlign: TextAlign.center,
                          onChanged: (String str){
                            _medicineName = str;
                          },
                        ),
                        width: 170,
                        padding: EdgeInsets.only(left: 16),
                      )
                    ],
                  ),
                  SizedBox(height: 30),
                  Text('요일 선택'),
                  CheckboxListTile(
                    title: Text("월요일"),
                    value: checkedMon,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedMon = newMonValue;
                        _checkedMon = checkedMon ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("화요일"),
                    value: checkedTue,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedTue = newMonValue;
                        _checkedTue = checkedTue ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("수요일"),
                    value: checkedWed,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedWed = newMonValue;
                        _checkedWed = checkedWed ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("목요일"),
                    value: checkedThu,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedThu = newMonValue;
                        _checkedThu = checkedThu ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("금요일"),
                    value: checkedFri,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedFri = newMonValue;
                        _checkedFri = checkedFri ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("토요일"),
                    value: checkedSat,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedSat = newMonValue;
                        _checkedSat = checkedSat ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  CheckboxListTile(
                    title: Text("일요일"),
                    value: checkedSun,
                    onChanged: (newMonValue) {
                      setState(() {
                        checkedSun = newMonValue;
                        _checkedSun = checkedSun ? '1' : '0';
                      });
                    },
                    controlAffinity: ListTileControlAffinity.leading,
                    //contentPadding: EdgeInsets.all(0),
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text('시간 1'),
                      Container(
                        child: RaisedButton(
                          child: Text(
                            '시간 선택하기',
                            style: TextStyle(color: Colors.blue),
                          ),
                          onPressed: () async {
                            DatePicker.showTime12hPicker(context,
                              showTitleActions: true,
                              //minTime: DateTime(1900, 1, 1),
                              //maxTime: DateTime.now(),
                              onChanged: (time) {
                                print('change $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time1 = hour+min+"00";
                              },
                              onConfirm: (time) {
                                print('confirm $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time1 = hour+min+"00";
                                print(_time1);
                              },
                              //currentTime: DateTime.now(), locale: LocaleType.ko);
                            );
                          },
                        ),
                        height: 40,
                        padding: EdgeInsets.only(left: 16),
                      )
                    ],
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text('시간 2'),
                      Container(
                        child: RaisedButton(
                          child: Text(
                            '날짜 선택하기',
                            style: TextStyle(color: Colors.blue),
                          ),
                          onPressed: () async {
                            DatePicker.showTime12hPicker(context,
                              showTitleActions: true,
                              //minTime: DateTime(1900, 1, 1),
                              //maxTime: DateTime.now(),
                              onChanged: (time) {
                                print('change $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time2 = hour+min+"00";
                              },
                              onConfirm: (time) {
                                print('confirm $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time2 = hour+min+"00";
                                print(_time2);
                              },
                              //currentTime: DateTime.now(), locale: LocaleType.ko);
                            );
                          },
                        ),
                        height: 40,
                        padding: EdgeInsets.only(left: 16),
                      )
                    ],
                  ),
                  SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: <Widget>[
                      Text('시간 3'),
                      Container(
                        child: RaisedButton(
                          child: Text(
                            '날짜 선택하기',
                            style: TextStyle(color: Colors.blue),
                          ),
                          onPressed: () async {
                            DatePicker.showTime12hPicker(context,
                              showTitleActions: true,
                              //minTime: DateTime(1900, 1, 1),
                              //maxTime: DateTime.now(),
                              onChanged: (time) {
                                print('change $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time3 = hour+min+"00";
                              },
                              onConfirm: (time) {
                                print('confirm $time');
                                String hour = time.hour < 10 ? "0"+time.hour.toString() : time.hour.toString();
                                String min = time.minute < 10 ? "0"+time.minute.toString() : time.minute.toString();
                                _time3 = hour+min+"00";
                                print(_time3);
                              },
                              //currentTime: DateTime.now(), locale: LocaleType.ko);
                            );
                          },
                        ),
                        height: 40,
                        padding: EdgeInsets.only(left: 16),
                      )
                    ],
                  ),
                  SizedBox(height: 50),
                  Container(
                    child: RaisedButton(
                        child: Text('등록'),
                        onPressed: () async {
                          setState(() {});
                          Map<String, dynamic> jsonBody = {
                            'name': "'"+_medicineName+"'",
                            'user_id': "'"+widget.userId+"'",
                            '월': "'"+_checkedMon+"'",
                            '화': "'"+_checkedTue+"'",
                            '수': "'"+_checkedWed+"'",
                            '목': "'"+_checkedThu+"'",
                            '금': "'"+_checkedFri+"'",
                            '토': "'"+_checkedSat+"'",
                            '일': "'"+_checkedSun+"'",
                            'time1': "'"+_time1+"'",
                            'time2': "'"+_time2+"'",
                            'time3': "'"+_time3+"'"};
                          print(jsonBody);
                          await postData('medicine_data', jsonBody).then((val) async {
                            Navigator.pop(context);
                          });
                        }
                    ),
                  ),
                  SizedBox(height: 50),
                ]
            )
        )
    );
  }
}
