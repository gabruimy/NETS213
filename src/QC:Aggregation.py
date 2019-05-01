import pandas as pd
import sys
import boto3
import re
import matplotlib.pyplot as plt

def aggregation(truck_data):
	trucks = dict()
	full_number = dict()
	full = list()
	for x in truck_data.index:
		name = truck_data.loc[x,"Input.truck_name"].lower().replace("_"," ")
		for y in range(1,31):
			food = "Answer.FoodItem" + str(y)
			data_food = truck_data.loc[x,food].lower()
			data_food = data_food.replace("&", "and")
			data_food = data_food.replace(".","")
			data_food = data_food.replace(",","")
			data_food = data_food.replace(" small","")
			data_food = data_food.replace(" large","")
			data_food = re.sub(" \(.*\)","",data_food)
			price = "Answer.Price" + str(y)
			data_price = str(truck_data.loc[x,price])
			data_price = data_price.replace("$","")
			data_price = data_price.split()
			data_price = "{0:.2f}".format(float(data_price[0]))
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
			if full_number.get(truck).get(food) > 2:
				num = 0;
				which = "";
				for price, number in prices.items():
					if(number > num):
						num = number
						which = price
				full.append((truck,food,which))
	return sorted(full)

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


def worker_aggregate_quality(aggregate, truck_data, correct):
	correct_full = list()
	worker_quality = dict()
	aggregate_data = [0,0,0,0]
	for x in correct.index:
		truck = correct.loc[x,"truck"].lower().replace("_"," ");
		for y in range(1,31):
			food = "FoodItem" + str(y)
			correct_food = correct.loc[x,food].lower()
			price = "Price" + str(y)
			correct_price = "{0:.2f}".format(correct.loc[x,price])
			if correct_food != "none":
				correct_full.append((truck,correct_food,correct_price))
	for a in truck_data.index:
		truck = truck_data.loc[a,"Input.truck_name"].lower().replace("_"," ")
		worker = truck_data.loc[a,"WorkerId"]
		for b in range(1,31):
			food = "Answer.FoodItem" + str(b)
			data_food = truck_data.loc[a,food].lower()
			data_food = data_food.replace("&", "and")
			data_food = data_food.replace(".","")
			data_food = data_food.replace(",","")
			data_food = data_food.replace(" small","")
			data_food = data_food.replace(" large","")
			data_food = re.sub(" \(.*\)","",data_food)
			price = "Answer.Price" + str(b)
			data_price = str(truck_data.loc[a,price])
			data_price = data_price.replace("$","")
			data_price = data_price.split()
			data_price = "{0:.2f}".format(float(data_price[0]))
			if data_food != "none":
				right = [x[2] for x in correct_full if x[0] == truck and x[1] == data_food]
				if len(right) != 0:
					worker_hold = worker_quality.get(worker)
					if worker_hold != None:
						if data_price in right:
							worker_hold[0] += 1
							worker_hold[1] += 1
							worker_hold[2] += 1
							worker_hold[3] += 1
							worker_quality.update({worker:worker_hold})
						else:
							worker_hold[0] += 1
							worker_hold[2] += 1
							worker_hold[3] += 1
							worker_quality.update({worker:worker_hold})
					else:
						if data_price in right:
							first = [1,1,1,1]
							worker_quality.update({worker:first})
						else:
							first = [1,0,1,1]
							worker_quality.update({worker:first})
				else:
					worker_hold = worker_quality.get(worker)
					if worker_hold != None:
						worker_hold[0] += 0
						worker_hold[1] += 0
						worker_hold[2] += 1
						worker_hold[3] += 1
						worker_quality.update({worker:worker_hold})
					else:
						first = [0,0,1,1]
						worker_quality.update({worker:first})
	for c in aggregate:
		right = [x[2] for x in correct_full if x[0] == c[0] and x[1] == c[1]]
		if len(right) != 0:
			if c[2] in right:
				aggregate_data[0] += 1
				aggregate_data[1] += 1
				aggregate_data[2] += 1
				aggregate_data[3] += 1
			else:
				aggregate_data[0] += 1
				aggregate_data[1] += 0
				aggregate_data[2] += 1
				aggregate_data[3] += 1
		else:
			aggregate_data[0] += 0
			aggregate_data[1] += 0
			aggregate_data[2] += 1
			aggregate_data[3] += 1
	
	full_food_right = 0
	full_price_right = 0
	all_worker_id = list()
	all_food_plt = list()
	all_price_plt = list()
	last_plt_names = ["worker food percent correct", "aggregate food percent correct", "worker price percent correct ", "aggregate price percent correct"]
	for g,h in worker_quality.items():
		food_right = h[0]/h[2]
		price_right = h[1]/h[3]
		full_food_right += food_right
		full_price_right += price_right
		all_worker_id.append(g)
		all_food_plt.append(food_right)
		all_price_plt.append(price_right)
	all_worker_id.append("aggregate")
	a_food_right = aggregate_data[0] / aggregate_data[2]
	a_price_right = aggregate_data[1] / aggregate_data[3]
	w_food_right = full_food_right / len(worker_quality) 
	w_price_right = full_price_right / len(worker_quality)
	all_food_plt.append(a_food_right)
	all_price_plt.append(a_price_right)
	full_compare_plt = [w_food_right,a_food_right,w_price_right,a_price_right]

	plt.figure(1, figsize=(18, 8))

	plt.rc('xtick',labelsize=8)
	plt.rc('ytick',labelsize=8)
	plt.subplot(311)
	plt.ylabel("percent of food items correct")
	plt.xlabel("worker id")
	plt.title("Correct Food Items Percent from Each Worker and Aggregate Output")
	plt.bar(all_worker_id, all_food_plt)
	plt.subplot(312)
	plt.ylabel("percent of price items correct")
	plt.xlabel("worker id")
	plt.title("Correct Price Items Percent from Each Worker and Aggregate Output")
	plt.bar(all_worker_id, all_price_plt)
	plt.subplot(313)
	plt.ylabel("percent correct")
	plt.xlabel("average")
	plt.title("Comparison of Worker Average and Aggregate Output")
	plt.bar(last_plt_names, full_compare_plt)
	plt.tight_layout()
	plt.show()

def main():
	if len(sys.argv) != 2:
		print("argument real, test, or data are for creating website data, getting worker quality on test hit, or creating visuals of worker quality versus aggregate quality repectively")
	elif sys.argv[1] == "real":
		truck_data = pd.read_csv("../data/Class_HITS.csv")
		price_out = aggregation(truck_data);

		prices_data_frame = pd.DataFrame(price_out, columns=["Truck","Food", "Price"])
		prices_data_frame.to_csv("../data/menu.csv",index=False)

	elif sys.argv[1] == "test":
		test_data = pd.read_csv("../data/Test_Output_Correct.csv");
		worker_data = pd.read_csv("../data/Test.csv");
		worker_qual_test = worker_quality_test(test_data,worker_data);
		#assign_worker_qualifications(worker_qual_test)

	elif sys.argv[1] == "data":
		truck_data = pd.read_csv("../data/Class_HITS.csv")
		correct_data = pd.read_csv("../data/Test_Output_Correct.csv")
		aggregate_out = aggregation(truck_data);
		all_quality = worker_aggregate_quality(aggregate_out, truck_data, correct_data)

if __name__ == '__main__':
    main()