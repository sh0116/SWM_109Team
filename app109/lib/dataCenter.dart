import 'dart:core';
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

// MEDICINE
class Medicine{
  String name;
  List<bool> week = new List<bool>(7);
  List<String> time = new List<String>(3);
}

String medicineName = 'medicine';

getMedicineName(){ return medicineName; }

setMedicineName(String name){ medicineName = name; }

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
  //print("print input" + input);
  ret = input.split(r", ");
  //print(ret);
  for(var i = 0 ; i < ret.length ; i++){
    //print(ret[i]);
    if(ret[i][0]=='[') ret[i] = ret[i].substring(1, ret[i].length);
    if(ret[i][ret[i].length-1]==']') ret[i] = ret[i].substring(0, ret[i].length-1);
    //print(ret[i]);
    ret[i] = ret[i].substring(1,ret[i].length-1);
    //print(ret[i]);
  }
  return ret;
}

List<Medicine> ListToMedicine(List input){
  List<Medicine> ret = List<Medicine>();
  for(var i = 0 ; i < input.length ; i+=11){
    Medicine nowMed = new Medicine();
    nowMed.name = input[i];
    //print(input[i]);
    for(var j = 0 ; j < 7 ; j++){
      //print(input[i+1+j]);
      nowMed.week[j] = input[i+1+j] == '1' ? true : false;
    }
    for(var j = 0 ; j < 3 ; j++){
      nowMed.time[j] = input[i+8+j].substring(0,input[i+8+j].length-3);
    }
    ret.add(nowMed);
  }
  return ret;
}

// Flask 서버를 통해 DB에서 값을 가져옴
Future<String> fetchData(http.Client client, String route, String data, String value) async {
  String query = FlaskURL+route+'?'+data+'='+value;
  //print(query);
  final response = await client.get(query);
  print("how" + response.body);
  return utf8.decode(response.bodyBytes);
}

Future<String> fetchAllData(http.Client client, String route, String data, String value) async {
  // 해당 URL로 데이터를 요청하고 수신함
  String query = FlaskURL+route+'?'+data+'='+value;
  final response = await client.get(query);
  print(response.body);
  String result = response.body;
  return result;
}
