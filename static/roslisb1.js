// Ros WEB SOCKET SERVER CONF

var ros = new ROSLIB.Ros({
    //url : 'ws:192.168.0.141:9090'
    url : 'ws:192.168.70.200:9090'
  });

  ros.on('connection', function() {
    document.getElementById("status").innerHTML = "Connected";
  });

  ros.on('error', function(error) {
    document.getElementById("status").innerHTML = "Error";
  });

  ros.on('close', function() {
    document.getElementById("status").innerHTML = "Closed";
  });

function mapLoad(){
  var viewer2D = new ROS2D.Viewer({
    divID : 'map',
    width : 1445 ,
    height : 880
  });

  var gridClient = new ROS2D.OccupancyGridClient({
    ros : ros,
    rootObject : viewer2D.scene,
    image: 'turtlebot.png',
    continuous: true
  });

  var robotMarker = new ROS2D.ArrowShape({
    size : 0.2,
    strokeSize : 0.2,
    pulse : false
  });

  var poseTopic = new ROSLIB.Topic({
    ros : ros,
    name : '/slam_out_pose',
    messageType:'geometry_msgs/PoseStamped',
  });

  poseTopic.subscribe(
    function (pose) {
      console.log(pose);
      console.log(pose.pose.position.x);
    }
  );

  poseTopic.subscribe(
  function(pose) {
    robotMarker.x = pose.pose.position.x;
    robotMarker.y = -pose.pose.position.y;

    let orientationQuerter=pose.pose.orientation
    var q0 = orientationQuerter.w;
    var q1 = orientationQuerter.x;
    var q2 = orientationQuerter.y;
    var q3 = orientationQuerter.z;
    degree=-Math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)) * 180.0 / Math.PI
    robotMarker.rotation = degree;
  });

  gridClient.rootObject.addChild(robotMarker);
  resize = 0.2
  gridClient.on('change', function(){
    viewer2D.scaleToDimensions(gridClient.currentGrid.width * resize, gridClient.currentGrid.height * resize);
    viewer2D.shift(gridClient.currentGrid.pose.position.x * resize, gridClient.currentGrid.pose.position.y * resize);
  });
}

// window.onload는 최종에 있는거 한번만 실행됨
window.addEventListener('onload', 
  console.log("mapload"),
  mapLoad()
)
