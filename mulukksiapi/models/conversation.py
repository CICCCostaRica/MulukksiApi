from mongoengine import *
import datetime
import json


class Conversation(Document):

    """
        This class represents a conversation between a potential new customer and a customer
        service agent. In a conversation messages can be exchanged and a Quote can be the 
        result of it. 
    """

    # -----------------------------------------------------------------------------------
    # CLASS ATTRIBUTES
    # -----------------------------------------------------------------------------------

    conversation_id = StringField(max_length=40, required=True)

    status = StringField(max_length=25, required=True)

    date_created = DateTimeField(default=datetime.datetime.now)

    parties = ListField(StringField(max_length=40))

    meta = {
        'indexes': [
            'conversation_id',
            'status'
        ]
    }

    # -----------------------------------------------------------------------------------
    # METHOD DICT
    # -----------------------------------------------------------------------------------
    def dict(self):
        """
            Creates a dictionary with current conversation's state
            :return: A dictionary representation of this class 
        """

        pparties = []

        for p in self.parties:
            pparties.append(p)

        return {
            "conversation_id ": self.conversation_id,
            "status": self.status,
            "date_created": self.date_created,
            "parties": pparties
        }

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def json(self):
        """
            Get a json string representation of the current application's state
            :return: json string
        """
        return json.dumps(self.dict())

    # -----------------------------------------------------------------------------------
    # METHOD JSON
    # -----------------------------------------------------------------------------------
    def add_participant(self, participant_id):
        """
            Adds a new participant into the conversation
            :param participant_id: The id of the user that will become a new participant of 
                                   the conversation
            :return: Nothing
        """
        self.parties.append(participant_id)
        self.save()
