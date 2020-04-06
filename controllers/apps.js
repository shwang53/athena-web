/**
 * GET /
 * index page.
 */

exports.getApps = (req, res) => {
  res.render('apps/index', {
    title: 'Applications'
  });
};

exports.getTargetTracker = (req, res, next) => {
  res.render('apps/target_tracker', {
    title: 'Target Tracker',
    target_locs: []
  })
};

exports.postTargetTracker = (req, res, next) => {
  console.log("postTargetTracker");
  var targets = require('../public/target_tracker/targets.json');
  var cameras = require('../public/target_tracker/cameras.json');

  data = JSON.stringify({
    target_locs: JSON.stringify(targets[req.body.target]),
    camera_time: JSON.stringify(cameras[req.body.target][req.body.algo])
  })
  res.send(data);

};

exports.getFloodDataset = (req, res, next) => {
  res.render('apps/eu_flood_dataset', {
    title: 'EU Flood Dataset',
    target_locs: []
  })
};

exports.postFloodDataset = (req, res, next) => {
  console.log("postFloodDataset");
  var metadata = require('../public/eu_flood_dataset/metadata.json');  
  result = []

  metadata.forEach(function(meta){        
    ts = timestamp(meta['capture_time']);
    stime = timestamp(req.body.stime);
    etime = timestamp(req.body.etime);
    
    if (meta.hasOwnProperty('coordinates') && ts >= stime && ts <= etime) {      
      result.push(meta);
    }
  })

  data = JSON.stringify(result);
  res.send(data);
    
};

// Create a new date from a string, return as a timestamp.
function timestamp(str) {
  return new Date(str).getTime();
};


exports.getSA = (req, res, next) => {
  res.render('apps/sa', {
    title: 'Situational Awareness',
    target_locs: []
  })
};

exports.postSA = (req, res) => {    

  if (req.body.type == 'prefix') {
    console.log('postSA for prefix');
    var metadata = require('../public/sa/prefix.json'); 
    // var active_prefix = require('../public/sa/active_prefix.json'); 
    data = JSON.stringify(metadata);
    res.send(data);

  } else if (req.body.type == 'select') {
    console.log('Request for select');
    // Generate list    
    let prefixes = JSON.stringify(req.body.prefix);
    let algo = req.body.algorithm;
    let budget = req.body.budget;
    let coverage = req.body.coverage;
    
    let runPy = new Promise(function(resolve, reject) {
      const { spawn } = require('child_process');
      const pyprog = spawn('python3', ['public/sa/prioritizer.py', req.user.email, prefixes, algo, budget]);      
      
      pyprog.stdout.on('data', (data) => {
        // console.log(`pyprog stdout:\n${data}`);
        resolve(data);
      });

      pyprog.stderr.on('data', (data) => {
        console.error(`pyprog stderr:\n${data}`);
      });

      setTimeout(() => reject(new Error("Whoops!")), 10000);
    });
    
    runPy.then(function(result) {
      console.log(result.toString());        
      res.end(result);      
    }, function(error) {
      console.log("Timeouted");  
      res.end("Failed!");
    })    
    
  } else if (req.body.type == 'retrieve') {

    console.log(req.body.name);
    let runPy = new Promise(function(resolve, reject) {
      const { spawn } = require('child_process');
      const pyprog = spawn('python3', ['public/sa/consumer.py', req.body.name]);      

      pyprog.stdout.on('data', (data) => {
        // console.log(`pyprog stdout:\n${data}`);
        resolve(data);
      });

      pyprog.stderr.on('data', (data) => {
        console.error(`pyprog stderr:\n${data}`);
      });

      setTimeout(() => reject(new Error("Whoops!")), 10000);
    });

    runPy.then(function(result) {
      // console.log(result.toString());  
      res.end(result);
    }, function(error) {
      console.log("Timeouted");  
      res.end("Failed!");
    })    

  } else {  
    
    console.log("Undefined request type: ", req.body.type)
    res.end("Undefined request type");    

  }
};

exports.getRR = (req, res, next) => {
  res.render('apps/rr', {
    title: 'Route Reconnaissance',
    target_locs: []
  })
};

exports.postRR = (req, res) => {    

  if (req.body.type == 'init') {
    console.log('postRR for init');    
    var routes = require('../public/rr/routes.json');      
    data = JSON.stringify(routes);
    res.send(data);

  } else if (req.body.type == 'routes') {
    console.log('postRR for routes');    

    let routes = JSON.stringify(req.body.routes);    
    let runPy = new Promise(function(resolve, reject) {
      const { spawn } = require('child_process');      
      const pyprog = spawn('python3', ['public/rr/tree_generator.py', req.user.email]);      

      pyprog.stdout.on('data', (data) => {
        console.log(`pyprog stdout:\n${data}`);
        resolve(data);
      });

      pyprog.stderr.on('data', (data) => {
        console.error(`pyprog stderr:\n${data}`);
      });

      setTimeout(() => reject(new Error("Whoops!")), 10000);
    });

    runPy.then(function(result) {
      // console.log(result.toString());  
      res.end(result.toString());
    }, function(error) {
      console.log("Timeouted");  
      res.end("Failed!");
    })    
  } else if (req.body.type == 'decide') {
    console.log('postRR for decision');    
    let runPy = new Promise(function(resolve, reject) {
      const { spawn } = require('child_process');      
      const pyprog = spawn('python3', ['public/rr/route_finder.py', req.user.email, req.body.vehicle_weight, req.body.source, req.body.dest, req.body.annotator]);      

      pyprog.stderr.on('data', (data) => {
        console.error(`pyprog stderr:\n${data}`);
      });

      resolve("Running");
    });

    runPy.then(function(result) {      
      res.end(result);
    }, function(error) {
      console.log("Timeouted");  
      res.end("Failed!");
    })    
  } else if (req.body.type == 'annotate') {
    console.log('postRR for human annotation');    
    let runPy = new Promise(function(resolve, reject) {
      const { spawn } = require('child_process');      
      const pyprog = spawn('python3', ['public/rr/annotate.py', req.user.email, req.body.value]);      

      pyprog.stdout.on('data', (data) => {
        console.log(`pyprog stdout:\n${data}`);
        resolve(data);
      });

      pyprog.stderr.on('data', (data) => {
        console.error(`pyprog stderr:\n${data}`);
      });

    });

    runPy.then(function(result) {      
      res.end(result);
    }, function(error) {
      console.log("Timeouted");  
      res.end("Failed!");
    })   
  } else if (req.body.type == 'reset') {

    console.log('postRR for reset');        
    //pkill.full("python3 route_finder.py "+req.user.email);

    var process = require('child_process');
    process.exec('pkill -f route_finder.py', function(err, stdout, stderr) {
        if (err) {
	    console.log("\n"+stderr);
	} else {
	    console.log(stdout);
	}
    });

    console.log("Done!");
    
  } else {  
    
    console.log("Undefined request type: ", req.body.type)
    res.end("Undefined request type");    

  }
};
