import 'dart:core';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

// FLASK SERVER
String FlaskURL = 'http://13.125.221.213:5000/';

// USER
String userId = '0';
String userName = '이름';
String userGender = 'F';
String userBirthday = '2000-01-01';
String userAddress = '주소';
String userContact = '010-1111-1111';

getUserId(){ return userId; }
getUserName(){ return userName; }
getUserGender(){ return userGender; }
getUserBirthday(){ return userBirthday; }
getUserAddress(){ return userAddress; }
getUserContact(){ return userContact; }

setUserId(String id){ userId = id; }
setUserName(String name){ userName = name; }
setUserGender(String gender){ userGender = gender; }
setUserBirthday(String birthday){ userBirthday = birthday; }
setUserAddress(String address){ userAddress = address; }
setUserContact(String contact){ userContact = contact; }

List<String> userIdList = List<String>();
List<String> userNameList = List<String>();

// PROTECTOR
String protId = '0';
String protName = '이름';
String protContact = '010-2222-2222';

getProtId(){ return protId; }
getProtName(){ return protName; }
getProtContact(){ return protContact; }

setProtId(String id){ protId = id; }
setProtName(String name){ protName = name; }
setProtContact(String contact){ protContact = contact; }

// ROBOT
String robotId = 'id';
String robotName = 'name';

getRobotId(){ return robotId; }
getRobotName(){ return robotName; }

setRobotId(String id){ robotId = id; }
setRobotName(String name){ robotName = name; }

// Flask 서버를 통해 DB에 저장
Future<String> postData(String routeTable, Map<String, dynamic> jsonBody) async {
  final http.Response response = await http.post(FlaskURL+routeTable+'/register',
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(jsonBody),
  );
  return 'post';
}

List<String> StrToList(String input){
  List<String> ret = List<String>();
  input = input.substring(1,input.length-1);
  //print(input);
  ret = input.split(r", ");
  //print(ret);
  for(var i = 0 ; i < ret.length ; i++){
    ret[i] = ret[i].substring(2,ret[i].length-2);
  }

  return ret;
}

// Flask 서버를 통해 DB에서 값을 가져옴
Future<String> fetchData(http.Client client, String route, String data, String value) async {
  String query = FlaskURL+route+'?'+data+'='+value;
  final response = await client.get(query);
  //print(StrToList(response.body));
  return response.body;
}

Future<String> fetchAllData(http.Client client, String route, String data, String value) async {
  // 해당 URL로 데이터를 요청하고 수신함
  String query = FlaskURL+route+'?'+data+'='+value;
  final response = await client.get(query);
  print(response.body);
  String result = response.body;
  return result;
}
