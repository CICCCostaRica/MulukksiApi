from flask import request, jsonify
from mulukksiapi import app
from mulukksiapi.models.conversation import Conversation
from flask_jwt import jwt_required, current_identity
import uuid


# --------------------------------------------------------------------------
#  POST /api/v1/conversation
# --------------------------------------------------------------------------
@app.route('/api/v1/conversation', methods=['POST'])
@jwt_required()
def post_conversation():
    """
        This endpoint allows us to create a new conversation. To create a new 
        conversation the following payload must be provided:
        
        :return: returns a json representation of the new conversation entity
    """

    creator_id = current_identity.id
    conversation = Conversation(
        conversation_id=str(uuid.uuid4()),
        status="new"
    )
    conversation.add_participant(creator_id)
    conversation.save()
    app.logger.info("A new conversation initiated by " + creator_id + " was successfully allocated")
    return jsonify(conversation.dict())


# --------------------------------------------------------------------------
#  POST /api/v1/conversation/<conversation_id>/participant
# --------------------------------------------------------------------------
@app.route('/api/v1/conversation/<conversation_id>/participant', methods=['POST'])
@jwt_required()
def post_participant(conversation_id):
    conversation = Conversation.objects.get(conversation_id=conversation_id)
    conversation.add_participant(current_identity.id)
    return jsonify(conversation.dict())


# --------------------------------------------------------------------------
#  GET /api/v1/conversation/<conversation_id>
# --------------------------------------------------------------------------
@app.route('/api/v1/conversation/<conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    conversation = Conversation.objects.get(conversation_id = conversation_id)
    return jsonify(conversation.dict())


# --------------------------------------------------------------------------
#  GET /api/v1/conversation/status/<status_id>
# --------------------------------------------------------------------------
@app.route('/api/v1/conversation/status/<status_id>', methods=['GET'])
@jwt_required()
def get_conversations(status_id):
    conversation = Conversation.objects.filter(status = status_id)
    conversations = []
    for count in conversation:
        conversations.append(count.dict())
    return jsonify(conversations)