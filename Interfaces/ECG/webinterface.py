from Interfaces.blueprints import ecg
from flask import jsonify, request
from queue import Queue, Empty

allow_list = ["ECG001", "ECG002"]

_taskQ = Queue()


def putTask(task):
    """
    向任务队列加入一个task
    :param task:
    :return:
    """
    _taskQ.put_nowait(task)


def flush():
    """
    清空任务队列
    :return:
    """
    with _taskQ.mutex:
        unfinished = _taskQ.unfinished_tasks - len(_taskQ.queue)
        if unfinished <= 0:
            if unfinished < 0:
                raise ValueError('task_done() called too many times')
            _taskQ.all_tasks_done.notify_all()
        _taskQ.unfinished_tasks = unfinished
        _taskQ.queue.clear()
        _taskQ.not_full.notify_all()


@ecg.route("/heartbeat", methods=["POST"])
def heartbeat():
    j = request.json
    retdata = {
        "type": "HC",
        "ack": False,
        "version": "0.1",
        "data": {
            "heartbeatID": 1,
            "Command": ""
        }
    }
    try:

        if j["type"] == "HR" and j["data"]["deviceType"] == "ECG" and j["data"]["deviceID"] in allow_list:
            try:
                task = _taskQ.get_nowait()
                if task == "DataStart":
                    retdata["data"]["Command"] = "DataStart"
                elif task == "DataEnd":
                    retdata["data"]["Command"] = "DataEnd"
            except Empty:
                pass
            return jsonify(retdata), 201
        else:
            return "error", 401
    except Exception as e:
        return repr(e), 404


@ecg.route("/login", methods=["POST"])
def login():
    retdata = {
        "type": "LC",
        "ack": False,
        "version": "0.1",
        "data": {
            "confirm": True,
            "faultCode": ""
        }
    }
    try:
        j = request.json
        if j["type"] == "LR" and j["data"]["deviceType"] == "ECG" and j["data"]["deviceID"] in allow_list:
            pass
        else:
            retdata["data"]["confirm"] = False
            retdata["data"]["faultCode"] = "Unknown Device!"
        return jsonify(retdata), 201
    except Exception as e:
        retdata["data"]["confirm"] = False
        retdata["data"]["faultCode"] = "Format Error: %s" % repr(e)
        return jsonify(retdata), 404


@ecg.route("/senddata", methods=["POST"])
def senddata():
    try:
        data = request.json
        # todo 解析数据
        return "ok", 201
    except Exception as e:
        return repr(e), 404
