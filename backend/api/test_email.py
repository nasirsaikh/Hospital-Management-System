

from flask_restful import Resource
from utils.notifications import send_email


class TestEmail(Resource):
    def get(self):
        send_email(
            "myemails.855@gmail.com",
            "SMTP Test",
            "<p>If you got this, SMTP is working! 🎉</p>"
        )
        return {"message": "sent"}, 200
