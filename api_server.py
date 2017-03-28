# flask_api server for vertretung
from flask import Flask, jsonify, abort
import json
import untis_parser

app = Flask(__name__)
plan = untis_parser.parseVertretungsplan()
klassen = set([])
for x in plan:
	klassen.add(x)

@app.route("/vertretung", methods=['GET'])
def vertretungsplan():
	return json.dumps([ob.__dict__ for ob in plan], ensure_ascii=False)

@app.route("/vertretung/<klasse>", methods=['GET'])
def vertretungsplan_by_klasse(klasse):
	plan_by_klasse = []
	for x in plan:
		if x.klasse == klasse:
			plan_by_klasse.append(x)
	return json.dumps([ob.__dict__ for ob in plan_by_klasse], ensure_ascii=False)

if __name__ == "__main__":
	app.run()