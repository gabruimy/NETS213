var express = require('express');
var app = express();
var bodyParser= require('body-parser');
var AWS = require('aws-sdk');
var cookieParser = require('cookie-parser');
app.use(cookieParser());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.set('view engine', 'ejs');


AWS.config.loadFromPath(__dirname+"/config.json");

var ddb = new AWS.DynamoDB({apiVersion: '2012-08-10'});





app.get('/', function(req, res){
	res.render(__dirname + "/views/main.ejs");
})

app.post('/locations',function(req,res){
	var params = {
		Select:"ALL_ATTRIBUTES",
		TableName:"Truck_Location"
	}
	ddb.scan(params,function(err,data){
		if(err){
			console.log(err);
		}else{
			var out = JSON.stringify(data);
			res.send(out);
		}
	})

});


app.post('/Menu',function(req,res){
	params = {
		ExpressionAttributeValues: {
   			":v1": {
     			S: req.body.name
    		}
  		},
  		KeyConditionExpression: "Truck_Name = :v1", 
  		ProjectionExpression: "Food,Price",
  		TableName:'Trucks'
	};
	ddb.query(params,function(err,data){
		if(err){
			console.log(err);
		}else{
			var food = new Array();
			var price = new Array();
			data.Items.forEach(function(element){
				food.push(element.Food.S);
				price.push(element.Price.N);
			});
			res.render(__dirname + '/views/menu.ejs',{'food':JSON.stringify(food),'price':JSON.stringify(price)});
		}
	});
});







app.listen(8080,'158.130.178.72');
app.listen(8080,'localhost');