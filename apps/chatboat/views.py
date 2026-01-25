from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import ask_gemini
from .utils import is_chocolate_query,is_greeting,greeting_response

class ChatBotView(APIView):
    def post(self, request):
        message = request.data.get("message", "").strip()

        if not message:
            return Response(
                {"reply": "Please enter a message."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if is_greeting(message):
            return Response({
                "reply": greeting_response()
            })

        # 1. Retrieve existing history from the session (or empty list if new)
        history = request.session.get('chat_history', [])

        # 2. Safety Check / Guardrail
        if not is_chocolate_query(message):
            return Response({
                "reply": "I specialize in our exquisite chocolate and nut collections. How can I assist you with those today?"
            })

        # 3. Call service with history
        reply, updated_history = ask_gemini(message, history)

       
        request.session['chat_history'] = updated_history

        return Response({"reply": reply})
    

class ClearChatView(APIView):
    def post(self, request):
        if 'chat_history' in request.session:
            del request.session['chat_history']
            request.session.modified = True
        
        return Response(
            {"status": "success", "message": "Conversation history cleared."}, 
            status=status.HTTP_200_OK
        )