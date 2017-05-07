# flask_api server for vertretung
from flask import Flask, jsonify, abort
import json, codecs
import argparse
import untis_parser

parser = argparse.ArgumentParser(prog="untisparse")
parser.add_argument('--cron', action='store_true')
parser.add_argument('-d', '--destination', default="./html")
args = parser.parse_args()

plan = untis_parser.parseVertretungsplan(date.today().isocalendar()[1])
klassen = set([])
for x in plan:
	klassen.add(x)

if args.cron:
	with open("{}/vertretung.json".format(args.destination), "w") as f:
		json.dump([ob.__dict__ for ob in plan], codecs.getwriter('utf-8')(f), ensure_ascii=False)
else:
	app = Flask(__name__)


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