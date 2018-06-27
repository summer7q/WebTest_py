from Interfaces.blueprints import ecg


@ecg.route("/heartbeat", methods=["GET"])
def heartbeat():
	return "ok", 201


