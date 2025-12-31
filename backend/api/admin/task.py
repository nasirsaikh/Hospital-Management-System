from flask_restful import Resource
import redis, json

r = redis.Redis(host="localhost", port=6379, db=2)

class TaskLogsAPI(Resource):
    def get(self, task_id):
        data = r.get(task_id)
        if not data:
            return {"message": "Task not found"}, 404
        
        return json.loads(data), 200
