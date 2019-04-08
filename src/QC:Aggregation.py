import pandas as pd

def aggregation(truck_data):
	trucks = dict()
	full = list()
	aggr_out = dict()
	for x in truck_data.index:
		name = truck_data.loc[x,"Truck Name"].lower()
		for y in range(1,5):
			food = "FoodItem" + str(y)
			data_food = truck_data.loc[x,food].lower()
			price = "Price" + str(y)
			data_price = "{0:.2f}".format(truck_data.loc[x,price])
			truck_food = trucks.get(name)
			if truck_food == None:
				foods = dict()
				prices = dict()
				prices.update({data_price:1})
				foods.update({data_food:prices})
				trucks.update({name:foods})
			else:
				food_price = truck_food.get(data_food)
				if food_price == None:
					prices = dict()
					prices.update({data_price:1})
					truck_food.update({data_food:prices})
				else:
					price_last = food_price.get(data_price)
					if price_last == None:
						food_price.update({data_price:1})
					else:
						price_last = price_last + 1
						food_price.update({data_price:price_last})
	for truck, foods in trucks.items():
		for food, prices in foods.items():
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

def main():

	truck_data = pd.read_csv("../data/nets213sampleprojectdata.csv")
	price_out, quality_in = aggregation(truck_data);
	worker_quality = quality_control(truck_data, quality_in);

	prices_data_frame = pd.DataFrame(price_out, columns=["Truck","Food", "Price"])
	prices_data_frame.to_csv("../data/menu.csv",index=False)

	quality_data_frame = pd.DataFrame(worker_quality, columns=["UserId","quality"])
	quality_data_frame.to_csv("../data/quality.csv", index=False)


if __name__ == '__main__':
    main()