import 'package:flutter/material.dart';
import 'package:test109/dataCenter.dart';
import 'package:http/http.dart' as http;
import 'package:test109/medicine/medicineInfo.dart';

class medicine extends StatefulWidget {
  medicine({Key key, this.userId}) : super(key: key);
  final String userId;

  @override
  _medicineState createState() => _medicineState();
}

class _medicineState extends State<medicine> {
  List<Medicine> medicineList = new List<Medicine>();

  @override
  initState(){
    getMedicineList();
    super.initState();
  }

  Future<void> getMedicineList() async{
    await fetchData(http.Client(), "medicine_data/info", "user_id", widget.userId).then((fetchMedicineData) async {
      //print(fetchName);
      //setUserName(fetchUserName);
      List<String> medicineString = StrToList(fetchMedicineData);
      //print("print medicine string");
      print(medicineString);
      medicineList = ListToMedicine(medicineString);
      //print("print medicine list");
      //print(medicineList[0].name + medicineList[1].name);
      print("--fetch medicine list success");
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('약 목록'),
        ),
        body: ListView.separated(
          padding: const EdgeInsets.all(10.0),
          itemCount: medicineList.length,
          itemBuilder: (BuildContext context, int index){
            return medicineTile(medicineList[index]);
          },
          separatorBuilder: (context, index) {
            return Divider();
          },
        ),
        floatingActionButton: FloatingActionButton(
          child: Icon(Icons.add),
          backgroundColor: Colors.blue,
          onPressed: () {
            Navigator.push(context, MaterialPageRoute<void>(builder: (BuildContext context){
              return medicineInfo(userId: widget.userId);
            })
            );
          },
        ),
    );
  }
}

class medicineTile extends StatefulWidget {
  medicineTile(this.med);
  final Medicine med;

  @override
  _medicineTileState createState() => _medicineTileState();
}

class _medicineTileState extends State<medicineTile>{
  List<String> weeks = ['월','화','수','목','금','토','일'];

  String validWeekday(List weekday){
    String retWeekday = "";
    print(weekday);
    for(var i = 0 ; i < weekday.length ; i++){
      if(weekday[i] == true){
        retWeekday += weeks[i];
        retWeekday += ", ";
      }
    }
    retWeekday = retWeekday.substring(0,retWeekday.length-2);
    return retWeekday;
  }

  String validTime(List time){
    String retTime = "";
    for(var i = 0 ; i < time.length ; i++){
      if(time[i] == 'N') break;
      retTime += time[i];
      retTime += ", ";
    }
    retTime = retTime.substring(0, retTime.length-2);
    return retTime;
  }

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Text(widget.med.name, textAlign: TextAlign.center,),
      title: Text(validWeekday(widget.med.week), textAlign: TextAlign.center,),
      subtitle: Text(validTime(widget.med.time), textAlign: TextAlign.center,),
    );

  }
}