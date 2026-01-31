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
            },status=status.HTTP_200_OK)

       
        history = request.session.get('chat_history', [])

   
        if not is_chocolate_query(message):
            return Response({
                "reply": "I specialize in our exquisite chocolate and nut collections. please ask about that?"
            },status=status.HTTP_200_OK)

     
        reply, updated_history = ask_gemini(message, history)

       
        request.session['chat_history'] = updated_history

        return Response({"reply": reply},status=status.HTTP_200_OK)
    

class ClearChatView(APIView):
    def post(self, request):
        if 'chat_history' in request.session:
            del request.session['chat_history']
            request.session.modified = True
        
        return Response(
            {"status": "success", "message": "Conversation history cleared."}, 
            status=status.HTTP_200_OK
        )