let canvas = document.getElementById("canvas");
let ctx = canvas.getContext("2d");
var forkarray =[];
var forkarray_y =[];
let cameraZoom = 1;
let MAX_ZOOM = 5;
let MIN_ZOOM = 0.1;
let SCROLL_SENSITIVITY = 0.0005;
var tag_coordinates = {};
var tagids;
var numberoftags;
var img = new Image();
var showingbot = true;
var showingdBot = false;
var show_AI_Path = false;
var showingmaterial = true;
var showingpeople = true;
var showingcart = true;
var showingpath = true;
var showingstation = true;
var showingZone = false;
var showingOrientation = false;
var path_json, station_json, zone_json;
var recordingstation = false;
var recordingZone = false;
var botstation = false;
var station_x, station_y, station_name, record_x, record_y;
var company_a = sessionStorage.getItem("Company");
var image_opacity = 0.5;
var windowinnerWidth, windowinnerHeight;
var botid, botname;
var botname_coordinates_x = [];
var botname_coordinates_y = [];
var recording_dist = 20;
var timetorecord;
let points = [];
let pointsOfZone_X = [];
let pointsOfZone_Y = [];
var edgesOfZone = [];
let tag_num;
var tag_orientation;
var angle_x;
var lookahead_x, lookahead_y;

if (
  navigator.platform != "iPad" &&
  navigator.platform != "iPhone" &&
  navigator.platform != "iPod"
) {
  windowinnerWidth = window.innerWidth;
  windowinnerHeight = window.innerHeight;
  //I'll use windowinnerWidth in production
} else {
  windowinnerWidth = 1000;
  windowinnerHeight = 1000;
}

let cameraOffset = { x: windowinnerWidth / 2, y: windowinnerHeight / 2 };
// console.log(path_list_dict)

//from http pozyx
var xflipped=1;
var yflipped=-1;
// var scale_factor=23.808595081335405,origin_x=(22454.611586306404/scale_factor),origin_y=yflipped*(-29967.083179526147/scale_factor);

// var xflipped = sessionStorage.getItem("xflipped");
// var yflipped = sessionStorage.getItem("yflipped");
// var scale_factor = sessionStorage.getItem("scale_factor"),
  var scale_factor=0.2796
  origin_x = 53,
  origin_y = 397;

  var real_distance_waypoints=50; //in cm
  record_distance_factor= real_distance_waypoints/(scale_factor*10);


const socket = io();
socket.on('positions', function(data) {
    canvas.width = windowinnerWidth;
    canvas.height = windowinnerHeight;

    // Translate to the canvas centre before zooming - so you'll always zoom on what you're looking directly at
    ctx.translate(windowinnerWidth / 2, windowinnerHeight / 2);
    ctx.scale(cameraZoom, cameraZoom);
    ctx.translate(
      -windowinnerWidth / 2 + cameraOffset.x,
      -windowinnerHeight / 2 + cameraOffset.y
    );
    ctx.clearRect(0, 0, windowinnerWidth, windowinnerHeight);
    img.src="static/FloorPlans/Floor3.png"
    ctx.globalAlpha = image_opacity;
    ctx.drawImage(
      img,
      -img.naturalWidth / 2,
      -img.naturalHeight / 2,
      img.naturalWidth,
      img.naturalHeight
    );
    // ctx.drawImage(img,-1183/2,-635/2,1183,635)
    ctx.globalAlpha = 1;

      // Draw positions
      Object.keys(data).forEach(id => {
          const position = data[id];
          // var xxxx =
          // (xflipped * position[0]) / scale_factor -
          // img.naturalWidth / 2 +
          // origin_x;
          // var yyyy =
          // (yflipped * position[1]) / scale_factor -
          // img.naturalHeight / 2 +
          // origin_y;
          var xxxx =
          (xflipped * position[0]) / scale_factor -
          img.naturalWidth / 2 +
          origin_x;
          var yyyy =
          (yflipped * position[1]) / scale_factor -
          img.naturalHeight / 2 +
          origin_y;
          if(position[2]>2)
          {
            drawCirc(xxxx, yyyy);
            drawstrokeCirc(xxxx, yyyy);
            drawText(
              id,
              xxxx - 13,
              yyyy + 25,
              12,
              "courier"
            );
          }
      });
  });

function increase_opacity() {
  // console.log("rahul's", doc.data())
  if (image_opacity < 1) image_opacity = image_opacity + 0.1;
  else image_opacity = 1;
  console.log(image_opacity);
}

function decrease_opacity() {
  // console.log("rahul's", doc.data())
  if (image_opacity > 0.1) image_opacity = image_opacity - 0.1;
  else image_opacity = 0;
  console.log(image_opacity);
}
// Called after form input is processed


// Called when a message arrives
function onMessageArrived(message) {
  // console.log("onMessageArrived: " + message.payloadString);
  // console.log(typeof(message.payloadString));
  data_json = JSON.parse(message.payloadString);
  var index = Object.keys(data_json).length;

  while (index != 0) {
    index = index - 1;

    // for orientation
    // console.log(data_json[index].data.tagData["eulerAngles"]["x"]);
    if (data_json[index].tagId == "26677") {
      console.log(data_json[index].data.tagData["eulerAngles"]["x"], "rahul");
      tag_orientation = data_json[index].data.tagData["eulerAngles"]["x"];
      if (tag_orientation != undefined) angle_x = tag_orientation;
    }
    // for orientation

    if (data_json[index].data.coordinates) {
      tag_coordinates[data_json[index].tagId] =
        data_json[index].data.coordinates;
      if (data_json[index].tagId == botid) {
        if (botname_coordinates_x.length == 0) {
          botname_coordinates_x.push(data_json[index].data.coordinates.x);
          botname_coordinates_y.push(data_json[index].data.coordinates.y);
        } else {
          // if((tag_coordinates[data_json[index].tagId].x-botname_coordinates_x[botname_coordinates_x.length-1])*(tag_coordinates[data_json[index].tagId].x-botname_coordinates_x[botname_coordinates_x.length-1])-(tag_coordinates[data_json[index].tagId].y-botname_coordinates_y[botname_coordinates_y.length-1])*(tag_coordinates[data_json[index].tagId].y-botname_coordinates_y[botname_coordinates_y.length-1])<recording_dist*recording_dist)
          if (true) {
            botname_coordinates_x.push(
              tag_coordinates[data_json[index].tagId].x
            );
            botname_coordinates_y.push(
              tag_coordinates[data_json[index].tagId].y
            );
          }
        }
      }
      // console.log("botname_x",botname_coordinates_x)
      // console.log("botname_y",botname_coordinates_y)

      if (
        botname_coordinates_x.length == timetorecord &&
        timetorecord != undefined
      ) {
        var botname_coordinates_x_avg = 0;
        var botname_coordinates_y_avg = 0;
        for (i = 0; i < botname_coordinates_x.length; i++) {
          botname_coordinates_x_avg += botname_coordinates_x[i];
          botname_coordinates_y_avg += botname_coordinates_y[i];
        }
        botname_coordinates_x_avg =
          botname_coordinates_x_avg / botname_coordinates_x.length;
        botname_coordinates_y_avg =
          botname_coordinates_y_avg / botname_coordinates_y.length;
        if (stationnamecounter == 0) {
          station_name = prompt("enter station name");
          tag_num = prompt("enter tag number");
          // trigger_interval=prompt("enter trigger interval")
          trigger_interval = 0;
          stationnamecounter = -1;
        }
        if (
          station_name == null &&
          tag_num == null &&
          trigger_interval == null
        ) {
          location.href = "/visualiser";
        }
        db.collection("company")
          .doc(company_a)
          .collection("stations")
          .doc(station_name)
          .set({
            info: {
              dock_type: "",
              tag_num: tag_num,
              trigger_interval: trigger_interval,
              dock_x: 0.0,
              dock_y: 0.0,
              dock_yaw: 0.0,
            },
            pose: {
              x: botname_coordinates_x_avg / 10,
              y: botname_coordinates_y_avg / 10,
            },
          })
          .then((docRef) => {
            // console.log("Document written with ID: ", docRef.id);
            location.href = "/visualiser";
          });
      }
    }
  }
}

// Called when the disconnection button is pressed
function startDisconnect() {
  client.disconnect();
}

function draw() {
  canvas.width = windowinnerWidth;
  canvas.height = windowinnerHeight;

  // Translate to the canvas centre before zooming - so you'll always zoom on what you're looking directly at
  ctx.translate(windowinnerWidth / 2, windowinnerHeight / 2);
  ctx.scale(cameraZoom, cameraZoom);
  ctx.translate(
    -windowinnerWidth / 2 + cameraOffset.x,
    -windowinnerHeight / 2 + cameraOffset.y
  );
  ctx.clearRect(0, 0, windowinnerWidth, windowinnerHeight);
  // ctx.fillStyle = "#991111"
  // drawRect(-50,-50,100,100)

  // ctx.fillStyle = "#eecc77"
  // drawRect(-35,-35,20,20)
  // drawRect(15,-35,20,20)
  // ctx.fillStyle = "#fff"
  // drawText("Simple Pan and Zoom Canvas", -255, -100, 32, "courier")

  // ctx.rotate(-31*Math.PI / 180)
  // ctx.fillStyle = `#${(Math.round(Date.now()/40)%4096).toString(16)}`
  // drawText("Now with touch!", -110, 100, 32, "courier")

  // ctx.fillStyle = "#fff"
  // ctx.rotate(31*Math.PI / 180)

  // drawText("Wow, you found me!", -260, -2000, 48, "courier")

  // img.src = sessionStorage.getItem("Company") + ".jpg";
  img.src="static/FloorPlans/Floor2.png"
  ctx.globalAlpha = image_opacity;
  ctx.drawImage(
    img,
    -img.naturalWidth / 2,
    -img.naturalHeight / 2,
    img.naturalWidth,
    img.naturalHeight
  );
  // ctx.drawImage(img,-1183/2,-635/2,1183,635)
  ctx.globalAlpha = 1;
  tagids = Object.keys(tag_coordinates);
  numberoftags = Object.keys(tag_coordinates).length;
  // console.log(tagids)
  while (numberoftags != 0) {
    // console.log(numberoftags);
    numberoftags = numberoftags - 1;
    var xxxx =
      (xflipped * tag_coordinates[tagids[numberoftags]].x) / scale_factor -
      img.naturalWidth / 2 +
      origin_x;
    var yyyy =
      (yflipped * tag_coordinates[tagids[numberoftags]].y) / scale_factor -
      img.naturalHeight / 2 +
      origin_y;

    // var angle_x = 158.5;
    if (
      tag_status &&
      bot_label_id_data &&
      cart_label_id_data &&
      material_label_id_data &&
      people_label_id_data
    ) {
      // console.log("status",tag_status)
      if (showingbot == true) {
        var status = tag_status[bot_label_id_data[tagids[numberoftags]]];
        if (bot_label_id_data[tagids[numberoftags]] != undefined) {
          // drawCirc(xxxx,yyyy)
          // drawstrokeCirc(xxxx,yyyy)
          console.log(tag_coordinates[tagids[numberoftags]].x,tag_coordinates[tagids[numberoftags]].y);
          if (status == "available") {
            ctx.fillStyle = "green";
          } else if (status == "engaged") {
            ctx.fillStyle = "red";
          }
          drawCirc(xxxx, yyyy);
          drawstrokeCirc(xxxx, yyyy);
          ctx.fillStyle = "black";
          drawText(
            bot_label_id_data[tagids[numberoftags]],
            xxxx - 20,
            yyyy + 22,
            12,
            "courier"
          );
          //   console.log(path_list_dict)
        }
        if (bot_label_id_data[tagids[numberoftags]] == "Gembot1.1")
        {
          ctx.fillStyle="red";
          drawCirc(
            (xflipped * lookahead_x * 10) / scale_factor - img.naturalWidth / 2 + origin_x,
            (yflipped * lookahead_y * 10) / scale_factor - img.naturalHeight / 2 + origin_y
            // origin_x,origin_y
          );
          ctx.fillStyle = "black";
        }
      }
      for(let i=1;i<forkarray.length;i++){
        ctx.beginPath();
        ctx.arc((xflipped * forkarray[i] * 10) / scale_factor - img.naturalWidth / 2 + origin_x, (yflipped * forkarray_y[i] * 10) / scale_factor - img.naturalHeight / 2 + origin_y, 3, 0, 2 * Math.PI);
        ctx.fillStyle = "blue";
        ctx.fill();
        ctx.closePath();
        ctx.fillStyle = "black";
        console.log(forkarray[i],forkarray_y[i]);
      }

      if (showingcart == true) {
        var status = tag_status[cart_label_id_data[tagids[numberoftags]]];
        if (cart_label_id_data[tagids[numberoftags]] != undefined) {
          // drawCirc(xxxx,yyyy)
          // drawstrokeCirc(xxxx,yyyy)
          // console.log("status", status);
          if (status == "available") {
            ctx.fillStyle = "green";
          } else if (status == "engaged") {
            ctx.fillStyle = "red";
          }
          ctx.moveTo(xxxx, yyyy);
          // ctx.lineTo(xxxx + 10 * Math.cos(angle_x), yyyy + 10* Math.sin(angle_x));
          // drawCirc(xxxx, yyyy);
          // drawstrokeCirc(xxxx, yyyy);
          // ctx.fillStyle = "black";
          // ctx.stroke();
          ctx.lineWidth = 2;
          // drawText(
          //   cart_label_id_data[tagids[numberoftags]],
          //   xxxx - 25,
          //   yyyy + 25,
          //   12,
          //   "courier"
          // );
          // console.log(angle_x)
          canvas_arrow(ctx, xxxx, yyyy, (angle_x + 110 + 180 + 60) / 57.296);

          ctx.stroke();
          //   console.log(path_list_dict)
        }
      }

      if (showingmaterial == true) {
        var status = tag_status[material_label_id_data[tagids[numberoftags]]];
        if (material_label_id_data[tagids[numberoftags]] != undefined) {
          // drawCirc(xxxx,yyyy)
          // drawstrokeCirc(xxxx,yyyy)
          console.log("status", status);
          if (status == "available") {
            ctx.fillStyle = "green";
          } else if (status == "engaged") {
            ctx.fillStyle = "red";
          }
          drawCirc(xxxx, yyyy);
          drawstrokeCirc(xxxx, yyyy);
          ctx.fillStyle = "black";
          drawText(
            material_label_id_data[tagids[numberoftags]],
            xxxx - 20,
            yyyy + 22,
            12,
            "courier"
          );
          //   console.log(path_list_dict)
        }
      }

      if (showingpeople == true) {
        var status = tag_status[people_label_id_data[tagids[numberoftags]]];
        if (people_label_id_data[tagids[numberoftags]] != undefined) {
          // drawCirc(xxxx,yyyy)
          // drawstrokeCirc(xxxx,yyyy)
          console.log("status", status);
          if (status == "available") {
            ctx.fillStyle = "green";
          } else if (status == "engaged") {
            ctx.fillStyle = "red";
          }
          drawCirc(xxxx, yyyy);
          drawstrokeCirc(xxxx, yyyy);
          ctx.fillStyle = "black";
          drawText(
            people_label_id_data[tagids[numberoftags]],
            xxxx - 20,
            yyyy + 22,
            12,
            "courier"
          );
          //   console.log(path_list_dict)
        }
      }
    }

    //   console.log(xxxx)
    //   console.log(yyyy)
    //   console.log(numberoftags)
  }
  if (recordingstation == true) {
    document.getElementById("popup1").style.visibility = "visible";
    drawCirc(station_x, station_y);
  }
  if (recordingZone == true) {
    document.getElementById("popup2").style.visibility = "visible";
    // var ctx = canvas.getContext("2d");
    polySort(points);
    drawZone(points);
  }

  if (station_json != undefined) {
    if (showingstation == true) {
      document.getElementById("station_table_button").style.display = "block";
      // document.getElementById("side_station_table").style.display = "block";
      station_json.forEach(stationPlot);
    }
    else {
      document.getElementById("station_table_button").style.display = "none";
      document.getElementById("side_station_table").style.display = "none";
    }
    
  }

  if (path_json != undefined) {
    if (showingpath == true) {
      array_of_edgesofpath= [];
      document.getElementById("path_table_button").style.display = "block";
      // document.getElementById("side_path_table").style.display = "block";
      const found = array_of_path.find(e => e.index === 1)

      if(found!= null){
        for (let i = 0; i < array_of_path.length; i++) {
          if (array_of_path[i].index === 1) {
            pathPlot(array_of_path[i].doc);
            
          }
        }
      }
      else{
        for (let i = 0; i < array_of_path.length; i++) {
          if (array_of_path[i].index === 0) {
            pathPlot(array_of_path[i].doc);
            
          }
        }
      }
      
      
      
    }

      else {
        document.getElementById("path_table_button").style.display = "none";
        document.getElementById("side_path_table").style.display = "none";
      }
  }
  // var tempx=[],tempy=[];
  // tempX.length=array_of_Dbots.length,tempY.length=array_of_Dbots.length;
  if(showingdBot==true){
    botDPlot(Dbots_x,Dbots_y);
  }

  if (showingZone == true) {
    // zone_json.forEach(zonePlot);
    // console.log("yo");
    array_of_edgesofzone = [];
    // document.getElementById("zone_table_button").style.display = "block";
    document.getElementById("side_zone_table").style.display = "block";
    for (let i = 0; i < array_of_zones.length; i++) {
      if (array_of_zones[i].index === 1) {
        zonePlot(array_of_zones[i].doc);
      }
    }
    for (let i = 0; i < array_of_edgesofzone.length; i++) {
      polySort(array_of_edgesofzone[i]);
      drawZone(array_of_edgesofzone[i]);
    }
  } else {
    document.getElementById("side_zone_table").style.display = "none";
    // document.getElementById("zone_table_button").style.display = "none";
  }

  if (showingOrientation == true) {
  }

  // drawRect(i+10,0,70,20)
  // i+=10;
  // drawRect()
  // console.log(img.width)
  requestAnimationFrame(draw);
}
// const fieldValue = admin.firestore.FieldValue;
// Gets the relevant location from a mouse or single touch event
const formZone = document.querySelector("#newZone");
let zone_name;
let nos_of_coordinates;
function addNewZone() {
  zone_name = formZone.zone_name.value;
  // nos_of_coordinates = formZone.nos_Of_Cordinates.value;
  db.collection("company")
    .doc(company_a)
    .collection("zones")
    .doc(zone_name)
    .set({
      x: [],
      y: [],
      // pose:[]
    })
    .then(function () {
      document.getElementById("popup2").style.display = "none";
      document.getElementById("save").style.display = "inline-block";
      console.log("Now record Zone ");
      // location.href="/visualiser";
    })
    .catch((error) => {
      console.log(error);
      throw new Error("something happened, see detail log");
    });
}
function getEventLocation(e) {
  if (e.touches && e.touches.length == 1) {
    return { x: e.touches[0].clientX, y: e.touches[0].clientY };
  } else if (e.clientX && e.clientY) {
    return { x: e.clientX, y: e.clientY };
  }
}

// function plotPath(x, y)
// {
//     ctx.arc(x, y, 5, 0, 2 * Math.PI);
//     ctx.fill();
// }

function drawCirc(x, y) {
  ctx.beginPath();
  ctx.arc(x, y, 6, 0, 2 * Math.PI);
  // ctx.fillStyle = "black";
  ctx.fill();
  ctx.closePath();
}

function drawstrokeCirc(x, y) {
  ctx.beginPath();
  ctx.globalAlpha = 0.3;
  ctx.arc(x, y, 14, 0, 2 * Math.PI);
  ctx.fill();
  ctx.globalAlpha = 1;
  // ctx.stroke();
  ctx.closePath();
}

function drawRect(x, y, width, height) {
  ctx.fillRect(x, y, width, height);
}

function drawText(text, x, y, size, font) {
  ctx.font = `${size}px ${font}`;
  ctx.fillText(text, x, y);
}

let isDragging = false;
let dragStart = { x: 0, y: 0 };

function onPointerDown(e) {
  isDragging = true;
  dragStart.x = getEventLocation(e).x / cameraZoom - cameraOffset.x;
  dragStart.y = getEventLocation(e).y / cameraZoom - cameraOffset.y;
  if (recordingstation == true) {
    getMousePosition(canvas, e);
    isDragging = false;
  }
  if (recordingZone == true) {
    getMousePositionForZone(canvas, e);

    console.log("on");
    isDragging = false;
    nos_of_coordinates = nos_of_coordinates - 1;

    // if (nos_of_coordinates === 0) {
    //   location.href = "/visualiser";
    // }

    // console.log(nos_of_coordinates);
  }
}

const formAdd = document.querySelector("#newDoc");

let trigger_interval;
function addNewTag() {
  station_name = formAdd.station_name.value;
  tag_num = formAdd.tag_num.value;
  trigger_interval = 0;
  db.collection("company")
    .doc(company_a)
    .collection("stations")
    .doc(station_name)
    .set({
      info: {
        dock_type: "",
        tag_num: tag_num,
        trigger_interval: trigger_interval,
        dock_x: 0.0,
        dock_y: 0.0,
        dock_yaw: 0.0,
      },
    })
    .then(function () {
      document.getElementById("popup1").style.display = "none";
      console.log("added the station");
      // location.href="/visualiser";
    })
    .catch((error) => {
      console.log(error);
      throw new Error("something happened, see detail log");
    });
}
function getMousePosition(canvasElem, event) {
  let rect = canvasElem.getBoundingClientRect();
  record_x = event.clientX - rect.left;
  record_y = event.clientY - rect.top;

  record_x = (record_x - windowinnerWidth / 2) / cameraZoom;
  record_y = (record_y - windowinnerHeight / 2) / cameraZoom;
  record_x = record_x + windowinnerWidth / 2 - cameraOffset.x;
  record_y = record_y + windowinnerHeight / 2 - cameraOffset.y;
  // console.log("Coordinate x: " + event.clientX,
  // "Coordinate y: " + event.clientY);
  // console.log(event.type)
  station_x = record_x;
  station_y = record_y;

  // drawCirc(station_x,station_y);

  // let station_name= popForm.station_name.value;
  // tag_num=popForm.tag_num.value;

  // // trigger_interval=prompt("enter trigger interval")

  // if(station_name==null&&tag_num==null&&trigger_interval==null)
  // {
  //   location.href="/visualiser"
  // }
  db.collection("company")
    .doc(company_a)
    .collection("stations")
    .doc(station_name)
    .update({
      // info:{
      //   dock_type:"",
      //   tag_num:tag_num,
      //   trigger_interval:trigger_interval,
      //   dock_x:0.0,
      //   dock_y:0.0,
      //   dock_yaw:0.0,
      // },
      pose: {
        x:
          ((station_x + img.naturalWidth / 2 - origin_x) *
            scale_factor *
            xflipped) /
          10,
        y:
          ((station_y + img.naturalHeight / 2 - origin_y) *
            scale_factor *
            yflipped) /
          10,
      },
    })
    .then((docRef) => {
      // console.log("Document written with ID: ", docRef.id);
      location.href = "/visualiser";
    });
}

// canvas.onclick = function (e) {
//   let x = e.clientX - this.offsetLeft;
//   let y = e.clientY - this.offsetTop;
//   let match = points.findIndex(([x0, y0]) => Math.abs(x0-x) + Math.abs(y0-y) <= 6);
//   if (match < 0) points.push([x, y]);
//   else points.splice(match, 1); // delete point when user clicks near it.
//   polySort(points);
//   drawZone(points);
// };
function getMousePositionForZone(canvasElem, event) {
  let rect = canvasElem.getBoundingClientRect();
  record_x = event.clientX - rect.left;
  record_y = event.clientY - rect.top;
  // drawCirc(0,0);

  record_x = (record_x - windowinnerWidth / 2) / cameraZoom;
  record_y = (record_y - windowinnerHeight / 2) / cameraZoom;
  record_x = record_x + windowinnerWidth / 2 - cameraOffset.x;
  record_y = record_y + windowinnerHeight / 2 - cameraOffset.y;
  console.log(
    "Coordinate x: " + event.clientX,
    "Coordinate y: " + event.clientY
  );
  // console.log(event.type)
  station_x = record_x;
  station_y = record_y;
  let match = points.findIndex(
    ([x0, y0]) => Math.abs(x0 - station_x) + Math.abs(y0 - station_y) <= 6
  );
  if (match < 0) {
    points.push([station_x, station_y]);
  } else points.splice(match, 1); // delete point when user clicks near it.
  // let station_name= popForm.station_name.value;
  // tag_num=popForm.tag_num.value;

  // // trigger_interval=prompt("enter trigger interval")

  // if(station_name==null&&tag_num==null&&trigger_interval==null)
  // {
  //   location.href="/visualiser"
  // }
  db.collection("company")
    .doc(company_a)
    .collection("zones")
    .doc(zone_name)
    .update({
      x: firebase.firestore.FieldValue.arrayUnion(
        ((station_x + img.naturalWidth / 2 - origin_x) *
          scale_factor *
          xflipped) /
          10
      ),
      y: firebase.firestore.FieldValue.arrayUnion(
        ((station_y + img.naturalHeight / 2 - origin_y) *
          scale_factor *
          yflipped) /
          10
      ),
      // pose: pointsOfZone
      // pose:{x:(station_x+img.naturalWidth/2-origin_x)*scale_factor*xflipped/10,
      // y:(station_y+img.naturalHeight/2-origin_y)*scale_factor*yflipped/10,}
    })
    .then((docRef) => {
      // console.log("Document written with ID: ", docRef.id);
      // console.log(points);
    });
}

function squaredPolar(point, centre) {
  return [
    Math.atan2(point[1] - centre[1], point[0] - centre[0]),
    (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2, // Square of distance
  ];
}

// Main algorithm:
function polySort(points) {
  // Get "centre of mass"
  // console.log("hi");
  let centre = [
    points.reduce((sum, p) => sum + p[0], 0) / points.length,
    points.reduce((sum, p) => sum + p[1], 0) / points.length,
  ];

  // Sort by polar angle and distance, centered at this centre of mass.
  for (let point of points) point.push(...squaredPolar(point, centre));
  points.sort((a, b) => a[2] - b[2] || a[3] - b[3]);
  // Throw away the temporary polar coordinates
  for (let point of points) point.length -= 2;
}

// I/O m
function drawZone(points) {
  // ctx.clearRect(0, 0, canvas.width, canvas.height);
  // console.log(points);
  if (!points.length) {
    // console.log("yo");
    return;
  }
  for (let [x, y] of points) {
    ctx.globalAlpha = 0.4;
    ctx.beginPath();
    ctx.font = "10px Arial";
    // ctx.strokeText("x",x-2,y+2);
    ctx.arc(x, y, 2, 0, 2 * Math.PI);

    ctx.closePath();
    ctx.fill();
  }
  ctx.beginPath();
  ctx.moveTo(...points[0]);
  for (let [x, y] of points.slice(1)) ctx.lineTo(x, y);
  ctx.closePath();

  ctx.fill();
  ctx.globalAlpha = 1;
}

function onPointerUp(e) {
  isDragging = false;
  initialPinchDistance = null;
  lastZoom = cameraZoom;
}

function onPointerMove(e) {
  if (isDragging) {
    cameraOffset.x = getEventLocation(e).x / cameraZoom - dragStart.x;
    cameraOffset.y = getEventLocation(e).y / cameraZoom - dragStart.y;
  }
}

function handleTouch(e, singleTouchHandler) {
  if (e.touches.length == 1) {
    singleTouchHandler(e.touches[0]);
    console.log(e);
    console.log(e.touches[0]);
  } else if (e.type == "touchmove" && e.touches.length == 2) {
    isDragging = false;
    handlePinch(e);
  }
}

let initialPinchDistance = null;
let lastZoom = cameraZoom;

function handlePinch(e) {
  e.preventDefault();

  let touch1 = { x: e.touches[0].clientX, y: e.touches[0].clientY };
  let touch2 = { x: e.touches[1].clientX, y: e.touches[1].clientY };

  // This is distance squared, but no need for an expensive sqrt as it's only used in ratio
  let currentDistance = (touch1.x - touch2.x) ** 2 + (touch1.y - touch2.y) ** 2;

  if (initialPinchDistance == null) {
    initialPinchDistance = currentDistance;
  } else {
    adjustZoom(null, currentDistance / initialPinchDistance);
  }
}

function adjustZoom(zoomAmount, zoomFactor) {
  if (!isDragging) {
    if (zoomAmount) {
      cameraZoom -= zoomAmount;
    } else if (zoomFactor) {
      console.log(zoomFactor);
      cameraZoom = zoomFactor * lastZoom;
    }

    cameraZoom = Math.min(cameraZoom, MAX_ZOOM);
    cameraZoom = Math.max(cameraZoom, MIN_ZOOM);

    console.log(zoomAmount);
  }
}

canvas.addEventListener("mousedown", onPointerDown, false);
canvas.addEventListener(
  "touchstart",
  (e) => handleTouch(e, onPointerDown),
  false
);
canvas.addEventListener("mouseup", onPointerUp, false);
canvas.addEventListener("touchend", (e) => handleTouch(e, onPointerUp), false);
canvas.addEventListener("mousemove", onPointerMove, false);
canvas.addEventListener(
  "touchmove",
  (e) => handleTouch(e, onPointerMove),
  false
);
canvas.addEventListener(
  "wheel",
  (e) => adjustZoom(e.deltaY * SCROLL_SENSITIVITY),
  false
);

// Ready, set, go
// startConnect();
// draw();
