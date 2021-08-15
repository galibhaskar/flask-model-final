from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok
import pickle
import numpy as np

model = pickle.load(open('model1.pkl','rb'))

app=Flask(__name__)
run_with_ngrok(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/",methods=['GET'])
def home():
  return "hello world"

@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
  try:
    data=request.json
    formData=[]
    for key,value in data.items():
      formData.append(value)
    print(formData)
    #formData=[val for val in arr]
    #print(formData)
    data_pred=[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    
    data_pred[0][0]=int(formData[8])
    data_pred[0][1]=int(formData[9])
    data_pred[0][2]=int(formData[10])
    data_pred[0][3]=int(formData[11])
    data_pred[0][4]=float(formData[12])
    data_pred[0][5]=int(formData[18])
    data_pred[0][6]=int(formData[19])
    for val in formData:
      if val=='California':
        data_pred[0][7]=1
      if val=='Nevada':
        data_pred[0][8]=1
      if val=='Oregon':
        data_pred[0][9]=1
      if val=='Washington':
        data_pred[0][10]=1
      if val=='Yes':
        data_pred[0][11]=1
      if val=='Extended':
        data_pred[0][12]=1
      if val=='Premium':
        data_pred[0][13]=1
      if val=='College':
        data_pred[0][14]=1
      if val=='Doctor':
        data_pred[0][15]=1
      if val=='High School or Below':
        data_pred[0][16]=1
      if val=='Master':
        data_pred[0][17]=1
      if val=='Employed':
        data_pred[0][18]=1
      if val=='Medical Leave':
        data_pred[0][19]=1
      if val=='Retired':
        data_pred[0][20]=1
      if val=='Unemployed':
        data_pred[0][21]=1
      if val=='Male':
        data_pred[0][22]=1
      if val=='Suburban':
        data_pred[0][23]=1
      if val=='Urban':
        data_pred[0][24]=1
      if val=='Married':
        data_pred[0][25]=1
      if val=='Single':
        data_pred[0][26]=1
      if val=='L2':
        data_pred[0][27]=1
      if val=='L3':
        data_pred[0][28]=1
      if val=='Offer 2':
        data_pred[0][29]=1
      if val=='Offer 3':
        data_pred[0][30]=1
      if val=='Offer 4':
        data_pred[0][31]=1
      if val=='Branch':
        data_pred[0][32]=1
      if val=='Call Center':
        data_pred[0][33]=1
      if val=='Web':
        data_pred[0][34]=1
      if val=='Luxury Car':
        data_pred[0][35]=1
      if val=='Luxury SUV':
        data_pred[0][36]=1
      if val=='SUV':
        data_pred[0][37]=1
      if val=='Sports Car':
        data_pred[0][38]=1
      if val=='Two-Door Car':
        data_pred[0][39]=1
      if val=='Medsize':
        data_pred[0][40]=1
      if val=='Small':
        data_pred[0][41]=1
    pred=model.predict(data_pred)
    pred=np.exp(pred)/10
    pred_offers=offers(pred[0], formData[15])
    return jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": {
            "clv":pred[0],
            "offers":pred_offers
        }
				})
    
  except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})

  #print(data_pred)

loyalty_points=['2x','3X','5X','7X','10X']
coverage_plan=['Basic','Extended','Premium','Other Premium Options']
discount_percentage=[35,30,20,15,10]
plan_price=[5000,7000,10000]

def getDiscount(price, discount):
  price=price-(price*discount)/100
  return price

def offers(clv, coverage):
  final_pred=[]
  offer_array=[
          {'loyaltyPoints':'2X','plan':'Basic', 'currentPrice':plan_price[0],'discountPercentage':35, 'planPrice':getDiscount(plan_price[0], 35)},
          {'loyaltyPoints':'3X','plan':'Basic','currentPrice':plan_price[0],'discountPercentage':30, 'planPrice':getDiscount(plan_price[0], 30)},
          {'loyaltyPoints':'5X','plan':'Extended','currentPrice':plan_price[1],'discountPercentage':20, 'planPrice':getDiscount(plan_price[1], 20)},
          {'loyaltyPoints':'7X','plan':'Premium','currentPrice':plan_price[2],'discountPercentage':15, 'planPrice':getDiscount(plan_price[2], 15)},
          {'loyaltyPoints':'10X','plan':'Other Premium Services','currentPrice':plan_price[2],'discountPercentage':10, 'planPrice':getDiscount(plan_price[2], discount_percentage[2])}
         ]
 
  if clv>6000:
    if coverage=='Basic':
      return offer_array[2:5]
    elif coverage=='Extended':
      return offer_array[3:5]
    else:
      return offer_array[4:5]
  if clv>3000 and clv<6000:
    return offer_array[1:5]
  if clv<3000:
    return offer_array[0:5]

if __name__=="__main__":
  app.run()