import pandas as pd
import sys
import boto3

def aggregation(truck_data):
	trucks = dict()
	full_number = dict()
	full = list()
	aggr_out = dict()
	for x in truck_data.index:
		name = truck_data.loc[x,"Input.Truck_Name"].lower()
		for y in range(1,31):
			food = "Answer.FoodItem" + str(y)
			data_food = truck_data.loc[x,food].lower()
			price = "Answer.Price" + str(y)
			data_price = "{0:.2f}".format(truck_data.loc[x,price])
			if data_food != "none":
				truck_food = trucks.get(name)
				truck_food_num = full_number.get(name)
				if truck_food == None:
					food_num = dict()
					food_num.update({data_food:1})
					full_number.update({name:food_num})
					foods = dict()
					prices = dict()
					prices.update({data_price:1})
					foods.update({data_food:prices})
					trucks.update({name:foods})
				else:
					food_price = truck_food.get(data_food)
					food_num = truck_food_num.get(data_food)
					if food_price == None:
						truck_food_num.update({data_food:1})
						prices = dict()
						prices.update({data_price:1})
						truck_food.update({data_food:prices})
					else:
						price_last = food_price.get(data_price)
						food_num += 1
						truck_food_num.update({data_food:food_num})
						if price_last == None:
							food_price.update({data_price:1})
						else:
							price_last = price_last + 1
							food_price.update({data_price:price_last})
	for truck, foods in trucks.items():
		for food, prices in foods.items():
			if full_number.get(truck).get(food) > 1:
				num = 0;
				which = "";
				for price, number in prices.items():
					if(number > num):
						num = number
						which = price
				full.append((truck,food,which))
				key = truck + food
				aggr_out.update({key:which})
	return sorted(full), aggr_out

"""
def quality_control(truck_data, aggr_check):
	out_qual_worker = list()
	qual_worker = dict()
	for x in truck_data.index:
		worker_id = truck_data.loc[x,"UserId"]
		name = truck_data.loc[x,"Truck Name"].lower()
		for y in range(1,5):
			food = "FoodItem" + str(y)
			data_food = truck_data.loc[x,food].lower()
			price = "Price" + str(y)
			data_price = "{0:.2f}".format(truck_data.loc[x,price])
			price_actual = aggr_check.get(name + data_food)
			if(data_price == price_actual):
				worker = qual_worker.get(worker_id)
				if worker == None:
					qual_worker.update({worker_id:[1,1]})
				else:
					worker[0] = worker[0] + 1
					worker[1] = worker[1] + 1
					qual_worker.update({worker_id:worker})
			else:
				worker = qual_worker.get(worker_id)
				if(worker == None):
					qual_worker.update({worker_id:[0,1]})
				else:
					worker[1] = worker[1] + 1
					qual_worker.update({worker_id:worker})

	for id, totals in qual_worker.items():
		quality = totals[0] / totals[1]
		out_qual_worker.append((id,quality))

	return sorted(out_qual_worker)
"""


def worker_quality_test(test_data,worker_data):
	worker_quality_test_data = list()
	test_data_dict = dict()
	for y in range(1,31):
		testFoodItem = "FoodItem" + str(y)
		testPrice = "Price" + str(y)
		test_food_out = test_data.loc[0,testFoodItem].lower()
		test_price_out = "{0:.2f}".format(test_data.loc[0,testPrice])
		test_data_dict.update({test_food_out:test_price_out})
	for x in worker_data.index:
		food = 0
		price = 0
		for z in range(1,31):
			foodItem = "Answer.FoodItem" + str(z)
			priceWorker = "Answer.Price" + str(z)
			food_worker = worker_data.loc[x,foodItem].lower()
			price_worker =  "{0:.2f}".format(worker_data.loc[x,priceWorker])
			exist_food = test_data_dict.get(food_worker);
			if exist_food != None:
				food += 1
				if(price_worker == exist_food):
					price += 1
		food_avg = food / 30
		price_avg = price / 30
		out_worker = (worker_data.loc[x,"workerId"],food_avg,price_avg)
		worker_quality_test_data.append(out_worker)
	return sorted(worker_quality_test_data)

def assign_worker_qualifications(worker_qual_data):
	client = boto3.client('mturk')
	for x in worker_qual_data:
		if x[1] >= .9 and x[2] >= .9:
			response = client.associate_qualification_with_worker(
				QualificationTypeId='string',
    			WorkerId=str(x[0]),
    			IntegerValue=100,
    			SendNotification=True)

def main():
	if sys.argv[1] == "real":
		truck_data = pd.read_csv("../data/Test.csv")
		price_out, quality_in = aggregation(truck_data);
		#worker_quality = quality_control(truck_data, quality_in);

		prices_data_frame = pd.DataFrame(price_out, columns=["Truck","Food", "Price"])
		prices_data_frame.to_csv("../data/menu.csv",index=False)

		#quality_data_frame = pd.DataFrame(worker_quality, columns=["UserId","quality"])
		#quality_data_frame.to_csv("../data/quality.csv", index=False)
	elif sys.argv[1] == "test":
		test_data = pd.read_csv("../data/Test_Output_Correct.csv");
		worker_data = pd.read_csv("../data/Test.csv");
		worker_qual_test = worker_quality_test(test_data,worker_data);
		assign_worker_qualifications(worker_qual_test)

if __name__ == '__main__':
    main()