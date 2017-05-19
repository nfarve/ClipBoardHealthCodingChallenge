import Record from '../../models/Record';

exports.departmentQuery = function(req,res){
  Record.find({department: req.params.departmentid}).exec(function(err, records){
    if (err)
      res.json({
        err,
        success: false,
      });
    res.json({
      records:records,
      success: true,
    });
  });
};

exports.educationQuery = function(req,res){
  Record.find({education: req.params.educationid}).exec(function(err, records){
    if (err)
      res.json({
        err,
        success: false,
      });
    res.json({
      records:records,
      success: true,
    });
  });
};

exports.salaryQuery = function(req,res){
  if (req.params.direction == "below"){
    Record.find({salary: {$lt: req.params.salaryamount}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
  else{
    Record.find({salary: {$gt: req.params.salaryamount}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
  
};

exports.ratioQuery = function(req,res){
  if (req.params.direction == "below"){
    Record.find({patientNurseRatio: {$lt: req.params.ratio}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
  else{
    Record.find({patientNurseRatio: {$gt: req.params.ratio}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
};

exports.experienceQuery = function(req,res){
  if (req.params.direction == "below"){
    Record.find({experience: {$lt: req.params.experience}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
  else{
    Record.find({experience: {$gt: req.params.experience}}).exec(function(err, records){
      if (err)
        res.json({
          err,
          success: false,
        });
      res.json({
        records:records,
        success: true,
      });
    });
  }
};



exports.all = function(req, res){
  Record.find().then((records) => {
    res.json({
      records: records,
      success: true,
    });
  }).catch((error) => {
    res.json({
      error,
      success: false,
    });
  });
};

