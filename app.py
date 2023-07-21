from flask import Flask,jsonify
import pandas
from dataService.dataService import GaseousFuel,LiquidFuel,SolidFuel

app = Flask(__name__)

@app.route("/ConversionUnits")
def getConversionUnits():
    gs = GaseousFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.MeasureColumns.values.tolist()
    return jsonify(res)



# Region for GaseousFuels
@app.route('/GaseousFuels')
def getGaseusFuels():
    gs = GaseousFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetFuels().tolist()
    return jsonify(res)

@app.route('/UnitsForGaseousFuels/<string:fuelName>')
def getUnitsForGaseousFuels(fuelName):
    gs = GaseousFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetUnitsForFuel(fuelName).tolist()
    return jsonify(res)

@app.route("/EmissionsForGaseousFieldByAFU/<string:fName>/<string:uName>/<string:cName>")
def getEmissionsForGaseousFuel(fName,uName,cName):
    gs = GaseousFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetEmissionsForFieldByAFU(fName,uName,cName)
    return jsonify(res)
    


#Region for Liquidfuels
@app.route('/LiquidFuels')
def getLiquidFuels():
    gs = LiquidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetFuels().tolist()
    return jsonify(res)

@app.route('/UnitsForLiquidFuels/<string:fuelName>')
def getUnitsForLiquidFuels(fuelName):
    gs = LiquidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetUnitsForFuel(fuelName).tolist()
    return jsonify(res)

@app.route("/EmissionsForLiquidFieldByAFU/<string:fName>/<string:uName>/<string:cName>")
def getEmissionsForLiquidFuel(fName,uName,cName):
    gs = LiquidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetEmissionsForFieldByAFU(fName,uName,cName)
    return jsonify(res)


# Solid Fuels
@app.route('/SolidFuels')
def getSolidFuels():
    gs = SolidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetFuels().tolist()
    return jsonify(res)

@app.route('/UnitsForSolidFuels/<string:fuelName>')
def getUnitsForSolidFuels(fuelName):
    gs = SolidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetUnitsForFuel(fuelName).tolist()
    return jsonify(res)

@app.route("/EmissionsForSolidFieldByAFU/<string:fName>/<string:uName>/<string:cName>")
def getEmissionsForSolidFuel(fName,uName,cName):
    gs = SolidFuel("C:/Users/AnudeepAkula/Downloads/DBEIS_GHG-conversion-factors-2022-full-set.xls")
    res = gs.GetEmissionsForFieldByAFU(fName,uName,cName)
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug = True)